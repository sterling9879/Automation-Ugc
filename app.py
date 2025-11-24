"""
Aplicação Gradio - Interface do SaaS de Geração de Vídeos com Lip-Sync
"""
import gradio as gr
from pathlib import Path
from typing import List, Tuple, Optional

from config import Config
from job_manager import JobManager
from audio_generator import AudioGenerator
from utils import get_logger

logger = get_logger(__name__)

# Inicializa gerenciador de jobs
job_manager = JobManager()

# Inicializa gerador de áudio para obter vozes
audio_generator = AudioGenerator()

def get_voice_choices() -> List[str]:
    """Obtém lista de vozes disponíveis do ElevenLabs"""
    try:
        voices = audio_generator.get_available_voices()
        if voices and len(voices) > 0:
            return [voice['name'] for voice in voices]
        else:
            logger.warning("Nenhuma voz disponível do ElevenLabs")
            return ["⚠️ Configure a API Key do ElevenLabs no arquivo .env"]
    except Exception as e:
        logger.error(f"Erro ao obter vozes do ElevenLabs: {e}")
        print(f"\n⚠️  AVISO: Não foi possível conectar ao ElevenLabs")
        print(f"   Verifique se a ELEVENLABS_API_KEY no arquivo .env está correta")
        print(f"   Erro: {e}\n")
        return ["⚠️ Erro ao conectar - Verifique a API Key do ElevenLabs"]

def get_model_choices() -> List[tuple]:
    """Obtém lista de modelos ElevenLabs disponíveis"""
    return [
        ("Multilingual v3 (🌟 Mais recente, melhor qualidade)", "eleven_multilingual_v3"),
        ("Turbo v3 (⚡ Mais rápido, geração em tempo real)", "eleven_turbo_v3"),
        ("Flash v3 (🚀 Ultra rápido, baixa latência)", "eleven_flash_v3"),
        ("Multilingual v2 (Melhor qualidade v2)", "eleven_multilingual_v2"),
        ("Turbo v2.5 (Rápido e eficiente)", "eleven_turbo_v2_5"),
        ("Turbo v2 (Versão anterior rápida)", "eleven_turbo_v2"),
        ("Multilingual v1 (Legado)", "eleven_multilingual_v1"),
        ("Monolingual v1 (Inglês apenas)", "eleven_monolingual_v1"),
    ]

def estimate_job(text: str) -> str:
    """
    Estima custo e tempo do processamento

    Args:
        text: Texto de entrada

    Returns:
        String formatada com estimativas
    """
    try:
        if not text or not text.strip():
            return "⚠️ Digite um texto para ver as estimativas"

        estimate = job_manager.get_job_estimate(text)

        output = f"""
📊 **Estimativa de Processamento**

📝 **Análise do Texto:**
- Caracteres: {estimate['num_chars']:,}
- Batches: {estimate['num_batches']}
- Vídeos a gerar: {estimate['num_videos']}

⏱️ **Tempo Estimado:** {estimate['estimated_time']}

💰 **Custo Estimado:**
- Gemini (formatação): {estimate['estimated_cost']['gemini']}
- ElevenLabs (áudio): {estimate['estimated_cost']['elevenlabs']}
- WaveSpeed (vídeo): {estimate['estimated_cost']['wavespeed']}
- **Total: {estimate['estimated_cost']['total']}**

ℹ️ Os valores são aproximados e podem variar conforme uso real das APIs.
"""
        return output

    except Exception as e:
        logger.error(f"Erro ao estimar job: {e}")
        return f"❌ Erro ao calcular estimativa: {str(e)}"

