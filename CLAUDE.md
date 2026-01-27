# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Run Commands

```bash
# Install dependencies
poetry install

# Run the CLI directly
poetry run claude-cli "Your prompt"

# Resume a conversation using session ID
poetry run claude-cli -r <session-id> "Follow-up prompt"

# Build standalone binary (~15MB)
poetry run pyinstaller --onefile --name claude-cli claude_cli/main.py
# Binary output: dist/claude-cli
```

## Architecture

This is a minimal CLI wrapper around the `claude-agent-sdk` Python package. The entire application is ~155 lines in a single file.

**Entry point**: `claude_cli/main.py`

- `main()` - CLI argument parsing with argparse
- `run_query()` - Async function that streams responses from the SDK

**Key configuration** (hardcoded in main.py):
- Model: `claude-opus-4-5-20251101`
- Permission mode: `acceptEdits` (auto-accepts file modifications)
- All 18 Claude Code tools enabled
- Conversation resume via `-r`/`--resume` option with session ID

**SDK types used**:
- `ClaudeAgentOptions` - Configuration for queries
- `AssistantMessage` with blocks: `TextBlock`, `ThinkingBlock`, `ToolUseBlock`, `ToolResultBlock`
- `ResultMessage` - Final session metadata (turns, duration, cost)
- Exceptions: `CLINotFoundError`, `ProcessError`, `CLIJSONDecodeError`

## Authentication

Requires one of:
1. `claude login` (Claude Max/Pro subscription)
2. `ANTHROPIC_API_KEY` environment variable
3. Amazon Bedrock or Google Vertex AI credentials
