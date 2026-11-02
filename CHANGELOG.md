# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-11-02

### Fixed
- Use relative API paths (`window.location.pathname`) for HA Ingress compatibility
- Web UI can now fetch `/api/tools/list` and `/api/chat/completion` through Ingress subpaths

## [0.1.1] - 2026-11-02

### Fixed
- Add `WORKDIR /app` before `CMD` in Dockerfile to ensure correct Python module imports
- Change port from 8099 to 8100 to avoid conflicts with other services
- Resolve syntax errors in `xiaomi_client.py` (type hints and assignments)
- Fix corrupted code in `main.py` (config access)
- Correct tools API format: return `{name, description}` instead of OpenAI schema
- Update Web UI to read `tool.name` instead of `tool.function.name`

## [0.1.0] - 2026-11-02

### Added
- Initial release of Xiaomi Home Assistant Agent
- Supervisor Add-on structure (`repository.yaml`, `config.yaml`, `Dockerfile`)
- FastAPI backend with async support
- Xiaomi MiMo client (OpenAI-compatible API)
- MCP Tool Registry with 11 tools for Home Assistant:
  - Entity control: `ha_get_entity_state`, `ha_list_entities`, `ha_call_service`
  - Configuration: `ha_read_config`, `ha_write_config`, `ha_validate_config`
  - Automation: `ha_get_automations`, `ha_create_automation`
  - System: `ha_restart`, `ha_check_config`
  - History: `ha_get_history`
- Modern Web UI with chat interface
- Tools sidebar with dynamic loading
- Safe config writing with automatic backups
- Documentation (README, QUICKSTART)

---

## Template for Future Releases

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Vulnerability fixes
```
