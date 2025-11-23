"""
Aplicação GUI Nativa - Windows Desktop Application
Interface gráfica profissional usando PyQt5
"""
import sys
import os
from pathlib import Path
from typing import List, Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QComboBox, QPushButton, QProgressBar,
    QFileDialog, QListWidget, QGroupBox, QMessageBox, QSplitter,
    QScrollArea, QFrame, QStatusBar, QTabWidget
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap

from job_manager import JobManager
from audio_generator import AudioGenerator
from utils import get_logger

logger = get_logger(__name__)

class WorkerThread(QThread):
    """Thread para processar vídeo sem travar a interface"""
    progress = pyqtSignal(str, int)  # (mensagem, porcentagem)
    finished = pyqtSignal(str, bool)  # (resultado, sucesso)
    error = pyqtSignal(str)

    def __init__(self, job_manager, text, voice, model, images):
        super().__init__()
        self.job_manager = job_manager
        self.text = text
        self.voice = voice
        self.model = model
        self.images = images

    def run(self):
        """Executa processamento em background"""
        try:
            # Cria job
            self.progress.emit("Criando job...", 5)
            job, error = self.job_manager.create_job(
                input_text=self.text,
                voice_name=self.voice,
                image_paths=self.images,
                model_id=self.model
            )

            if error:
                self.error.emit(f"Erro na validação: {error}")
                return

            # Processa job
            def update_progress(msg: str, percent: int):
                self.progress.emit(msg, percent)

            final_video = self.job_manager.process_job(job, update_progress)

            self.finished.emit(str(final_video), True)

        except Exception as e:
            logger.error(f"Erro no processamento: {e}", exc_info=True)
            self.error.emit(str(e))


