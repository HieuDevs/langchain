# Langchain Tutorial

This project demonstrates the usage of LangChain with various LLM providers

## Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver
- OpenAI API key
- Google Cloud Firestore credentials
- (Optional) Anthropic API key

## Installation

1. Install uv:

   ```bash
   pip install uv
   ```

2. Create and activate a virtual environment:

   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   # OR
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:

   ```bash
   uv pip install -r requirements.txt
   # OR
   uv pip install .
   ```

## Environment Setup

1. Create a `.env` file in the project root:

   ```
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key  # Optional
   ```

2. Set up Google Cloud Firestore:
   - Create a new project in Google Cloud Console
   - Enable Firestore API
   - Set up authentication credentials
   - Update the PROJECT_ID in main.py

## Using the Application

1. Run the main application:

   ```bash
   uv run -m main
   ```

2. Select a model from the available options:
   - gpt-4o
   - gpt-4o-mini
   - gpt-3.5-turbo
   - o1-preview
   - o1-mini

3. Start chatting with the model. The conversation history will be stored in Firestore.

## Using uv

### Key Commands

- Install packages:

  ```bash
  uv pip install <package-name>
  ```

- Install from requirements.txt:

  ```bash
  uv pip install -r requirements.txt
  ```

- Create virtual environment:

  ```bash
  uv venv
  ```

- Run Python scripts:

  ```bash
  uv run python script.py
  # OR
  uv run -m module_name
  ```
