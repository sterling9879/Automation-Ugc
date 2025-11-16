"""
Uploader alternativo usando serviços compatíveis com WaveSpeed
"""
import requests
from pathlib import Path
from utils import get_logger
import base64

logger = get_logger(__name__)

class WaveSpeedCompatibleUploader:
    """Upload de arquivos para serviços compatíveis com WaveSpeed"""

    @staticmethod
    def upload_to_fileio(file_path: Path) -> str:
        """
        Faz upload para file.io (compatível com WaveSpeed)
        Retenção: 14 dias
        """
        try:
            logger.info(f"Tentando upload para file.io (compatível WaveSpeed)...")

            with open(file_path, 'rb') as f:
                # file.io com configurações específicas
                response = requests.post(
                    'https://file.io',
                    files={'file': f},
                    data={'expires': '14d'},  # 14 dias
                    timeout=120
                )

            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                url = data['link']
                logger.info(f"✅ Upload file.io concluído: {url}")
                return url
            else:
                raise Exception(f"file.io retornou erro: {data}")

        except Exception as e:
            logger.error(f"❌ file.io falhou: {e}")
            raise

    @staticmethod
    def upload_to_pixeldrain(file_path: Path) -> str:
        """
        Faz upload para pixeldrain.com (CDN profissional, aceito por WaveSpeed)
        Permanente, sem limites razoáveis
        """
        try:
            logger.info(f"Tentando upload para pixeldrain.com...")

            with open(file_path, 'rb') as f:
                response = requests.post(
                    'https://pixeldrain.com/api/file',
                    files={'file': f},
                    timeout=120
                )

            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                file_id = data['id']
                # URL direta para download
                url = f"https://pixeldrain.com/api/file/{file_id}?download"
                logger.info(f"✅ Upload pixeldrain concluído: {url}")
                return url
            else:
                raise Exception(f"pixeldrain retornou erro: {data}")

        except Exception as e:
            logger.error(f"❌ pixeldrain falhou: {e}")
            raise

    @staticmethod
    def upload_to_gofile(file_path: Path) -> str:
        """
        Faz upload para gofile.io (CDN rápido e confiável)
        """
        try:
            logger.info(f"Tentando upload para gofile.io...")

            # Primeiro, pega o melhor servidor
            server_response = requests.get('https://api.gofile.io/getServer', timeout=30)
            server_response.raise_for_status()
            server_data = server_response.json()

            if server_data.get('status') != 'ok':
                raise Exception("Não foi possível obter servidor do gofile")

            server = server_data['data']['server']

            # Upload do arquivo
            with open(file_path, 'rb') as f:
                upload_response = requests.post(
                    f'https://{server}.gofile.io/uploadFile',
                    files={'file': f},
                    timeout=120
                )

            upload_response.raise_for_status()
            upload_data = upload_response.json()

            if upload_data.get('status') != 'ok':
                raise Exception(f"gofile upload falhou: {upload_data}")

            # URL direta do arquivo
            download_page = upload_data['data']['downloadPage']
            # Extrair ID do arquivo da página
            file_id = download_page.split('/')[-1]

            # Gofile tem URLs diretas no formato:
            # Vamos usar a URL de download direta
            url = upload_data['data'].get('downloadPage')

            logger.info(f"✅ Upload gofile concluído: {url}")
            return url

        except Exception as e:
            logger.error(f"❌ gofile falhou: {e}")
            raise

    @staticmethod
    def upload_to_uguu(file_path: Path) -> str:
        """
        Faz upload para uguu.se (serviço estável, 3 dias de retenção)
        """
        try:
            logger.info(f"Tentando upload para uguu.se...")

            with open(file_path, 'rb') as f:
                response = requests.post(
                    'https://uguu.se/upload',
                    files={'files[]': f},
                    timeout=120
                )

            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                url = data['files'][0]['url']
                logger.info(f"✅ Upload uguu.se concluído: {url}")
                return url
            else:
                raise Exception(f"uguu.se retornou erro: {data}")

        except Exception as e:
            logger.error(f"❌ uguu.se falhou: {e}")
            raise

    @staticmethod
    def upload_file_wavespeed_compatible(file_path: Path) -> str:
        """
        Faz upload para serviços compatíveis com WaveSpeed
        Tenta múltiplos serviços em ordem de confiabilidade

        Returns:
            URL pública acessível pela WaveSpeed
        """
        logger.info(f"📤 Upload compatível WaveSpeed: {file_path.name}...")

        # Ordem de preferência (serviços que WaveSpeed provavelmente aceita)
        services = [
            ('pixeldrain.com', WaveSpeedCompatibleUploader.upload_to_pixeldrain),
            ('file.io', WaveSpeedCompatibleUploader.upload_to_fileio),
            ('uguu.se', WaveSpeedCompatibleUploader.upload_to_uguu),
        ]

        errors = []

        for service_name, upload_func in services:
            try:
                logger.info(f"🔄 Tentando {service_name}...")
                url = upload_func(file_path)
                logger.info(f"✅ Upload bem-sucedido via {service_name}")

                # Testa se a URL é acessível
                test_response = requests.head(url, timeout=10, allow_redirects=True)
                if test_response.status_code == 200:
                    logger.info(f"✅ URL verificada e acessível: {url}")
                    return url
                else:
                    logger.warning(f"⚠️  URL retornou status {test_response.status_code}")
                    continue

            except Exception as e:
                error_msg = f"{service_name}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"⚠️  {service_name} falhou, tentando próximo...")
                continue

        # Se todos falharam
        error_details = "\n".join(f"  - {err}" for err in errors)
        raise Exception(
            f"Falha ao fazer upload de {file_path.name} para serviços compatíveis. "
            f"Todos os serviços falharam:\n{error_details}"
        )