class LipSyncApp(QMainWindow):
    """Aplicação Principal - GUI Nativa do Windows"""

    def __init__(self):
        super().__init__()
        self.job_manager = JobManager()
        self.audio_generator = AudioGenerator()
        self.image_paths = []
        self.worker = None

        self.init_ui()

    def init_ui(self):
        """Inicializa a interface gráfica"""
        self.setWindowTitle("LipSync Video Generator - Profissional")
        self.setGeometry(100, 100, 1200, 800)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Splitter para dividir tela
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # === PAINEL ESQUERDO ===
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # === PAINEL DIREITO ===
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        # Proporção 60-40
        splitter.setStretchFactor(0, 6)
        splitter.setStretchFactor(1, 4)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto para gerar vídeos")

        # Estilo moderno
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QTextEdit, QComboBox, QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                background-color: #e0e0e0;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 5px;
            }
        """)

    def create_left_panel(self):
        """Cria painel esquerdo (inputs)"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # === ROTEIRO ===
        script_group = QGroupBox("📝 Roteiro do Vídeo")
        script_layout = QVBoxLayout()

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "Digite ou cole o texto completo do seu roteiro aqui...\n\n"
            "Cada parágrafo será processado separadamente.\n"
            "O sistema divide automaticamente em batches de 3 parágrafos."
        )
        self.text_input.setMinimumHeight(200)
        script_layout.addWidget(self.text_input)

        script_group.setLayout(script_layout)
        layout.addWidget(script_group)

        # === CONFIGURAÇÕES DE VOZ ===
        voice_group = QGroupBox("🎤 Configurações de Voz")
        voice_layout = QVBoxLayout()

        # Voz
        voice_layout.addWidget(QLabel("Selecione a Voz (ElevenLabs):"))
        self.voice_combo = QComboBox()
        self.load_voices()
        voice_layout.addWidget(self.voice_combo)

        # Modelo
        voice_layout.addWidget(QLabel("Modelo de Voz:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "eleven_multilingual_v2 (Melhor qualidade)",
            "eleven_turbo_v2_5 (Mais rápido)",
            "eleven_turbo_v2 (Rápido)",
            "eleven_multilingual_v1 (Legado)",
            "eleven_monolingual_v1 (Inglês)"
        ])
        voice_layout.addWidget(self.model_combo)

        voice_group.setLayout(voice_layout)
        layout.addWidget(voice_group)

        # === IMAGENS ===
        images_group = QGroupBox("🖼️ Imagens do Apresentador")
        images_layout = QVBoxLayout()

        # Botão de upload
        upload_btn = QPushButton("📁 Adicionar Imagens (PNG/JPG)")
        upload_btn.clicked.connect(self.select_images)
        images_layout.addWidget(upload_btn)

        # Lista de imagens
        self.images_list = QListWidget()
        self.images_list.setMaximumHeight(150)
        images_layout.addWidget(self.images_list)

        # Botão remover
        remove_btn = QPushButton("🗑️ Remover Selecionadas")
        remove_btn.setStyleSheet("background-color: #d13438;")
        remove_btn.clicked.connect(self.remove_images)
        images_layout.addWidget(remove_btn)

        images_group.setLayout(images_layout)
        layout.addWidget(images_group)

        # === BOTÕES DE AÇÃO ===
        buttons_layout = QHBoxLayout()

        # Estimar
        estimate_btn = QPushButton("📊 Estimar Custo")
        estimate_btn.clicked.connect(self.estimate_cost)
        buttons_layout.addWidget(estimate_btn)

        # Gerar
        self.generate_btn = QPushButton("🎬 GERAR VÍDEO")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                font-size: 16px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #0e6b0e;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_video)
        buttons_layout.addWidget(self.generate_btn)

        layout.addLayout(buttons_layout)

        # Espaçador
        layout.addStretch()

        return panel

    def create_right_panel(self):
        """Cria painel direito (progresso e resultado)"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # === PROGRESSO ===
        progress_group = QGroupBox("⚙️ Progresso do Processamento")
        progress_layout = QVBoxLayout()

        # Label de status
        self.status_label = QLabel("Aguardando início...")
        self.status_label.setWordWrap(True)
        progress_layout.addWidget(self.status_label)

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # === LOGS ===
        logs_group = QGroupBox("📋 Logs do Sistema")
        logs_layout = QVBoxLayout()

        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setMaximumHeight(200)
        self.logs_text.setPlaceholderText("Logs aparecerão aqui durante o processamento...")
        logs_layout.addWidget(self.logs_text)

        # Botão limpar logs
        clear_logs_btn = QPushButton("🗑️ Limpar Logs")
        clear_logs_btn.clicked.connect(lambda: self.logs_text.clear())
        logs_layout.addWidget(clear_logs_btn)

        logs_group.setLayout(logs_layout)
        layout.addWidget(logs_group)

        # === RESULTADO ===
        result_group = QGroupBox("✅ Vídeo Final")
        result_layout = QVBoxLayout()

        self.result_label = QLabel("Nenhum vídeo gerado ainda")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        result_layout.addWidget(self.result_label)

        # Botão abrir vídeo
        self.open_video_btn = QPushButton("📂 Abrir Vídeo")
        self.open_video_btn.setEnabled(False)
        self.open_video_btn.clicked.connect(self.open_video)
        result_layout.addWidget(self.open_video_btn)

        # Botão abrir pasta
        self.open_folder_btn = QPushButton("📁 Abrir Pasta do Vídeo")
        self.open_folder_btn.setEnabled(False)
        self.open_folder_btn.clicked.connect(self.open_folder)
        result_layout.addWidget(self.open_folder_btn)

        result_group.setLayout(result_layout)
        layout.addWidget(result_group)

        # Espaçador
        layout.addStretch()

        return panel

    def load_voices(self):
        """Carrega vozes do ElevenLabs"""
        try:
            self.log("Carregando vozes do ElevenLabs...")
            voices = self.audio_generator.get_available_voices()

            if voices:
                for voice in voices:
                    self.voice_combo.addItem(voice['name'])
                self.log(f"✅ {len(voices)} vozes carregadas")
            else:
                self.voice_combo.addItem("⚠️ Nenhuma voz disponível")
                self.log("⚠️ Nenhuma voz encontrada. Verifique API key.")
        except Exception as e:
            self.log(f"❌ Erro ao carregar vozes: {e}")
            self.voice_combo.addItem("❌ Erro ao conectar")

    def select_images(self):
        """Abre diálogo para selecionar imagens"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecione Imagens do Apresentador",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if files:
            for file in files:
                if file not in self.image_paths:
                    self.image_paths.append(file)
                    self.images_list.addItem(Path(file).name)

            self.log(f"✅ {len(files)} imagem(ns) adicionada(s)")

    def remove_images(self):
        """Remove imagens selecionadas"""
        selected = self.images_list.selectedItems()
        if not selected:
            return

        for item in selected:
            row = self.images_list.row(item)
            self.images_list.takeItem(row)
            if row < len(self.image_paths):
                self.image_paths.pop(row)

        self.log(f"🗑️ {len(selected)} imagem(ns) removida(s)")

    def estimate_cost(self):
        """Estima custo e tempo"""
        text = self.text_input.toPlainText()

        if not text.strip():
            QMessageBox.warning(self, "Aviso", "Digite um texto para estimar!")
            return

        try:
            estimate = self.job_manager.get_job_estimate(text)

            msg = f"""
📊 ESTIMATIVA DE PROCESSAMENTO

📝 Análise do Texto:
  • Caracteres: {estimate['num_chars']:,}
  • Batches: {estimate['num_batches']}
  • Vídeos a gerar: {estimate['num_videos']}

⏱️ Tempo Estimado: {estimate['estimated_time']}

💰 Custo Estimado:
  • Gemini: {estimate['estimated_cost']['gemini']}
  • ElevenLabs: {estimate['estimated_cost']['elevenlabs']}
  • WaveSpeed: {estimate['estimated_cost']['wavespeed']}
  • TOTAL: {estimate['estimated_cost']['total']}

ℹ️ Valores são aproximados
"""
            QMessageBox.information(self, "Estimativa", msg)
            self.log("📊 Estimativa calculada")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao estimar: {e}")

    def generate_video(self):
        """Inicia geração de vídeo"""
        # Validações
        text = self.text_input.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Aviso", "Digite um roteiro!")
            return

        if not self.image_paths:
            QMessageBox.warning(self, "Aviso", "Adicione pelo menos 1 imagem!")
            return

        voice = self.voice_combo.currentText()
        if "⚠️" in voice or "❌" in voice:
            QMessageBox.warning(self, "Aviso", "Selecione uma voz válida!")
            return

        # Modelo
        model_text = self.model_combo.currentText()
        model = model_text.split(" ")[0]  # Extrai ID do modelo

        # Confirmação
        reply = QMessageBox.question(
            self,
            "Confirmar Geração",
            f"Iniciar geração de vídeo?\n\n"
            f"• Roteiro: {len(text)} caracteres\n"
            f"• Voz: {voice}\n"
            f"• Modelo: {model}\n"
            f"• Imagens: {len(self.image_paths)}\n\n"
            f"Este processo pode levar vários minutos.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # Desabilita botão
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("⏳ Processando...")

        # Limpa resultado anterior
        self.result_label.setText("Processando...")
        self.open_video_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)
        self.logs_text.clear()

        # Inicia worker thread
        self.worker = WorkerThread(
            self.job_manager,
            text,
            voice,
            model,
            self.image_paths
        )
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

        self.log("🚀 Iniciando processamento...")

    def update_progress(self, message: str, percent: int):
        """Atualiza progresso"""
        self.status_label.setText(message)
        self.progress_bar.setValue(percent)
        self.status_bar.showMessage(message)
        self.log(f"[{percent}%] {message}")

    def on_finished(self, video_path: str, success: bool):
        """Chamado quando processamento termina"""
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("🎬 GERAR VÍDEO")

        if success:
            self.result_label.setText(f"✅ Vídeo gerado com sucesso!\n\n{video_path}")
            self.open_video_btn.setEnabled(True)
            self.open_folder_btn.setEnabled(True)
            self.final_video_path = video_path

            self.log("✅ PROCESSAMENTO CONCLUÍDO!")

            QMessageBox.information(
                self,
                "Sucesso!",
                f"Vídeo gerado com sucesso!\n\n{video_path}"
            )

    def on_error(self, error_msg: str):
        """Chamado quando há erro"""
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("🎬 GERAR VÍDEO")

        self.result_label.setText(f"❌ Erro: {error_msg}")
        self.log(f"❌ ERRO: {error_msg}")

        QMessageBox.critical(
            self,
            "Erro no Processamento",
            f"Ocorreu um erro:\n\n{error_msg}"
        )

    def open_video(self):
        """Abre o vídeo gerado"""
        if hasattr(self, 'final_video_path'):
            os.startfile(self.final_video_path)

    def open_folder(self):
        """Abre a pasta do vídeo"""
        if hasattr(self, 'final_video_path'):
            folder = Path(self.final_video_path).parent
            os.startfile(folder)

    def log(self, message: str):
        """Adiciona mensagem aos logs"""
        self.logs_text.append(message)
        # Auto-scroll
        self.logs_text.verticalScrollBar().setValue(
            self.logs_text.verticalScrollBar().maximum()
        )


def main():
    """Ponto de entrada da aplicação"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno

    # Fonte padrão
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Janela principal
    window = LipSyncApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
