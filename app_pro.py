"""
LipSync Video Generator - Interface Profissional
Sistema completo de gerenciamento e geração de vídeos com IA
"""
import gradio as gr
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime
import json

from config import Config
from job_manager import JobManager
from audio_generator import AudioGenerator
from project_manager import ProjectManager
from utils import get_logger

logger = get_logger(__name__)

# Inicializa gerenciadores
project_manager = ProjectManager()

# CSS customizado para tema claro
CUSTOM_CSS = """
/* Tema Claro Profissional */
:root {
    --primary-color: #1e88e5;
    --secondary-color: #7b2cbf;
    --success-color: #00c853;
    --warning-color: #ff9800;
    --danger-color: #f44336;
    --bg-white: #ffffff;
    --bg-light: #f5f5f5;
    --bg-card: #ffffff;
    --text-dark: #212121;
    --text-muted: #757575;
    --border-light: #e0e0e0;
}

.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%) !important;
}

/* Header Estilizado */
.app-header {
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    padding: 2rem;
    border-radius: 1rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 16px rgba(30, 136, 229, 0.2);
}

.app-header h1 {
    color: white !important;
    font-weight: 800 !important;
    font-size: 2.5rem !important;
    margin: 0 !important;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.app-header p {
    color: rgba(255, 255, 255, 0.95) !important;
    font-size: 1.1rem !important;
    margin-top: 0.5rem !important;
}

/* Cards */
.stat-card {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 1rem !important;
    padding: 1.5rem !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    transition: all 0.3s ease !important;
}

.stat-card:hover {
    border-color: var(--primary-color) !important;
    box-shadow: 0 4px 16px rgba(30, 136, 229, 0.15) !important;
    transform: translateY(-2px) !important;
}

.stat-number {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    color: var(--primary-color) !important;
    line-height: 1 !important;
}

.stat-label {
    font-size: 0.9rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin-top: 0.5rem !important;
}

/* Tabs Modernos */
.tab-nav button {
    background: var(--bg-white) !important;
    border: 1px solid var(--border-light) !important;
    color: var(--text-dark) !important;
    border-radius: 0.5rem !important;
    margin-right: 0.5rem !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.tab-nav button.selected {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
    border-color: var(--primary-color) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3) !important;
}

/* Inputs e Dropdowns */
input, textarea, select {
    background: var(--bg-white) !important;
    border: 1px solid var(--border-light) !important;
    color: var(--text-dark) !important;
    border-radius: 0.5rem !important;
    padding: 0.75rem !important;
}

input:focus, textarea:focus, select:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1) !important;
}

/* Botões */
.primary-btn {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
    border: none !important;
    color: white !important;
    padding: 1rem 2rem !important;
    border-radius: 0.5rem !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3) !important;
    transition: all 0.3s ease !important;
}

.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(30, 136, 229, 0.4) !important;
}

.secondary-btn {
    background: var(--bg-white) !important;
    border: 1px solid var(--primary-color) !important;
    color: var(--primary-color) !important;
}

/* Progress Bar */
.progress-container {
    background: var(--bg-card) !important;
    border-radius: 1rem !important;
    padding: 1.5rem !important;
    border: 1px solid var(--border-light) !important;
}

.progress-bar {
    height: 1rem !important;
    background: linear-gradient(90deg, var(--primary-color), var(--success-color)) !important;
    border-radius: 0.5rem !important;
    box-shadow: 0 2px 8px rgba(0, 200, 83, 0.3) !important;
}

/* Log Terminal */
.log-terminal {
    background: #1e1e1e !important;
    color: #00c853 !important;
    font-family: 'Fira Code', 'Courier New', monospace !important;
    border-radius: 0.5rem !important;
    padding: 1rem !important;
    border: 1px solid var(--border-light) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

/* Avatar Grid */
.avatar-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
    padding: 1rem;
}

.avatar-item {
    background: var(--bg-card);
    border: 2px solid var(--border-light);
    border-radius: 0.75rem;
    padding: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.avatar-item:hover {
    border-color: var(--primary-color);
    box-shadow: 0 4px 12px rgba(30, 136, 229, 0.2);
    transform: scale(1.05);
}

.avatar-item.selected {
    border-color: var(--success-color);
    box-shadow: 0 0 16px rgba(0, 200, 83, 0.3);
}

/* Status Badges */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
}

.badge-success {
    background: rgba(0, 200, 83, 0.1);
    color: var(--success-color);
    border: 1px solid var(--success-color);
}

.badge-processing {
    background: rgba(30, 136, 229, 0.1);
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
}

.badge-error {
    background: rgba(244, 67, 54, 0.1);
    color: var(--danger-color);
    border: 1px solid var(--danger-color);
}

/* Video Gallery */
.video-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    padding: 1rem;
}

.video-card {
    background: var(--bg-card);
    border-radius: 1rem;
    overflow: hidden;
    border: 1px solid var(--border-light);
    transition: all 0.3s ease;
}

.video-card:hover {
    border-color: var(--primary-color);
    box-shadow: 0 8px 20px rgba(30, 136, 229, 0.2);
    transform: translateY(-4px);
}

/* Accordion */
.accordion-header {
    background: var(--bg-white) !important;
    color: var(--text-dark) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 0.5rem !important;
}

/* Markdown Customizado */
.markdown-text {
    color: var(--text-dark) !important;
}

.markdown-text h1, .markdown-text h2, .markdown-text h3 {
    color: var(--primary-color) !important;
}

.markdown-text code {
    background: rgba(30, 136, 229, 0.1) !important;
    color: var(--primary-color) !important;
    padding: 0.2rem 0.4rem !important;
    border-radius: 0.25rem !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: var(--bg-light);
}

::-webkit-scrollbar-thumb {
    background: var(--primary-color);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--secondary-color);
}
"""

