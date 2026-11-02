# Changelog

## [0.3.4] - 2026-11-02

### Fixed
- Restore the Supervisor credential with S6 `with-contenv` before starting Python.
- Read the S6 container environment as a fallback; refuse unauthenticated requests instead of sending an empty Bearer.
- Preserve multi-tool assistant messages and reasoning, and send JSON tool results on every round.
- Report the tool-round limit explicitly, without pretending background work continues.
- Prefer Supervisor `/data/options.json`; no personal HA token or protection-mode changes required.

### Security
- Remove full environment logging and ineffective build-time DNS overrides.

### Tests
- Add regression coverage for environment/S6 credentials, missing credentials, proxy paths, service requests, multi-tool chaining and release packaging.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.3] - 2026-11-02

### Fixed
- **Iterative tool-call loop**: AI now executes ALL tool calls until done (max 8 rounds), instead of one-shot
- Properly chains assistant tool_call messages with tool results for API format
- Response only returns when AI finishes its full chain of tool calls


## [0.3.2] - 2026-11-02

### Fixed
- Fix ha_client.py syntax corruption (redactor issue) - rewrote with safe code
- Use SUPERVISOR_TOKEN environment variable for HA API authentication
- Correct HA API URL to http://supervisor/core/api
- Remove duplicate hassio_role in config.yaml


## [0.3.1] - 2026-11-02

### Fixed
- Complete Web UI redesign: compact layout, no more giant bullet spacing
- Fix `response.json()` JavaScript typo that broke chat sending
- Built-in markdown renderer (no CDN dependency - works behind HA Ingress)
- Tools list shows HTTP errors instead of stuck on "Loading tools..."
- Tighter message spacing throughout


## [0.3.0] - 2026-11-02

### Added
- **Real Home Assistant API integration** (ha_client.py) - tools now speak to actual HA
- New tool: `ha_search_entities` - search devices by name (e.g., "Plafoniera", "Birou")
- All tools (list_entities, call_service, get_state, automations, check_config) now use real HA REST API

### Fixed
- Strip function call markup (`<function=...>`) from displayed messages
- Built-in markdown parser as fallback when CDN fails in Ingress
- Further reduced message spacing (margin 0.35rem, padding 0.6rem)


## [0.2.2] - 2026-11-02

### Fixed
- Execute tool calls automatically and get follow-up response from AI
- Reduce message spacing in chat UI
- Tool results are now sent back to AI for natural conversation flow


## [0.2.1] - 2026-11-02

### Fixed
- Parse tool call arguments from JSON string to dict (Xiaomi API returns string, Pydantic expects dict)
- Fix `ValidationError: Input should be a valid dictionary` when AI calls tools


## [0.1.6] - 2026-11-02

### Fixed
- Improve config loading to correctly read Supervisor options from `/data/options.yaml`
- Add detailed logging for config loading and validation
- Ensure custom `xiaomi_api_base` URLs (e.g., `token-plan-ams.xiaomimimo.com`) are used from UI config

## [0.1.5] - 2026-11-02

### Fixed
- Add Google DNS (8.8.8.8, 8.8.4.4) to container `/etc/resolv.conf` to fix DNS resolution failures
- Improve error messages for DNS resolution errors (`Name does not resolve`)

## [0.1.4] - 2026-11-02

### Added
- Detailed logging for chat completion requests (message count, config keys, client status)
- Log API call parameters (model, base URL, tools count)
- User-friendly error messages for common issues (401, 404, timeout, connection)

## [0.1.3] - 2026-11-02

### Added
- CHANGELOG.md file to track all changes
- Template for future releases

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
