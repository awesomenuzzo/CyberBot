# Cybersecurity RAG Bot

A full-stack cybersecurity recommendation system powered by Anthropic's Claude and Retrieval-Augmented Generation (RAG).

## Features

- Interactive cybersecurity consultation through natural language
- Follow-up questions to gather context about your specific situation
- Tailored recommendations based on up-to-date cybersecurity knowledge
- Citations to relevant sources from the knowledge base
- Support for custom knowledge documents

## Setup

### Prerequisites

- Python 3.10 or higher
- Poetry package manager 
- Anthropic API key (for Claude)

### Installation with Poetry

1. Install Poetry if you haven't already:

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
source ~/.zshrc
```

2. Install the poetry shell plugin:

```bash
poetry self add poetry-plugin-shell
```

3. Install dependencies:

```bash
poetry install
poetry shell
```

### Environment Setup

Create a `.env` file in the project root with your API keys:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Preparing Your Knowledge Base

The RAG system requires cybersecurity documents to provide up-to-date recommendations. You can:

1. Create a directory with `.txt` files containing cybersecurity information
2. Include information about:
   - Common vulnerabilities and exploits
   - Security best practices
   - Tool documentation
   - Compliance frameworks
   - Recent security advisories

Example directory structure:
```
knowledge_base/
  ├── cve_database.txt
  ├── security_tools/
  │   ├── firewalls.txt
  │   ├── encryption.txt
  │   └── ...
  ├── compliance/
  │   ├── hipaa.txt
  │   ├── pci_dss.txt
  │   └── ...
  └── best_practices/
      ├── network_security.txt
      ├── cloud_security.txt
      └── ...
```

## Usage

Run the bot with:

```bash
python src/main.py
```

The bot will:
1. Ask for your cybersecurity question or concern
2. Ask follow-up questions to understand your specific situation
3. Generate a tailored recommendation with citations to relevant sources

## Example Interaction

```
What cybersecurity issue can I help you with today? How can I secure my small business network?

I need some additional information to provide the best recommendation.

What type of business do you operate and what sensitive data do you handle?
What is your current network setup (number of devices, servers, cloud services)?
Have you experienced any security incidents or have specific threats you're concerned about?
What is your budget range for security improvements?
Do you have any compliance requirements (PCI DSS, HIPAA, etc.)?

[After answering these questions, the bot will provide a detailed recommendation]
```

## Troubleshooting

If you encounter issues with dependencies:

```bash
exit
poetry env list
poetry env remove <your-venv-name>
poetry install
poetry shell
```