def get_audio_provider_choices() -> List[tuple]:
    """Retorna lista de provedores de áudio disponíveis"""
    providers = []
    if Config.ELEVENLABS_API_KEY:
        providers.append(("🎙️ ElevenLabs (Text-to-Speech v3)", "elevenlabs"))
    if Config.MINIMAX_API_KEY:
        providers.append(("🎵 MiniMax Audio (Text-to-Speech)", "minimax"))
    if not providers:
        providers.append(("⚠️ Nenhum provedor configurado", "none"))
    return providers

def get_voice_choices(provider: str = None) -> List[str]:
    """Obtém lista de vozes disponíveis"""
    try:
        if provider is None or provider == 'none':
            provider = Config.AUDIO_PROVIDER

        audio_gen = AudioGenerator(provider=provider)
        voices = audio_gen.get_available_voices()

        if voices and len(voices) > 0:
            return [voice['name'] for voice in voices]
        return [f"⚠️ Configure API Key do {provider}"]
    except Exception as e:
        logger.error(f"Erro ao obter vozes: {e}")
        return [f"❌ Erro ao conectar"]

def update_voices_by_provider(provider: str):
    """Atualiza vozes quando provedor muda"""
    voices = get_voice_choices(provider)
    return gr.Dropdown(choices=voices, value=voices[0] if voices else None)

def format_duration(seconds: float) -> str:
    """Formata duração em segundos para string legível"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}min"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def get_dashboard_stats() -> tuple:
    """Retorna estatísticas para o dashboard"""
    stats = project_manager.get_stats()
    projects = len(project_manager.list_projects())
    avatars = len(project_manager.list_avatars())
    templates = len(project_manager.list_templates())

    return (
        stats['total_videos'],
        projects,
        avatars,
        templates,
        format_duration(stats['total_duration']),
        f"{stats['total_chars']:,} caracteres"
    )

def create_project_interface(name: str, description: str) -> str:
    """Cria novo projeto"""
    try:
        if not name or not name.strip():
            return "❌ Nome do projeto é obrigatório"

        project = project_manager.create_project(name.strip(), description.strip())

        return f"""✅ **Projeto Criado com Sucesso!**

📁 **Nome:** {project['name']}
🆔 **ID:** `{project['id']}`
📝 **Descrição:** {project['description'] or 'Sem descrição'}
📅 **Criado em:** {datetime.fromisoformat(project['created_at']).strftime('%d/%m/%Y %H:%M')}
📂 **Pasta:** `{project['path']}`

O projeto está pronto para receber vídeos!
"""
    except Exception as e:
        logger.error(f"Erro ao criar projeto: {e}")
        return f"❌ Erro ao criar projeto: {str(e)}"

def list_projects_interface() -> str:
    """Lista todos os projetos"""
    projects = project_manager.list_projects()

    if not projects:
        return "📭 **Nenhum projeto criado ainda**\n\nCrie seu primeiro projeto na aba 'Novo Projeto'!"

    output = f"📂 **Total de Projetos:** {len(projects)}\n\n---\n\n"

    for project in sorted(projects, key=lambda x: x['created_at'], reverse=True):
        status_badge = "🟢 ATIVO" if project['status'] == 'active' else "⚪ ARQUIVADO"
        videos_count = len(project['videos'])

        output += f"""
