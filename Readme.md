## Terminal TODO App (Textual TUI)

This project is a small **terminal-based TODO manager** built with the
[`textual`](https://github.com/Textualize/textual) framework and `rich`. It
runs entirely in your terminal and lets you manage a numbered list of tasks
with simple commands.

The original Django/CodeRed CMS README was template text and is no longer
relevant to this project.

### Features

- **In-terminal UI**: Header, footer, input box and TODO panel using Textual.
- **Simple commands** to manage tasks:
  - **Add** a task: `add buy milk` (or just `buy milk`)
  - **Mark done**: `done 2`
  - **Mark not done**: `undone 2`
  - **Delete**: `del 2` (also `delete`, `remove`, `rm`)
- **Visual status**:
  - `[x]` for completed tasks
  - `[ ]` for pending tasks
- **Inline help** in the TODO panel showing available commands and status
  messages.

### Requirements

- Python 3.8+ (recommended)
- `textual`
- `rich`
- `textual-inputs`

You can install the dependencies either with `pipenv` (recommended for this
project) or plain `pip`.

#### Using pipenv

From the project root:

```bash
pipenv install
pipenv run python simpleTUI.py
```

#### Using pip

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install textual rich textual-inputs
python simpleTUI.py
```

### Usage

When the app starts, you will see:

- A **TODOs panel** on the left with the current list of tasks.
- An **input box** where you can type commands.

Type commands into the input box and press **Enter**:

- **Add a task**
  - `add buy milk`
  - or simply: `buy milk`
- **Mark a task as done**
  - `done 1`
- **Mark a task as not done**
  - `undone 1`
- **Delete a task**
  - `del 1`
-- **Quit the app**
  - Press `q`

### Persistence

- Tasks are stored in a simple JSON file named `tasks.json` in the project
  directory.
- When the app starts, it will **load existing tasks** from `tasks.json` (if
  present).
- After any change (add, done, undone, delete), the app will **save the
  updated list** back to `tasks.json`.
- If `tasks.json` does not exist yet, it will be created automatically the
  first time you modify the list.

### Notes

- This project was inspired by:
  - [`pyenv`/`pipenv` workflow article](https://medium.com/@autoferrit/how-to-use-pyenv-pipenv-for-python-virtual-environments-fe70459a4037)
  - [Textual TODO TUI tutorial](https://pythongui.org/how-to-build-a-todo-tui-application-with-textual/)

