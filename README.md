# 🎙️ Discord Audio Recorder Bot

Um bot para Discord desenvolvido em Python capaz de entrar em canais de voz (Palcos) e gravar o áudio dos usuários, salvando os arquivos localmente.

## 🚀 O Projeto
Este projeto foi criado para explorar a integração com a API do Discord, manipulação de streams de áudio em tempo real e estruturação de bots usando o padrão **Command** (através de Cogs). 

### 💡 Desafio Técnico Superado
Durante o desenvolvimento, o Discord implementou globalmente o protocolo DAVE (End-to-End Encryption - E2EE) para chamadas de voz, o que invalidou temporariamente a decodificação de áudio em bibliotecas padrão, gerando o bloqueio de WebSocket `4017`. 
A solução de contorno arquitetada foi migrar o tráfego do bot para **Canais de Palco (Stage Channels)**, onde a criptografia estrita não bloqueia a captação de pacotes Opus, permitindo que a gravação continue funcionando perfeitamente enquanto a comunidade open-source atualiza as bibliotecas base.

## 🛠️ Tecnologias Utilizadas
* **Python 3**
* **Pycord** (Fork do discord.py com suporte a Voice Sinks)
* **PyNaCl** (Para criptografia e rede de voz)
* **python-dotenv** (Para gerenciamento seguro de variáveis de ambiente)

## ⚙️ Funcionalidades
* `/record`: Conecta o bot ao canal de Palco atual e inicia a captação de áudio.
* `/stop_recording`: Encerra a gravação, processa o buffer de áudio e envia os arquivos `.wav` gerados diretamente no chat.
* **Isolamento de Escopo:** Comandos estruturados usando o design pattern Command (Cogs) para facilitar a manutenção e escalabilidade.

## 💻 Como rodar localmente

1. Clone este repositório:
```bash
git clone https://github.com/Man0ela/Gravar_audio_discord.git
```

2. Instale as dependências necessárias:
```bash
python -m pip install "py-cord[voice]" PyNaCl python-dotenv
```

3. Crie um arquivo .env na raiz do projeto e adicione o token do seu bot:
```text
DISCORD_TOKEN=seu_token_aqui
```

4. Execute o bot:
```bash
python main.py
```
