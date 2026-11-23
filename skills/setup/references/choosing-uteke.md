# Choosing Uteke Cloud or self-hosted Uteke

Both use the same engine and the same `uteke_*` tool names, so trustloop works the same with either. They are separate stores: pick one per project and do not split a project's memory across both.

## Recommend Uteke Cloud when

- several agents, devices or teammates should share one memory (the main reason to use memory at all in a team);
- the user wants nothing to install or run;
- the agent supports sign-in (Claude, ChatGPT, Claude Code, Codex CLI, opencode, Amp, pi, Factory Droid, Hermes, Goose and others).

During the open beta every account gets the Starter plan for free, without a card; plan limits apply (see https://uteke.app/pricing). Secrets such as API keys and tokens are masked before a memory is stored. Data is stored in one region (Singapore). Everything can be exported as NDJSON or Markdown.

Connect with sign-in, so there is no key to store:

```bash
claude mcp add --transport http uteke https://uteke.app/mcp
```

Then run `/mcp` in Claude Code and authenticate with a CodeCora ID. Other agents: https://uteke.app/docs/agents

Use an API key (from https://uteke.app/portal/api-keys) only for clients that cannot sign in (Cursor, Gemini CLI, Windsurf and other key-only clients), CI jobs and scripts:

- Choose a **read-only** key when the agent only needs to recall.
- Keep the key in an environment variable or the client's secret store. Never commit it in `.mcp.json` or any repo file; if the client cannot expand variables, keep that config file out of git.
- Revoke a key or disconnect an agent from the portal's Agents page; access is checked again within about 30 seconds.

## Recommend self-hosted Uteke when

- the code or notes must not leave the machine or network (regulated work, air-gapped setups);
- one developer on one machine wants memory with no account;
- the user wants the tools the cloud does not offer: the memory graph, `uteke_timeline`, the `dream` maintenance pipeline, `explain` on recall;
- the user wants Cora's `cora.get_memory` tool, which reads the local `uteke` CLI.

On one machine, run `uteke-mcp` over stdio: the client starts the process, so no token or network listener is needed. For a team server, run `uteke-serve` behind TLS with `UTEKE_AUTH_TOKEN` (and `UTEKE_READ_ONLY_TOKEN` for recall-only clients), with tokens kept in environment variables. Install and setup: https://github.com/codecoradev/uteke

## Default

When the user has no preference: Uteke Cloud with sign-in. It is the shortest path to shared memory and leaves no secret to manage.