### {project['name']} {status_badge}

- **ID:** `{project['id']}`
- **Descrição:** {project['description'] or 'Sem descrição'}
- **Criado em:** {datetime.fromisoformat(project['created_at']).strftime('%d/%m/%Y %H:%M')}
- **Vídeos:** {videos_count}
- **Pasta:** `{project['path']}`

---
"""

    return output

def process_video_generation_pro(
    project_id: str,
    text: str,
    provider: str,
    voice_name: str,
    model_id: str,
    images: List[gr.File],
    max_workers: int,
    progress=gr.Progress()
) -> Tuple[Optional[str], str, str]:
    """Processa geração de vídeo com sistema profissional"""

    # Logs iniciais
    logs = []

    def log(message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        logs.append(log_entry)
        return "\n".join(logs)

    try:
        # Valida projeto
        if not project_id or project_id == "none":
            return None, "", "❌ Selecione um projeto"

        project = project_manager.get_project(project_id)
        if not project:
            return None, "", "❌ Projeto não encontrado"

        # Valida inputs
        if not text or not text.strip():
            return None, "", "❌ Digite o roteiro do vídeo"

        if not images or len(images) == 0:
            return None, "", "❌ Faça upload de pelo menos uma imagem"

        log(f"🚀 Iniciando geração de vídeo para projeto: {project['name']}")
        log(f"📊 Provedor de áudio: {provider}")
        log(f"🎤 Voz selecionada: {voice_name}")
        log(f"📝 Tamanho do roteiro: {len(text)} caracteres")

        # Extrai paths das imagens
        image_paths = []
        for img in images:
            if hasattr(img, 'name'):
                image_paths.append(img.name)
            elif isinstance(img, str):
                image_paths.append(img)

        log(f"🖼️ Imagens carregadas: {len(image_paths)}")

        # Cria job manager
        progress(0, desc="Inicializando sistema...")
        job_mgr = JobManager(audio_provider=provider)

        log("✅ JobManager inicializado")

        # Cria job
        progress(5, desc="Criando job...")
        job, error = job_mgr.create_job(
            input_text=text,
            voice_name=voice_name,
            image_paths=image_paths,
            model_id=model_id
        )

        if error:
            log(f"❌ Erro na validação: {error}", "ERROR")
            return None, log(""), f"❌ Erro na validação: {error}"

        log(f"✅ Job criado: {job.job_id}")

        # Processa job
        def update_progress(message: str, percent: int):
            progress(percent / 100, desc=message)
            log(f"⏳ {message} ({percent}%)")

        log("🎬 Iniciando processamento...")
        final_video = job_mgr.process_job(
            job=job,
            progress_callback=update_progress,
            max_workers_video=max_workers
        )

        log("✅ Vídeo gerado com sucesso!")

        # Adiciona vídeo ao projeto
        video_info = {
            'job_id': job.job_id,
            'path': str(final_video),
            'created_at': datetime.now().isoformat(),
            'chars': len(text),
            'duration': (job.completed_at - job.created_at).total_seconds()
        }

        project_manager.add_video_to_project(project_id, video_info)
        project_manager.update_stats(len(text), video_info['duration'])

        log(f"📂 Vídeo adicionado ao projeto: {project['name']}")

        # Mensagem de sucesso
        success_message = f"""
<div class="stat-card">

## ✅ Vídeo Gerado com Sucesso!

### 📊 Informações do Processo

- **🆔 Job ID:** `{job.job_id}`
- **📁 Projeto:** {project['name']}
- **📹 Arquivo:** `{final_video.name}`
- **⏱️ Tempo de Processamento:** {format_duration(video_info['duration'])}
- **📝 Caracteres Processados:** {video_info['chars']:,}
- **🔊 Provedor de Áudio:** {provider.upper()}
- **🎤 Voz Utilizada:** {voice_name}

### 📂 Localização

```
{final_video}
```

