# Claude CLI

A command-line tool powered by Claude Agent SDK.

## Installation

```bash
poetry install
```

## Build Binary

スタンドアロンのバイナリを作成：

```bash
# ビルド
poetry run pyinstaller --onefile --name claude-cli claude_cli/main.py

# 実行
./dist/claude-cli "Your prompt here"
```

バイナリは `dist/claude-cli` に生成されます（約15MB）。

## Usage

```bash
# Basic usage
claude-cli "Your prompt here"

# With working directory
claude-cli "Read the main.py file" -c /path/to/project

# Verbose mode (show tool usage and thinking)
claude-cli "Create a hello world script" -v
```

## Features

- Streaming output
- All Claude Code tools enabled (Read, Write, Edit, Bash, Glob, Grep, etc.)
- Uses claude-opus-4-5-20251101 model

## Authentication

以下のいずれかの方法で認証できます：

1. **Claude Code ログイン（推奨）**
   ```bash
   claude login
   ```
   Claude Max/Proサブスクリプションが必要

2. **環境変数**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   ```

3. **Amazon Bedrock / Google Vertex AI**
   - 各プロバイダーの認証設定に従う
