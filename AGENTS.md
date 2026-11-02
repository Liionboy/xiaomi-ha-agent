# Release checks

- Keep `config.yaml`, FastAPI version and CHANGELOG.md synchronized for every release.
- Build the actual Dockerfile, then run `docker run --rm --entrypoint python3 -v "$PWD:/repo:ro" xiaomi-ha-agent:test /repo/tests/test_regressions.py`. Compilation alone is not enough.
- Keep the base image /init entrypoint; start `/scripts/run.sh` with `#!/command/with-contenv bash`. S6 clears the environment otherwise.
- HA proxy uses SUPERVISOR_TOKEN automatically. Do not request personal HA tokens or disable protection mode. Never log environment variables or credentials.
- Supervisor options are `/data/options.json`. Do not infer DNS failures from an invented API default.
- An installed add-on Update rebuilds this source-based image. Preserve options: do not advise uninstall/reinstall routinely.
- One assistant message contains all tool_calls in a round; append it once, preserve reasoning_content, then append one JSON tool result per id.
- Report unverified live behavior explicitly. Never claim a light changed based solely on compilation or a mock test.
