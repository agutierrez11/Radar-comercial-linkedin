The smoothest environment for LazyCodex is Ubuntu or macOS. The harness leans on shell, Git, Node.js/npm, Codex config files, and hooks — all of which behave predictably on Unix-like systems.

### Operating system

| OS | Recommendation | Notes |
| --- | --- | --- |
| **Ubuntu** | Most recommended | Server and dev environments both have predictable paths, shells, and package management. |
| **macOS** | Recommended | Good for local development. Homebrew plus Node.js/npm is all you need. |
| **Windows** | Not recommended | Native Windows shells and path differences cause unnecessary friction with hooks, CLI, file permissions, and script execution. |

If you must use Windows, run Codex and LazyCodex inside **WSL2 Ubuntu** rather than native Windows. Keep the project on the WSL2 filesystem for the most stable experience.

### Before you install

| Item | Expected state |
| --- | --- |
| Codex | Codex App or Codex CLI installed and logged in. |
| Node.js/npm | A maintained Node.js LTS. `npx` ships with npm. |
| Project | A repository opened in Codex that you want to work in. |
| Git | A Git repository so changes can be tracked and reverted. |
| Secrets | Provider keys live in the shell or Codex environment — never pasted into project files. |

You do **not** need to install Bun unless you are building LazyCodex from source. Normal install and usage go through the `npx` path.

Check your versions first:

```bash
node -v
npm -v
npx -v
```

If they are missing, install Node.js:

```bash
# Ubuntu or WSL2 Ubuntu
sudo apt update
sudo apt install -y nodejs npm

# macOS
brew install node
```

### Author recommendations

- **Start with the Codex App.** Install, login, session management, and skill invocation are all visible in the GUI, which is less confusing for first-time users.
- **Use ChatGPT Pro or above.** The docs assume the Codex usage environment that comes with ChatGPT Pro and above.
- **Try bare Codex first.** If you have never used a coding agent before, spend a session with Codex alone before adding LazyCodex on top. Understanding how the base agent responds and edits files makes the harness layer easier to follow.
- **Stick to supported models.** Mixing in GLM, Kimi, Mimo, or other non-default model stacks is not recommended. The docs and skill flows are written around Codex and OmO defaults.
