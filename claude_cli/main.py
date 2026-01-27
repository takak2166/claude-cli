"""Main CLI entry point for Claude CLI."""

import argparse
import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ThinkingBlock,
    ToolUseBlock,
    ToolResultBlock,
    ResultMessage,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError,
)


# All available tools in Claude Code
ALL_TOOLS = [
    "Read",
    "Write",
    "Edit",
    "Bash",
    "Glob",
    "Grep",
    "NotebookEdit",
    "WebFetch",
    "WebSearch",
    "TodoWrite",
    "Task",
    "ExitPlanMode",
    "EnterPlanMode",
    "ListMcpResources",
    "ReadMcpResource",
    "KillShell",
    "TaskOutput",
    "Skill",
]

# Default model
DEFAULT_MODEL = "claude-opus-4-5-20251101"


async def run_query(
    prompt: str,
    cwd: str | None = None,
    verbose: bool = False,
    resume: str | None = None,
) -> None:
    """Run a query with Claude and stream the response."""
    options = ClaudeAgentOptions(
        model=DEFAULT_MODEL,
        allowed_tools=ALL_TOOLS,
        permission_mode="acceptEdits",
        cwd=cwd or str(Path.cwd()),
        resume=resume,
    )

    try:
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text, end="", flush=True)
                    elif isinstance(block, ThinkingBlock) and verbose:
                        print(f"\n[Thinking] {block.thinking}\n", flush=True)
                    elif isinstance(block, ToolUseBlock) and verbose:
                        print(f"\n[Tool: {block.name}] {block.input}\n", flush=True)
                    elif isinstance(block, ToolResultBlock) and verbose:
                        content = block.content
                        if isinstance(content, str):
                            preview = content[:200] + "..." if len(content) > 200 else content
                        else:
                            preview = str(content)[:200]
                        print(f"[Result] {preview}\n", flush=True)
            elif isinstance(message, ResultMessage):
                print()  # Final newline
                # Always output session_id for conversation continuity
                print(f"\n[Session: {message.session_id}]")
                if verbose:
                    print(f"[Turns: {message.num_turns}]")
                    print(f"[Duration: {message.duration_ms}ms]")
                    if message.total_cost_usd:
                        print(f"[Cost: ${message.total_cost_usd:.4f}]")

    except CLINotFoundError:
        print(
            "Error: Claude Code CLI not found. Please install it first.",
            file=sys.stderr,
        )
        sys.exit(1)
    except ProcessError as e:
        print(f"Error: Process failed with exit code {e.exit_code}", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)
    except CLIJSONDecodeError as e:
        print(f"Error: Failed to parse response: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Claude CLI - A command-line tool powered by Claude Agent SDK",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="The prompt to send to Claude",
    )
    parser.add_argument(
        "-c",
        "--cwd",
        type=str,
        default=None,
        help="Working directory for Claude (default: current directory)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show verbose output including tool usage and thinking",
    )
    parser.add_argument(
        "-r",
        "--resume",
        type=str,
        default=None,
        help="Session ID to resume a previous conversation",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    asyncio.run(run_query(args.prompt, args.cwd, args.verbose, args.resume))


if __name__ == "__main__":
    main()