def process_video_generation(
    text: str,
    voice_name: str,
    model_id: str,
    images: List[gr.File],
    progress=gr.Progress()
) -> Tuple[Optional[str], str, str]:
    """
    Processa geração completa de vídeo

    Args:
        text: Texto de entrada
        voice_name: Nome da voz selecionada
        model_id: Modelo ElevenLabs a usar
        images: Lista de imagens enviadas
        progress: Objeto de progresso do Gradio

    Returns:
        (video_path, status_message, error_message)
    """
    try:
        # Valida inputs
        if not text or not text.strip():
            return None, "", "❌ Por favor, digite o roteiro do vídeo"

        if not images or len(images) == 0:
            return None, "", "❌ Por favor, faça upload de pelo menos uma imagem"

        # Extrai paths das imagens
        image_paths = []
        for img in images:
            if hasattr(img, 'name'):
                image_paths.append(img.name)
            elif isinstance(img, str):
                image_paths.append(img)
            else:
                logger.warning(f"Formato de imagem desconhecido: {type(img)}")

        if not image_paths:
            return None, "", "❌ Não foi possível processar as imagens enviadas"

        logger.info(f"Iniciando processamento com {len(image_paths)} imagens")

        # Cria job
        progress(0, desc="Criando job...")

        job, error = job_manager.create_job(
            input_text=text,
            voice_name=voice_name,
            image_paths=image_paths,
            model_id=model_id
        )

        if error:
            return None, "", f"❌ Erro na validação: {error}"

        # Processa job
        def update_gradio_progress(message: str, percent: int):
            """Callback para atualizar progresso no Gradio"""
            progress(percent / 100, desc=message)

        final_video = job_manager.process_job(
            job=job,
            progress_callback=update_gradio_progress
        )

        # Retorna vídeo gerado
        success_message = f"""
✅ **Vídeo gerado com sucesso!**

📹 Job ID: `{job.job_id}`
📁 Localização: `{final_video}`
⏱️ Processado em: {(job.completed_at - job.created_at).total_seconds():.1f} segundos

🎬 Você pode fazer download do vídeo abaixo.
"""

        logger.info(f"Job {job.job_id} concluído com sucesso")

        return str(final_video), success_message, ""

    except Exception as e:
        error_msg = f"❌ Erro durante processamento: {str(e)}"
        logger.error(error_msg)
        return None, "", error_msg

