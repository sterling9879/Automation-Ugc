# 🎬 SaaS de Geração de Vídeos com Lip-Sync

Sistema completo para geração automatizada de vídeos profissionais com sincronização labial (lip-sync) usando inteligência artificial.

## 🌟 Visão Geral

Este sistema transforma roteiros de texto em vídeos completos com apresentadores virtuais usando:

- **🤖 Gemini 2.5 Flash Lite**: Formatação e otimização automática de texto
- **🎙️ ElevenLabs**: Síntese de voz de alta qualidade em múltiplos idiomas
- **🎬 WaveSpeed Wan 2.2**: Geração de vídeo com lip-sync realista
- **🎞️ FFmpeg**: Concatenação e edição de vídeos
- **🖥️ Gradio**: Interface web intuitiva e moderna

## 🎯 Funcionalidades

✅ **Processamento Automático de Texto**
- Divisão inteligente em batches
- Formatação otimizada para narração
- Suporte a textos longos (até 100.000 caracteres)

✅ **Síntese de Voz Natural**
- Mais de 70 idiomas suportados
- Vozes customizáveis e realistas
- Processamento em paralelo para otimização

✅ **Geração de Vídeo com Lip-Sync**
- Sincronização labial precisa
- Múltiplas imagens do apresentador
- Variação automática entre ângulos

✅ **Pipeline Completo**
- Processamento de ponta a ponta
- Sistema de progresso em tempo real
- Tratamento robusto de erros com retry
- Logs detalhados de cada etapa

✅ **Interface Intuitiva**
- Interface web responsiva
- Preview em tempo real
- Estimativa de custo e tempo
- Download fácil do vídeo final

## 📋 Pré-requisitos

### Ferramentas Necessárias

- **Python 3.8+**
- **FFmpeg** (para processamento de vídeo)
- **Git** (para versionamento)

### Chaves de API

Você precisará criar contas e obter chaves de API para:

1. **ElevenLabs** - https://elevenlabs.io
2. **Google Gemini** - https://ai.google.dev
3. **WaveSpeed** - https://wavespeed.ai

## 🚀 Instalação

### 1. Clone o Repositório

```bash
git clone <repository-url>
cd Automation-Ugc
```

### 2. Instale o FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Baixe de https://ffmpeg.org/download.html
- Adicione ao PATH do sistema

### 3. Crie um Ambiente Virtual

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 5. Configure as Variáveis de Ambiente

Copie o arquivo de exemplo e configure suas chaves de API:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas chaves:

```env
ELEVENLABS_API_KEY=sk_your_elevenlabs_key_here
GEMINI_API_KEY=AIzaSy_your_gemini_key_here
WAVESPEED_API_KEY=your_wavespeed_key_here

MAX_CONCURRENT_REQUESTS=10
TEMP_FOLDER=./temp
BATCH_SIZE=3
```

## 🎮 Como Usar

### Iniciar a Aplicação

```bash
python app.py
```

A interface web será aberta em: **http://localhost:7860**

### Passo a Passo

1. **Digite o Roteiro**
   - Cole ou digite seu texto no campo de roteiro
   - O texto será automaticamente dividido em parágrafos

2. **Selecione a Voz**
   - Escolha uma voz disponível do ElevenLabs
   - As vozes suportam mais de 70 idiomas

3. **Upload das Imagens**
   - Faça upload de 1-20 imagens do apresentador
   - Use diferentes ângulos para variedade
   - Formatos aceitos: PNG, JPG, JPEG

4. **Estimativa (Opcional)**
   - Clique em "Estimar Custo e Tempo"
   - Veja previsão de tempo e custos de API

5. **Gerar Vídeo**
   - Clique em "Gerar Vídeo"
   - Acompanhe o progresso em tempo real
   - Faça download do vídeo final quando concluído

## 📁 Estrutura do Projeto

```
Automation-Ugc/
├── app.py                  # Interface Gradio principal
├── config.py               # Configurações do sistema
├── utils.py                # Funções utilitárias
├── text_processor.py       # Processamento com Gemini
├── audio_generator.py      # Geração de áudio (ElevenLabs)
├── video_generator.py      # Geração de vídeo (WaveSpeed)
├── video_concatenator.py   # Concatenação (FFmpeg)
├── job_manager.py          # Gerenciamento de jobs
├── requirements.txt        # Dependências Python
├── .env.example            # Template de configuração
├── .env                    # Configurações (criar manualmente)
└── README.md              # Esta documentação

temp/                       # Arquivos temporários (criado automaticamente)
├── job_{uuid}/
│   ├── formatted_text/
│   │   ├── batch_1.txt
│   │   ├── batch_2.txt
│   │   └── ...
│   ├── audios/
│   │   ├── audio_1.mp3
│   │   ├── audio_2.mp3
│   │   └── ...
│   ├── videos/
│   │   ├── video_1.mp4
│   │   ├── video_2.mp4
│   │   └── ...
│   ├── images/
│   │   └── (cópias das imagens enviadas)
│   ├── final_output.mp4
│   └── state.json          # Estado do job
```

## 🔧 Módulos do Sistema

### `text_processor.py`
- Divide texto em parágrafos
- Agrupa em batches configuráveis
- Envia para Gemini para formatação
- Salva textos formatados

### `audio_generator.py`
- Lista vozes disponíveis do ElevenLabs
- Gera áudios em paralelo
- Suporta múltiplos idiomas e vozes
- Retry automático em caso de falha

### `video_generator.py`
- Upload de arquivos para serviço temporário (0x0.st)
- Submete tarefas para WaveSpeed Wan 2.2
- Polling de resultados com timeout
- Download de vídeos gerados

