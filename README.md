You may need to install the poetry package manager by running the following commands (assuming you are on a mac):

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
source ~/.zshrc
```

If you are on a Windows machine, you can install the poetry package manager by visiting the [official website](https://python-poetry.org/docs/#installing-with-the-official-installer).

You may also need to separately install the poetry shell plugin by running the following command:

```bash
poetry self add poetry-plugin-shell
```

## Setup
To setup the project, you can run the following commands:

```bash
cd backend # navigate to the backend directory
poetry install # install the dependencies
poetry shell # activate the poetry shell. You can deactivate the shell by running `exit`.
```

This will create a virtual poetry environment and install the dependencies listed in the `pyproject.toml` file. 
- to add a new dependency, you can run `poetry add <dependency>`
- to remove a dependency, you can run `poetry remove <dependency>`
- to update a dependency, you can run `poetry update <dependency>`

Occasionally, your poetry shell environment will not properly recognize a dependency, despite it being installed. If this happens, you can try the following commands:

```bash
exit
poetry env list
poetry env remove <your-venv-name> # this will remove the existing venv, for example: poetry env remove lioncal-MP8gxbp4-py3.10
poetry install # this will reinstall the dependencies properly
poetry shell
```
