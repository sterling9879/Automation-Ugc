"""
Módulo de geração de áudio usando ElevenLabs API
"""
from elevenlabs import ElevenLabs
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import Config
from utils import get_logger, retry_with_backoff

logger = get_logger(__name__)

class AudioGenerator:
    """Gera áudios usando ElevenLabs API"""

    def __init__(self):
        """Inicializa o gerador de áudio"""
        self.client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)
        self.available_voices = None
        logger.info("AudioGenerator inicializado")

    def get_available_voices(self) -> List[Dict[str, str]]:
        """
        Obtém lista de vozes disponíveis na conta ElevenLabs

        Returns:
            Lista de dicts com informações das vozes:
            [
                {'voice_id': 'xxx', 'name': 'Rachel', 'labels': {...}},
                ...
            ]
        """
        try:
            if self.available_voices is None:
                logger.info("Buscando vozes disponíveis...")
                voices = self.client.voices.get_all()

                self.available_voices = [
                    {
                        'voice_id': voice.voice_id,
                        'name': voice.name,
                        'labels': voice.labels if hasattr(voice, 'labels') else {}
                    }
                    for voice in voices.voices
                ]

                logger.info(f"Encontradas {len(self.available_voices)} vozes disponíveis")

            return self.available_voices

        except Exception as e:
            logger.error(f"Erro ao buscar vozes: {e}")
            # Retorna vozes padrão em caso de erro
            return [
                {'voice_id': 'default', 'name': 'Default Voice', 'labels': {}}
            ]

    def get_voice_id_by_name(self, voice_name: str) -> str:
        """
        Obtém voice_id pelo nome da voz

        Args:
            voice_name: Nome da voz

        Returns:
            voice_id correspondente ou primeiro voice_id disponível
        """
        voices = self.get_available_voices()

        for voice in voices:
            if voice['name'].lower() == voice_name.lower():
                return voice['voice_id']

        # Se não encontrar, retorna a primeira voz disponível
        if voices:
            logger.warning(f"Voz '{voice_name}' não encontrada. Usando '{voices[0]['name']}'")
            return voices[0]['voice_id']

        logger.error("Nenhuma voz disponível")
        return 'default'

    @retry_with_backoff(max_retries=3, base_delay=2.0)
    def generate_audio(
        self,
        text: str,
        voice_id: str,
        output_path: Path,
        model_id: str = "eleven_multilingual_v2"
    ) -> Path:
        """
        Gera áudio a partir de texto

        Args:
            text: Texto para sintetizar
            voice_id: ID da voz a usar
            output_path: Caminho para salvar o áudio
            model_id: Modelo ElevenLabs a usar

        Returns:
            Path do arquivo de áudio gerado

        Raises:
            Exception: Se a geração falhar após retries
        """
        try:
            logger.info(f"Gerando áudio para: {output_path.name}")

            # Gera áudio usando a API text_to_speech
            audio_data = self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id=model_id,
                output_format="mp3_44100_128"
            )

            # Salva arquivo
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'wb') as f:
                # audio_data é um iterador de bytes
                for chunk in audio_data:
                    f.write(chunk)

            logger.info(f"Áudio gerado com sucesso: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"Erro ao gerar áudio para {output_path.name}: {e}")
            raise

    def generate_audios_batch(
        self,
        texts: List[Dict],
        voice_id: str,
        output_dir: Path,
        progress_callback=None,
        max_workers: int = None
    ) -> List[Dict]:
        """
        Gera múltiplos áudios em paralelo

        Args:
            texts: Lista de dicts com textos formatados
                   [{'batch_number': 1, 'formatted_text': '...', ...}, ...]
            voice_id: ID da voz a usar
            output_dir: Diretório para salvar áudios
            progress_callback: Função de callback para progresso
            max_workers: Número máximo de workers paralelos (None = auto)

        Returns:
            Lista de dicts com informações dos áudios gerados
            [
                {
                    'audio_number': 1,
                    'text': '...',
                    'audio_path': Path('audio_1.mp3'),
                    'duration': 45.2  # em segundos (se disponível)
                },
                ...
            ]
        """
        logger.info(f"Iniciando geração de {len(texts)} áudios")

        # Cria diretório de áudios
        audio_dir = output_dir / 'audios'
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Determina número de workers
        if max_workers is None:
            max_workers = min(Config.MAX_CONCURRENT_REQUESTS, len(texts))

        results = []

        def generate_single_audio(text_data: Dict) -> Dict:
            """Gera um único áudio"""
            audio_number = text_data['batch_number']
            text = text_data['formatted_text']

            audio_path = audio_dir / f'audio_{audio_number}.mp3'

            if progress_callback:
                progress_callback(f"Gerando áudio {audio_number}/{len(texts)}...")

            generated_path = self.generate_audio(
                text=text,
                voice_id=voice_id,
                output_path=audio_path
            )

            return {
                'audio_number': audio_number,
                'text': text,
                'audio_path': generated_path,
                'duration': None  # Pode ser calculado se necessário
            }

        # Processa em paralelo
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(generate_single_audio, text_data): text_data
                for text_data in texts
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"Áudio {result['audio_number']} concluído")
                except Exception as e:
                    text_data = futures[future]
                    logger.error(f"Erro ao gerar áudio {text_data['batch_number']}: {e}")
                    # Continua mesmo se um áudio falhar
                    results.append({
                        'audio_number': text_data['batch_number'],
                        'text': text_data['formatted_text'],
                        'audio_path': None,
                        'error': str(e)
                    })

        # Ordena resultados por número
        results.sort(key=lambda x: x['audio_number'])

        logger.info(f"Geração de áudios concluída: {len(results)} áudios")

        return results

def test_audio_generator():
    """Função de teste do gerador de áudio"""
    from pathlib import Path
    import tempfile

    generator = AudioGenerator()

    print(f"\n{'='*60}")
    print(f"TESTE DO AUDIO GENERATOR")
    print(f"{'='*60}\n")

    # Lista vozes disponíveis
    print("Vozes disponíveis:")
    voices = generator.get_available_voices()
    for voice in voices[:5]:  # Mostra apenas as 5 primeiras
        print(f"  - {voice['name']} (ID: {voice['voice_id']})")
    print()

    # Testa geração de áudio
    test_texts = [
        {
            'batch_number': 1,
            'formatted_text': 'Olá! Este é um teste de geração de áudio.'
        },
        {
            'batch_number': 2,
            'formatted_text': 'A inteligência artificial está transformando o mundo.'
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        voice_id = generator.get_voice_id_by_name(voices[0]['name'])

        results = generator.generate_audios_batch(
            texts=test_texts,
            voice_id=voice_id,
            output_dir=Path(tmpdir)
        )

        print("Áudios gerados:")
        for result in results:
            if result.get('audio_path'):
                print(f"  - Áudio {result['audio_number']}: {result['audio_path']}")
            else:
                print(f"  - Áudio {result['audio_number']}: ERRO - {result.get('error')}")

if __name__ == "__main__":
    test_audio_generator()
