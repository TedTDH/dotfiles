# opencode

Tracked in this repo (stow-style under `opencode/.config/opencode/`):

- `cli.json` — TUI-only prefs (theme, session, tabs, diffs). Safe to commit.
- `agents/learn.md` — global Learn agent (mode `all`, read-only, shell asks). Symlinked to `~/.config/opencode/agents/learn.md`.

Deliberately NOT tracked:

- `service.json` — contains server password/secret.
- `auth.json` — provider credentials.
- `theme-backgrounds.json` — generated cache.
- `log/` — logs.

Setup on a new machine:

```sh
mkdir -p ~/.config/opencode/agents
ln -sf ~/dotfiles/opencode/.config/opencode/agents/learn.md ~/.config/opencode/agents/learn.md
# optional, if you want cli.json managed from here:
# ln -sf ~/dotfiles/opencode/.config/opencode/cli.json ~/.config/opencode/cli.json
```