def create_interface():
    """Cria interface Gradio"""

    # Tema customizado
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo",
    )

    with gr.Blocks(theme=theme, title="Gerador de Vídeos com Lip-Sync") as app:

        gr.Markdown("""
        # 🎬 Gerador de Vídeos com Lip-Sync

        Transforme seu roteiro em vídeos profissionais com sincronização labial automática!

        ### 📋 Como usar:
        1. **Digite ou cole seu roteiro** no campo de texto
        2. **Selecione a voz** do apresentador (ElevenLabs)
        3. **Faça upload das imagens** do apresentador (diferentes ângulos)
        4. **Clique em "Gerar Vídeo"** e aguarde o processamento

        ---
        """)

        with gr.Row():
            with gr.Column(scale=2):

                # INPUT: Texto
                text_input = gr.Textbox(
                    label="📝 Roteiro do Vídeo",
                    placeholder="Digite ou cole o texto completo do seu roteiro aqui...\n\nCada parágrafo será processado separadamente.",
                    lines=15,
                    max_lines=30
                )

                # INPUT: Voz
                voice_dropdown = gr.Dropdown(
                    label="🎤 Selecione a Voz (ElevenLabs)",
                    choices=get_voice_choices(),
                    value=get_voice_choices()[0] if get_voice_choices() else None
                )

                # INPUT: Modelo
                model_dropdown = gr.Dropdown(
                    label="🤖 Selecione o Modelo de Voz (ElevenLabs)",
                    choices=get_model_choices(),
                    value="eleven_multilingual_v3"
                )

                # INPUT: Imagens
                images_input = gr.File(
                    label="🖼️ Imagens do Apresentador (1-20 imagens PNG/JPG)",
                    file_count="multiple",
                    file_types=["image"]
                )

                # Botão de estimativa
                estimate_btn = gr.Button("📊 Estimar Custo e Tempo", variant="secondary", size="sm")

                # Área de estimativa
                estimate_output = gr.Markdown(label="Estimativa")

                # Botão de processar
                process_btn = gr.Button("🎬 Gerar Vídeo", variant="primary", size="lg")

            with gr.Column(scale=1):

                gr.Markdown("### 🎯 Status do Processamento")

                # Mensagem de sucesso
                status_output = gr.Markdown(label="Status")

                # Mensagem de erro
                error_output = gr.Markdown(label="Erro")

                # OUTPUT: Vídeo final
                video_output = gr.Video(
                    label="🎥 Vídeo Final",
                    format="mp4"
                )

        # Informações adicionais
        with gr.Accordion("ℹ️ Informações Técnicas", open=False):
            gr.Markdown(f"""
            ### 🔧 Configurações Atuais

            **APIs Integradas:**
            - 🤖 **Gemini 2.5 Flash Lite**: Formatação e otimização de texto
            - 🎙️ **ElevenLabs**: Síntese de voz de alta qualidade
            - 🎬 **WaveSpeed Wan 2.2**: Geração de vídeo com lip-sync
            - 🎞️ **FFmpeg**: Concatenação de vídeos

            **Limites:**
            - Texto: {Config.MIN_TEXT_LENGTH:,} - {Config.MAX_TEXT_LENGTH:,} caracteres
            - Imagens: {Config.MIN_IMAGES} - {Config.MAX_IMAGES} arquivos
            - Formatos de imagem: PNG, JPG, JPEG
            - Resolução de vídeo: {Config.DEFAULT_RESOLUTION}
            - Batches de texto: {Config.BATCH_SIZE} parágrafos por batch

            **Estrutura de Pastas:**
            - Diretório temporário: `{Config.TEMP_FOLDER}`
            - Cada job cria: `/job_{{uuid}}/{{formatted_text, audios, videos, images}}/`
            - Vídeo final: `final_output.mp4`
            """)

        with gr.Accordion("📚 Exemplo de Roteiro", open=False):
            example_script = """Olá! Bem-vindo ao nosso canal sobre tecnologia e inovação.

Hoje vamos falar sobre inteligência artificial e como ela está transformando o mundo dos negócios.

A IA não é mais ficção científica. Ela está presente em nossas vidas diariamente, desde assistentes virtuais até sistemas de recomendação.

Empresas de todos os tamanhos estão adotando IA para automatizar processos, melhorar a experiência do cliente e tomar decisões mais inteligentes.

Neste vídeo, você vai aprender os conceitos básicos de IA, suas aplicações práticas e como começar a implementar em sua empresa.

Fique conosco até o final para descobrir as tendências que vão dominar o mercado nos próximos anos!

Não se esqueça de se inscrever no canal e ativar o sininho para não perder nenhuma novidade.

Vamos começar!"""

            gr.Textbox(
                value=example_script,
                label="Exemplo de roteiro formatado",
                lines=10,
                interactive=False
            )

        # Conecta eventos
        estimate_btn.click(
            fn=estimate_job,
            inputs=[text_input],
            outputs=[estimate_output]
        )

        process_btn.click(
            fn=process_video_generation,
            inputs=[text_input, voice_dropdown, model_dropdown, images_input],
            outputs=[video_output, status_output, error_output]
        )

        # Footer
        gr.Markdown("""
        ---
        <div style="text-align: center; color: #666;">
            <p>🚀 Desenvolvido com Gradio | Powered by Gemini, ElevenLabs & WaveSpeed</p>
        </div>
        """)

    return app

def main():
    """Função principal"""
    logger.info("Iniciando aplicação Gradio...")

    try:
        # Cria interface
        app = create_interface()

        # Lança aplicação
        logger.info("Abrindo navegador...")
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
            inbrowser=True  # Abre automaticamente no navegador padrão
        )
    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {e}")
        print(f"\n❌ Erro ao iniciar aplicação: {e}")
        print("\nVerifique:")
        print("1. Se todas as API keys estão configuradas corretamente no .env")
        print("2. Se as dependências estão instaladas: pip install -r requirements.txt")
        print("3. Se o FFmpeg está instalado e no PATH")
        raise

if __name__ == "__main__":
    main()