</div>
"""

        log("🎉 Processo finalizado com sucesso!")

        return str(final_video), success_message, log("")

    except Exception as e:
        error_msg = f"❌ Erro durante processamento: {str(e)}"
        log(error_msg, "ERROR")
        logger.error(error_msg)
        return None, "", log("")

def create_dashboard_tab():
    """Cria aba do dashboard"""
    with gr.Tab("📊 Dashboard"):
        gr.Markdown("""
        <div class="app-header">
            <h1>🎬 LipSync Video Generator</h1>
            <p>Sistema Profissional de Geração de Vídeos com Inteligência Artificial</p>
        </div>
        """)

        # Estatísticas
        with gr.Row():
            total_videos = gr.Markdown("0", elem_classes=["stat-card"])
            total_projects = gr.Markdown("0", elem_classes=["stat-card"])
            total_avatars = gr.Markdown("0", elem_classes=["stat-card"])
            total_templates = gr.Markdown("0", elem_classes=["stat-card"])

        with gr.Row():
            total_duration = gr.Markdown("0s", elem_classes=["stat-card"])
            total_chars = gr.Markdown("0", elem_classes=["stat-card"])

        refresh_stats_btn = gr.Button("🔄 Atualizar Estatísticas", size="sm")

        # Vídeos recentes
        gr.Markdown("## 🎥 Vídeos Recentes")
        recent_videos = gr.Markdown("Nenhum vídeo gerado ainda")

        def update_dashboard():
            videos, projects, avatars, templates, duration, chars = get_dashboard_stats()

            videos_md = f"""
<div class="stat-card">
<div class="stat-number">{videos}</div>
<div class="stat-label">Vídeos Gerados</div>
</div>
"""

            projects_md = f"""
<div class="stat-card">
<div class="stat-number">{projects}</div>
<div class="stat-label">Projetos</div>
</div>
"""

            avatars_md = f"""
<div class="stat-card">
<div class="stat-number">{avatars}</div>
<div class="stat-label">Avatares</div>
</div>
"""

            templates_md = f"""
<div class="stat-card">
<div class="stat-number">{templates}</div>
<div class="stat-label">Templates</div>
</div>
"""

            duration_md = f"""
<div class="stat-card">
<div class="stat-number">{duration}</div>
<div class="stat-label">Tempo Total</div>
</div>
"""

            chars_md = f"""
<div class="stat-card">
<div class="stat-number">{chars}</div>
<div class="stat-label">Processados</div>
</div>
"""

            # Vídeos recentes
            recent = project_manager.get_recent_videos(5)
            if recent:
                recent_md = "### 🎬 Últimos 5 Vídeos\n\n"
                for video in recent:
                    created = datetime.fromisoformat(video['created_at'])
                    recent_md += f"""
