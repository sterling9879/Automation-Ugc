"""
Configurações e validações do sistema
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Configurações centralizadas do sistema"""

    # API Keys
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    WAVESPEED_API_KEY = os.getenv('WAVESPEED_API_KEY')

    # Configurações Gerais
    MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', 10))
    TEMP_FOLDER = Path(os.getenv('TEMP_FOLDER', './temp'))

    # Configurações de Processamento
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 3))
    POLL_INTERVAL = float(os.getenv('POLL_INTERVAL', 10.0))  # 10 segundos entre polls
    POLL_TIMEOUT = float(os.getenv('POLL_TIMEOUT', 900.0))   # 15 minutos timeout total

    # Configurações de Vídeo
    DEFAULT_RESOLUTION = os.getenv('DEFAULT_RESOLUTION', '480p')
    VIDEO_QUALITY = os.getenv('VIDEO_QUALITY', 'high')

    # Formatos suportados
    SUPPORTED_IMAGE_FORMATS = {'.png', '.jpg', '.jpeg'}
    SUPPORTED_AUDIO_FORMATS = {'.wav', '.mp3'}
    SUPPORTED_VIDEO_FORMATS = {'.mp4'}

    # Limites
    MIN_TEXT_LENGTH = 10
    MAX_TEXT_LENGTH = 100000
    MIN_IMAGES = 1
    MAX_IMAGES = 20

    @classmethod
    def validate(cls):
        """Valida se todas as configurações necessárias estão presentes"""
        errors = []

        if not cls.ELEVENLABS_API_KEY:
            errors.append("ELEVENLABS_API_KEY não configurada")

        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY não configurada")

        if not cls.WAVESPEED_API_KEY:
            errors.append("WAVESPEED_API_KEY não configurada")

        if errors:
            raise ValueError(f"Erros de configuração:\n" + "\n".join(f"- {e}" for e in errors))

        # Cria pasta temp se não existir
        cls.TEMP_FOLDER.mkdir(parents=True, exist_ok=True)

        return True

# Valida configurações ao importar
Config.validate()
