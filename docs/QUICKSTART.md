# Quick Start Guide

## 🚀 Instalare Rapidă în Home Assistant

### Pasul 1: Adaugă Repository-ul

1. Deschide Home Assistant
2. Mergi la **Settings → Apps → Install app → ⋮ → Repositories**
3. Adaugă: `https://github.com/Liionboy/xiaomi-ha-agent`

### Pasul 2: Instalează Add-on-ul

1. Găsește **"Xiaomi Home Assistant Agent"** în store
2. Click **Install**
3. Așteaptă finalizarea instalării

### Pasul 3: Configurează

1. Mergi la tab-ul **Configuration**
2. Completează câmpurile:
   - **Xiaomi API Key**: cheia ta API de la Xiaomi
   - **Xiaomi Model**: `mimo-v2.6-pro` (implicit)
   - **Max Tokens**: `4096` (implicit)
   - **Temperature**: `0.7` (implicit)
3. Click **Save**

### Pasul 4: Pornește

1. Click **Start**
2. Click **"Open Web UI"**
3. Începe să conversați cu agentul!

## 🔑 Cum obții Xiaomi API Key

1. Vizitează [https://ai.xiaomi.com](https://ai.xiaomi.com)
2. Autentifică-te cu contul tău Xiaomi
3. Mergi la **API Keys → Create New Key**
4. Copiază cheia și adaug-o în configurația add-on-ului

## 💬 Exemple de Utilizare

### Creează o automatizare
```
Creează o automatizare care aprinde luminile din living la asfințit
```

### Verifică configurația
```
Verifică configuration.yaml pentru eventuale probleme
```

### Controlează dispozitive
```
Stinge toate luminile din casă
```

### Analizează istoricul
```
Arată-mi tendințele de temperatură din ultimele 24 de ore
```

## 🛠️ Dezvoltare Locală

Pentru testare locală (în afara Home Assistant):

```bash
# Clonează repository-ul
git clone https://github.com/Liionboy/xiaomi-ha-agent.git
cd xiaomi-ha-agent

# Construiește Docker image
./scripts/build.sh

# Rulează local
docker run -p 8099:8099 \
  -e XIAOMI_API_KEY=cheia_ta_aici \
  -e XIAOMI_API_BASE=https://api.xiaomi.com/v1 \
  xiaomi-ha-agent:latest

# Accesează Web UI
open http://localhost:8099
```

## 📁 Structura Proiectului

```
xiaomi-ha-agent/
├── addon/
│   ├── config.yaml          # Configurație add-on
│   ├── Dockerfile           # Build Docker
│   └── app/
│       ├── main.py          # Aplicația FastAPI principală
│       ├── core/
│       │   ├── config.py    # Încărcare configurație
│       │   ├── mcp.py       # Registry MCP tools
│       │   ├── tools.py     # Implementare tools HA
│       │   └── xiaomi_client.py  # Client API Xiaomi
│       ├── api/
│       │   ├── chat.py      # Endpoint-uri chat
│       │   ├── config.py    # Management configurație
│       │   └── tools.py     # Endpoint-uri tools
│       └── static/
│           └── index.html   # Web UI
├── scripts/
│   ├── build.sh             # Script build
│   └── run.sh               # Script pornire
└── README.md                # Documentație principală
```

## 🔧 Configurare Avansată

### System Prompt Personalizat

Poți personaliza comportamentul agentului modificând `system_prompt` în configurație:

```yaml
system_prompt: |
  Ești un asistent AI specializat în Home Assistant.
  Ajută utilizatorii să creeze și să gestioneze configurația smart home.
  Validează întotdeauna modificările înainte de a le aplica și explică ce faci.
  Vorbește în română și fii prietenos.
```

### Temperatură Creativitate

- **0.0 - 0.3**: Răspunsuri precise, deterministe (recomandat pentru config)
- **0.4 - 0.7**: Echilibru între precizie și creativitate (implicit)
- **0.8 - 1.0**: Răspunsuri creative, variate

## 🐛 Troubleshooting

### Eroare: "Invalid API Key"
- Verifică că ai introdus corect cheia API
- Asigură-te că cheia nu a expirat
- Verifică accesul la [Xiaomi AI Platform](https://ai.xiaomi.com)

### Eroare: "Connection Timeout"
- Verifică conexiunea la internet
- Verifică că `xiaomi_api_base` este corect
- Încearcă să mărești timeout-ul în configurație

### Tools nu apar în Web UI
- Verifică log-urile add-on-ului
- Asigură-te că toate dependențele sunt instalate
- Restart add-on-ul

## 📞 Suport

- 🐛 [Raportează Probleme](https://github.com/Liionboy/xiaomi-ha-agent/issues)
- 💬 [Discuții](https://github.com/Liionboy/xiaomi-ha-agent/discussions)
- 📖 [Documentație Completă](README.md)

## 📝 Licență

MIT License