### `video_concatenator.py`
- Concatena múltiplos vídeos
- Suporte a transições (opcional)
- Usa FFmpeg para processamento
- Otimizado para performance

### `job_manager.py`
- Orquestra todo o pipeline
- Gerencia estado dos jobs
- Sistema de progresso em tempo real
- Tratamento de erros e retry

## ⚙️ Configurações Avançadas

### Ajustar Batch Size

No arquivo `.env`, ajuste o tamanho dos batches:

```env
BATCH_SIZE=3  # Número de parágrafos por batch
```

### Limites de Processamento Paralelo

```env
MAX_CONCURRENT_REQUESTS=10  # Número máximo de requisições simultâneas
```

### Timeouts

```env
POLL_INTERVAL=5    # Intervalo entre polls (segundos)
POLL_TIMEOUT=600   # Timeout total (segundos)
```

### Qualidade de Vídeo

```env
DEFAULT_RESOLUTION=480p  # Opções: 480p, 720p, 1080p
VIDEO_QUALITY=high       # Opções: low, medium, high
```

## 🎨 Personalizar Prompt do Gemini

O prompt usado para formatação de texto está em `text_processor.py`, método `_get_formatting_prompt()`.

Para personalizar:

1. Abra `text_processor.py`
2. Localize o método `_get_formatting_prompt()`
3. Edite o prompt conforme suas necessidades
4. Salve e reinicie a aplicação

**Exemplo de customização:**

```python
def _get_formatting_prompt(self, batch_text: str, batch_number: int) -> str:
    return f"""Você é um roteirista especializado em vídeos para YouTube.

Formate o seguinte texto para ser narrado de forma energética e envolvente:

{batch_text}

Requisitos:
- Tom casual e amigável
- Frases curtas e impactantes
- Use emojis quando apropriado
- Adicione calls-to-action

TEXTO FORMATADO:"""
```

## 💰 Estimativa de Custos

Os custos variam conforme uso das APIs:

| API | Custo Aproximado |
|-----|------------------|
| **Gemini 2.5 Flash Lite** | $0.10 / 1M caracteres entrada |
| **ElevenLabs** | $0.30 / 1K caracteres |
| **WaveSpeed Wan 2.2** | $0.20 / vídeo |

**Exemplo para vídeo de 1000 palavras (~6000 caracteres):**
- Gemini: ~$0.001
- ElevenLabs: ~$1.80
- WaveSpeed (3 vídeos): ~$0.60
- **Total: ~$2.40**

## 🐛 Troubleshooting

### Erro: "FFmpeg não encontrado"

**Solução:** Instale o FFmpeg conforme instruções em "Instalação"

### Erro: "API key inválida"

**Solução:** Verifique se as chaves em `.env` estão corretas e ativas

### Erro: "Rate limit atingido"

**Solução:**
- Aguarde alguns minutos
- Reduza `MAX_CONCURRENT_REQUESTS` em `.env`
- Considere upgrade do tier da API

### Vídeos não estão sendo gerados

**Solução:**
- Verifique conexão com internet
- Confirme que as imagens estão em formato válido (PNG/JPG)
- Verifique logs em `temp/job_{uuid}/state.json`

### Erro ao fazer upload de arquivos

**Solução:**
- O sistema usa 0x0.st para upload temporário
- Se houver problemas, considere implementar upload para S3
- Veja instruções em `video_generator.py`

## 📊 Logs e Monitoramento

Logs são salvos automaticamente e mostrados no console:

```bash
2025-11-16 10:30:00 - JobManager - INFO - Job criado: abc-123-def
2025-11-16 10:30:05 - TextProcessor - INFO - Formatando batch #1...
2025-11-16 10:30:10 - AudioGenerator - INFO - Gerando áudio 1/3...
```

Estado de cada job é salvo em:
```
temp/job_{uuid}/state.json
```

## 🔒 Segurança

⚠️ **IMPORTANTE:**

- Nunca commit o arquivo `.env` no Git
- Mantenha suas API keys em segredo
- Use variáveis de ambiente em produção
- Limite acesso à interface Gradio se expor publicamente

## 🚀 Deploy em Produção

### Opção 1: Docker (Recomendado)

```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
```

```bash
docker build -t lipsync-saas .
docker run -p 7860:7860 --env-file .env lipsync-saas
```

### Opção 2: Servidor Linux

```bash
# Instale dependências
sudo apt-get install python3-pip ffmpeg

# Configure o ambiente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Use PM2 ou systemd para manter rodando
pm2 start app.py --name lipsync-saas
```

## 📈 Performance

**Tempos Médios:**
- Formatação de texto: ~3s por batch
- Geração de áudio: ~5s por áudio
- Geração de vídeo (lip-sync): ~2min por vídeo
- Concatenação: ~10s

**Para vídeo de 3 batches (3 vídeos):**
- Tempo total: ~8-10 minutos
- Pode variar conforme carga das APIs

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é fornecido "como está" para fins educacionais e de desenvolvimento.

## 🙏 Agradecimentos

- **ElevenLabs** - Síntese de voz de alta qualidade
- **Google Gemini** - Processamento de linguagem natural
- **WaveSpeed** - Geração de vídeo com IA
- **Gradio** - Framework de interface web

## 📞 Suporte

Para questões e suporte:
- Abra uma issue no GitHub
- Consulte a documentação das APIs
- Verifique os logs do sistema

---

**Desenvolvido com ❤️ usando Python, IA e muita automação!**
