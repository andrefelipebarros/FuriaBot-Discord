![FURIA Logo](https://upload.wikimedia.org/wikipedia/pt/f/f9/Furia_Esports_logo.png?20221021154128)

# 🚀 FURIA Discord Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) 
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/) 
[![Discord](https://img.shields.io/badge/Platform-Discord-7289DA.svg)](https://discord.com/) 

---

## 🌐 Idiomas / Languages

- 🇧🇷 **Português**  
- 🇺🇸 **English**

---

## 🇧🇷 Versão em Português

### 🎮 Descrição

**FURIA Discord Bot** é um bot para servidores Discord de fãs de CS:GO da FURIA, desenvolvido no **Challenge #1: Experiência Conversacional**.  
Ele permite:

- acompanhar partidas ao vivo  
- consultar resultados e estatísticas  
- criar enquetes de torcida  
- navegar por menus de comandos  

### ✨ Funcionalidades

- 🔴 **Live Status**: monitoramento automático de partidas via PandaScore API.  
- ⏭️ **Próxima Partida**: data, horário, adversário e liga.  
- 🏆 **Último Resultado**: evento, placar e desfecho via scraping do Liquipedia.  
- 📊 **Estatísticas**: kills, deaths, assists, ADR, MVP.  
- 📋 **Enquete de Torcida**: vote no jogador que vai brilhar.  
- 🔄 **Toggle Line**: alterne entre lineup masculino e feminino.  
- 🔗 **Redes Sociais**: links oficiais.  
- ❓ **/help**: menu de ajuda interativo.  

### 🏗️ Arquitetura

```mermaid
sequenceDiagram
    participant Usuário
    participant Discord
    participant Bot
    participant Cogs
    participant Services
    participant APIs

    Usuário->>Discord: /live, /next, /stats, botões
    Discord->>Bot: Evento de Interação
    Bot->>Cogs: live_status, matches, stats, poll, socials
    Cogs->>Services: fetch_live, fetch_next, scrape_results, fetch_stats
    Services->>APIs: PandaScore, Liquipedia, BO3.gg
    APIs-->>Services: JSON/HTML
    Services-->>Cogs: Dados processados
    Cogs-->>Bot: embed/response
    Bot-->>Discord: send/edit messages
    Discord-->>Usuário: Exibe respostas
````

> **Serviços externos**:
>
> * 🔹 **PandaScore**: partidas ao vivo e próximas partidas (services `services/pandascore.py`, `services/live_status.py`)
> * 🔹 **Liquipedia**: scraping de resultados e eventos (service `services/result_matcher.py`)
> * 🔹 **BO3.gg**: placares detalhados (service `services/last_scoreboard.py`)

### 🛠️ Tech Stack

* **Linguagem**: Python 3.9+
* **Library**: discord.py
* **HTTP**: httpx (async) & requests
* **Parsing HTML**: BeautifulSoup4
* **Env**: python-dotenv

### 📂 Estrutura do Projeto

```text
src/
├── bot.py               # Entry point
├── config.py            # Configurações e constantes
├── help_menu.py         # Estrutura do /help
├── cogs/                # Comandos organizados por extensão (cogs)
│   ├── live_status.py
│   ├── matches.py
│   ├── poll.py
│   ├── socials.py
│   └── stats.py
├── services/            # Integrações externas
│   ├── pandascore.py
│   ├── live_status.py
│   ├── last_scoreboard.py
│   ├── result_matcher.py
│   └── roster_service.py
├── .env                 # Variáveis de ambiente
└── README.md            # Documentação
```

### ⚙️ Instalação

```bash
git clone https://github.com/seu-usuario/Furia-Bot-Discord-Challenge1.git
cd Furia-Bot-Discord-Challenge1/src
python3 -m venv .venv
# Linux/MacOS
source .venv/bin/activate
# Windows
.\.venv\Scripts\activate
pip install -r ../requirements.txt
cp .env.example .env
# Edite .env com DISCORD_TOKEN e PANDASCORE_TOKEN
```

### ▶️ Uso

```bash
python bot.py
```

**Principais Slash Commands**

| Comando       | Descrição                                |
| ------------- | ---------------------------------------- |
| `/live`       | Inicia monitoramento de partidas ao vivo |
| `/stoplive`   | Encerra monitoramento                    |
| `/nextmatch`  | Exibe informações da próxima partida     |
| `/lastresult` | Exibe o último resultado                 |
| `/stats`      | Estatísticas de jogador ou partida       |
| `/poll`       | Cria enquete de torcida                  |
| `/socials`    | Links das redes sociais oficiais         |
| `/help`       | Exibe menu de ajuda                      |

### 🚀 Roadmap (Futuras Melhorias)

* ⏰ Notificações pré-jogo (10 min antes)
* 🤖 Chatbot com IA para FAQs
* 📅 Agenda semanal com exportação de calendário
* 🌐 Suporte multilíngue (EN, ES, PT)
* 📈 Histórico de interações de fãs

### 🤝 Contribuição

1. Abra uma *issue* para discutir ideias
2. Faça um fork e crie uma branch
3. Envie um Pull Request

### 📄 Licença

Este projeto está licenciado sob a licença MIT.

---

## 🇺🇸 English Version

### 🎮 Description

**FURIA Discord Bot** is a Discord bot for CS:GO FURIA fans as part of **Challenge #1: Conversational Experience**. Users can:

- follow live matches  
- view results & stats  
- create fan polls  
- navigate via slash commands  

### ✨ Features

- 🔴 **Live Status**: automatic updates via PandaScore API.  
- ⏭️ **Next Match**: date, time, opponent, league.  
- 🏆 **Last Result**: event, score via Liquipedia scraping.  
- 📊 **Stats**: kills, deaths, assists, ADR, MVP.  
- 📋 **Fan Poll**: vote for your player.  
- 🔄 **Toggle Line**: switch men’s/women’s roster.  
- 🔗 **Socials**: official links.  
- ❓ **/help**: interactive help menu.  

### 🏗️ Architecture

```mermaid
sequenceDiagram
    participant User
    participant Discord
    participant Bot
    participant Cogs
    participant Services
    participant APIs

    User->>Discord: /live, /nextmatch, /stats, buttons
    Discord->>Bot: Interaction event
    Bot->>Cogs: live_status, matches, stats, poll, socials
    Cogs->>Services: fetch_live, fetch_next, scrape_results, fetch_stats
    Services->>APIs: PandaScore, Liquipedia, BO3.gg
    APIs-->>Services: JSON/HTML
    Services-->>Cogs: processed data
    Cogs-->>Bot: embed/response
    Bot-->>Discord: send/edit messages
    Discord-->>User: displays replies
````

> **External services**:
>
> * 🔹 **PandaScore**: live & next matches (services `services/pandascore.py`, `services/live_status.py`)
> * 🔹 **Liquipedia**: results & event scraping (service `services/result_matcher.py`)
> * 🔹 **BO3.gg**: detailed scoreboards (service `services/last_scoreboard.py`)

### 🛠️ Tech Stack

* **Language**: Python 3.9+
* **Library**: discord.py
* **HTTP**: httpx (async) & requests
* **HTML Parsing**: BeautifulSoup4
* **Env**: python-dotenv

### 📂 Project Structure

```text
src/
├── bot.py
├── config.py
├── help_menu.py
├── cogs/
│   ├── live_status.py
│   ├── matches.py
│   ├── poll.py
│   ├── socials.py
│   └── stats.py
├── services/
│   ├── pandascore.py
│   ├── live_status.py
│   ├── last_scoreboard.py
│   ├── result_matcher.py
│   └── roster_service.py
├── .env
└── README.md
```

### ⚙️ Installation

```bash
git clone https://github.com/your-username/Furia-Bot-Discord-Challenge1.git
cd Furia-Bot-Discord-Challenge1/src
python3 -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.\.venv\Scripts\activate
pip install -r ../requirements.txt
cp .env.example .env
# Set DISCORD_TOKEN and PANDASCORE_TOKEN in .env
```

### ▶️ Usage

```bash
python bot.py
```

**Main Slash Commands**

| Command       | Description                 |
| ------------- | --------------------------- |
| `/live`       | Start live match monitoring |
| `/stoplive`   | Stop live monitoring        |
| `/nextmatch`  | Show next match info        |
| `/lastresult` | Show last match result      |
| `/stats`      | Show player or match stats  |
| `/poll`       | Create a fan poll           |
| `/socials`    | Display social media links  |
| `/help`       | Show help menu              |

### 🚀 Roadmap

* ⏰ Pre‑game notifications (10 min before)
* 🤖 AI‑driven FAQ chatbot
* 📅 Weekly schedule + calendar export
* 🌐 Multilingual (EN, ES, PT)
* 📈 Fan interaction history

### 🤝 Contributing

1. Open an issue
2. Fork & branch
3. Submit a PR

### 📄 License

MIT License. © 2025 FURIA Esports
