# Xiaomi Home Assistant Agent

🤖 **AI-powered configuration assistant for Home Assistant, powered by Xiaomi MiMo**

Transform your Home Assistant configuration with natural language, powered by Xiaomi's MiMo AI models.

## ✨ Features

- 🧠 **AI-Powered Editing** — Modify your HA configuration using natural language
- 🛠️ **MCP Tools** — Deep integration with HA entities, services, automations, and configuration
- 🔧 **Smart Validation** — Automatic config validation before applying changes
- 💬 **Chat Interface** — Clean, modern web UI for interacting with the agent
- 🔐 **Safe Config Writing** — Automatic backups and rollback support
- 🏠 **Home Context** — Agent understands your specific setup
- ⚡ **Fast & Efficient** — Powered by Xiaomi MiMo models

## 🚀 Installation

### Via Supervisor (Recommended)

1. **Add Repository**
   - Go to Settings → Apps → Install app → ⋮ → Repositories
   - Add: `https://github.com/Liionboy/xiaomi-ha-agent`

2. **Install Add-on**
   - Find "Xiaomi Home Assistant Agent" in the store
   - Click Install

3. **Configure**
   - Go to Configuration tab
   - Add your Xiaomi API key
   - Configure model and parameters
   - Click Save

4. **Start**
   - Click Start
   - Click "Open Web UI" to access the interface

### Manual Installation

For development or testing:

```bash
# Clone repository
git clone https://github.com/Liionboy/xiaomi-ha-agent.git
cd xiaomi-ha-agent

# Copy to HA add-ons directory
cp -r addon/ /path/to/ha/addons/xiaomi_ha_agent/

# Install via Supervisor UI
```

## ⚙️ Configuration

| Option | Description | Default |
|--------|-------------|---------|
| `xiaomi_api_key` | Your Xiaomi API key | — |
| `xiaomi_api_base` | API base URL | `https://api.xiaomi.com/v1` |
| `xiaomi_model` | Model to use | `mimo-v2.6-pro` |
| `max_tokens` | Maximum response tokens | `4096` |
| `temperature` | Response creativity (0-1) | `0.7` |
| `system_prompt` | Custom system prompt | See below |

### Getting Your Xiaomi API Key

1. Visit [Xiaomi AI Platform](https://ai.xiaomi.com)
2. Sign in with your Xiaomi account
3. Go to API Keys → Create New Key
4. Copy the key and add it to the add-on configuration

## 🛠️ Available Tools

The agent has access to the following MCP tools:

### Entity Control
- `ha_get_entity_state` — Get current entity state
- `ha_list_entities` — List all entities
- `ha_call_service` — Call HA services (turn_on, turn_off, etc.)

### Configuration
- `ha_read_config` — Read configuration files
- `ha_write_config` — Write config with automatic backup
- `ha_validate_config` — Validate HA configuration

### Automation
- `ha_get_automations` — List all automations
- `ha_create_automation` — Create new automations

### System
- `ha_restart` — Restart Home Assistant
- `ha_check_config` — Check configuration for errors
- `ha_get_history` — Get entity state history

## 💬 Usage Examples

### Create an Automation
```
Create an automation that turns on the living room lights at sunset
```

### Debug an Issue
```
Why isn't my bedroom motion sensor triggering automations?
```

### Review Configuration
```
Check my configuration.yaml for any issues
```

### Control Devices
```
Turn off all the lights in the house
```

### Analyze History
```
Show me the temperature trends for the past 24 hours
```

## 🔒 Security

- **Path Traversal Protection** — Cannot access files outside config directory
- **Automatic Backups** — Every config change is backed up
- **Validation** — Changes are validated before applying
- **HTTPS Support** — Secure connection with optional certificate verification

## 📁 Project Structure

```
xiaomi-ha-agent/
├── addon/
│   ├── config.yaml          # Add-on configuration
│   ├── Dockerfile           # Docker build
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── core/
│   │   │   ├── config.py    # Configuration loading
│   │   │   ├── mcp.py       # MCP tool registry
│   │   │   ├── tools.py     # HA tools implementation
│   │   │   └── xiaomi_client.py  # Xiaomi API client
│   │   ├── api/
│   │   │   ├── chat.py      # Chat endpoints
│   │   │   ├── config.py    # Config management
│   │   │   └── tools.py     # Tools endpoints
│   │   └── static/
│   │       └── index.html   # Web UI
│   └── scripts/
│       └── run.sh           # Startup script
├── docs/                    # Documentation
└── README.md               # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Credits

- Built by [Liionboy](https://github.com/Liionboy)
- Powered by [Xiaomi MiMo](https://ai.xiaomi.com)
- Inspired by [OpenCode for Home Assistant](https://github.com/magnusoverli/opencode)

## 📞 Support

- 🐛 [Report Issues](https://github.com/Liionboy/xiaomi-ha-agent/issues)
- 💬 [Discussions](https://github.com/Liionboy/xiaomi-ha-agent/discussions)
- 📖 [Documentation](docs/)