**{video.get('project_name', 'Sem projeto')}**
- 📅 {created.strftime('%d/%m/%Y %H:%M')}
- 📁 `{Path(video['path']).name}`
---
"""
            else:
                recent_md = "📭 Nenhum vídeo gerado ainda"

            return videos_md, projects_md, avatars_md, templates_md, duration_md, chars_md, recent_md

        refresh_stats_btn.click(
            fn=update_dashboard,
            outputs=[total_videos, total_projects, total_avatars, total_templates, total_duration, total_chars, recent_videos]
        )
        
        # Retorna componentes e função para carregamento posterior
        return update_dashboard, [total_videos, total_projects, total_avatars, total_templates, total_duration, total_chars, recent_videos]

def create_projects_tab():
    """Cria aba de gerenciamento de projetos"""
    with gr.Tab("📁 Projetos"):
        gr.Markdown("## 📂 Gerenciamento de Projetos")

        with gr.Tab("➕ Novo Projeto"):
            gr.Markdown("### Criar Novo Projeto")

            project_name = gr.Textbox(
                label="📝 Nome do Projeto",
                placeholder="Ex: Vídeos Educacionais, Campanha Marketing, etc.",
                max_lines=1
            )

            project_desc = gr.Textbox(
                label="📋 Descrição",
                placeholder="Descreva o propósito deste projeto...",
                lines=3
            )

            create_project_btn = gr.Button("➕ Criar Projeto", variant="primary", size="lg")
            project_output = gr.Markdown()

            create_project_btn.click(
                fn=create_project_interface,
                inputs=[project_name, project_desc],
                outputs=[project_output]
            )

        with gr.Tab("📋 Meus Projetos"):
            gr.Markdown("### Lista de Projetos")

            refresh_projects_btn = gr.Button("🔄 Atualizar Lista", size="sm")
            projects_list = gr.Markdown()

            refresh_projects_btn.click(
                fn=list_projects_interface,
                outputs=[projects_list]
            )
        
        # Retorna função e componentes para carregamento posterior
        return list_projects_interface, [projects_list]

def create_generator_tab():
    """Cria aba de geração de vídeos"""
    with gr.Tab("🎬 Gerar Vídeo"):
        gr.Markdown("## 🎥 Geração Profissional de Vídeos")

        with gr.Row():
            with gr.Column(scale=2):
                # Seleção de projeto
                projects = project_manager.list_projects()
                project_choices = [(p['name'], p['id']) for p in projects] if projects else [("Nenhum projeto", "none")]

                project_select = gr.Dropdown(
                    label="📁 Selecione o Projeto",
                    choices=project_choices,
                    value=project_choices[0][1] if project_choices else "none",
                    info="Escolha em qual projeto salvar o vídeo"
                )

                # Roteiro
                script_input = gr.Textbox(
                    label="📝 Roteiro do Vídeo",
                    placeholder="Digite ou cole seu roteiro aqui...\n\nO sistema dividirá automaticamente em batches de 3 parágrafos.",
                    lines=12
                )

                # Provedor de áudio
                provider_select = gr.Dropdown(
                    label="🔊 Provedor de Áudio",
                    choices=get_audio_provider_choices(),
                    value=get_audio_provider_choices()[0][1],
                    info="Escolha o serviço de síntese de voz"
                )

                # Voz
                voice_select = gr.Dropdown(
                    label="🎤 Voz do Apresentador",
                    choices=[],
                    value=None,
                    info="As vozes são carregadas automaticamente"
                )

                # Modelo (ElevenLabs)
                model_select = gr.Dropdown(
                    label="🤖 Modelo de Voz (ElevenLabs)",
                    choices=[
                        ("Multilingual v3 🌟", "eleven_multilingual_v3"),
                        ("Turbo v3 ⚡", "eleven_turbo_v3"),
                        ("Flash v3 🚀", "eleven_flash_v3"),
                    ],
                    value="eleven_multilingual_v3",
                    info="Relevante apenas para ElevenLabs"
                )

                # Imagens
                images_input = gr.File(
                    label="🖼️ Imagens do Apresentador (1-20 imagens PNG/JPG)",
                    file_count="multiple",
                    file_types=["image"]
                )

                # Controle de concorrência
                max_workers_slider = gr.Slider(
                    label="⚡ Vídeos Simultâneos no WaveSpeed",
                    minimum=1,
                    maximum=10,
                    value=3,
                    step=1,
                    info="Mais vídeos simultâneos = mais rápido (usa mais créditos)"
                )

                # Botão de geração
                generate_btn = gr.Button("🎬 GERAR VÍDEO", variant="primary", size="lg", elem_classes=["primary-btn"])

            with gr.Column(scale=1):
                gr.Markdown("### 🎯 Status do Processamento")

                # Saída de status
                status_output = gr.Markdown("", elem_classes=["stat-card"])

                # Logs em tempo real
                gr.Markdown("### 📊 Logs do Sistema")
                logs_output = gr.Textbox(
                    label="",
                    lines=15,
                    max_lines=20,
                    show_label=False,
                    elem_classes=["log-terminal"],
                    interactive=False
                )

                # Vídeo final
                video_output = gr.Video(
                    label="🎥 Vídeo Gerado",
                    format="mp4"
                )

        # Event handlers
        provider_select.change(
            fn=update_voices_by_provider,
            inputs=[provider_select],
            outputs=[voice_select]
        )

        generate_btn.click(
            fn=process_video_generation_pro,
            inputs=[project_select, script_input, provider_select, voice_select, model_select, images_input, max_workers_slider],
            outputs=[video_output, status_output, logs_output]
        )

def create_interface():
    """Cria interface principal"""
    with gr.Blocks(
        theme=gr.themes.Default(
            primary_hue="blue",
            secondary_hue="purple",
            neutral_hue="gray",
        ),
        css=CUSTOM_CSS,
        title="LipSync Video Generator Pro"
    ) as app:

        # Tabs principais
        dashboard_fn, dashboard_outputs = create_dashboard_tab()
        projects_fn, projects_outputs = create_projects_tab()
        create_generator_tab()

        # Footer
        gr.Markdown("""
        ---
        <div style="text-align: center; color: #8b93b8; padding: 2rem;">
            <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
                🚀 <strong>LipSync Video Generator Pro</strong> v2.0
            </p>
            <p style="font-size: 0.9rem;">
                Powered by Gemini • ElevenLabs • MiniMax • WaveSpeed
            </p>
        </div>
        """)
        
        # Carrega estatísticas do dashboard e lista de projetos ao iniciar
        app.load(fn=dashboard_fn, outputs=dashboard_outputs)
        app.load(fn=projects_fn, outputs=projects_outputs)

    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
