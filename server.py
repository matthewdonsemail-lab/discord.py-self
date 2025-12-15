from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel


class Parameter(BaseModel):
    name: str
    type: str
    required: bool
    description: str


class Operation(BaseModel):
    id: str
    name: str
    category: str
    summary: str
    description: str
    parameters: List[Parameter]
    sources: List[str]


app = FastAPI(
    title="discord.py-self Programmatic Interface",
    description=(
        "Exposes the capabilities described in the documentation as HTTP endpoints "
        "for programmatic discovery and automation."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"

OPERATIONS: Dict[str, Operation] = {}


def add_operation(operation: Operation) -> None:
    OPERATIONS[operation.id] = operation


# Authentication and runtime
add_operation(
    Operation(
        id="authenticate_with_token",
        name="Authenticate with user token",
        category="authentication",
        summary="Document how to retrieve and present a Discord user token for API calls.",
        description=(
            "Tokens are required for every user-scoped action. The documentation explains how to "
            "obtain a token from the Discord client via the developer console or network headers."
        ),
        parameters=[
            Parameter(
                name="acquisition_method",
                type="string",
                required=True,
                description="`console_snippet` for scripted retrieval or `manual_header` for copy/paste from a captured request.",
            ),
            Parameter(
                name="token",
                type="string",
                required=True,
                description="The Discord user token to reuse for subsequent client operations.",
            ),
        ],
        sources=["docs/authenticating.rst L11-L30"],
    )
)

add_operation(
    Operation(
        id="create_client_session",
        name="Create client session",
        category="runtime",
        summary="Create a discord.Client instance to manage the connection lifecycle.",
        description=(
            "Constructs the client that will own all subsequent gateway and REST interactions, with optional "
            "session-aware behaviors driven by user-account features."
        ),
        parameters=[
            Parameter(
                name="intents",
                type="object",
                required=False,
                description="Gateway intent configuration to control received events.",
            ),
            Parameter(
                name="status_tracking",
                type="boolean",
                required=False,
                description="Whether to enable session state tracking for the connected user.",
            ),
        ],
        sources=[
            "docs/quickstart.rst L22-L61",
            "README.rst L35-L38",
        ],
    )
)

add_operation(
    Operation(
        id="register_event_handler",
        name="Register event handler",
        category="runtime",
        summary="Attach lifecycle or dispatch callbacks such as on_ready or on_message.",
        description=(
            "Uses the Client.event decorator to bind coroutine callbacks to gateway events, enabling "
            "message handling and startup routines."
        ),
        parameters=[
            Parameter(
                name="event",
                type="string",
                required=True,
                description="The Discord event name to bind (e.g., `on_ready`, `on_message`).",
            ),
            Parameter(
                name="callback_name",
                type="string",
                required=True,
                description="The coroutine function name registered for the event.",
            ),
        ],
        sources=["docs/quickstart.rst L26-L53"],
    )
)

add_operation(
    Operation(
        id="run_client",
        name="Run client",
        category="runtime",
        summary="Start the client using the provided user token and manage reconnection.",
        description=(
            "Invokes client.run with the user token to establish the connection to Discord and begin "
            "receiving events and dispatching handlers."
        ),
        parameters=[
            Parameter(
                name="token",
                type="string",
                required=True,
                description="User token used for authentication.",
            ),
            Parameter(
                name="reconnect",
                type="boolean",
                required=False,
                description="Whether the client should attempt to reconnect automatically.",
            ),
        ],
        sources=["docs/quickstart.rst L38-L61"],
    )
)

add_operation(
    Operation(
        id="handle_rate_limits",
        name="Handle rate limits",
        category="runtime",
        summary="Rely on the built-in rate limit handling to avoid 429 responses.",
        description=(
            "Documents how the library automatically respects Discord rate limits to keep requests compliant and paced."
        ),
        parameters=[
            Parameter(
                name="policy",
                type="string",
                required=False,
                description="Optional description of custom handling layered on top of the built-in limiter.",
            )
        ],
        sources=["README.rst L30-L33"],
    )
)

add_operation(
    Operation(
        id="self_bot_safety",
        name="Self-bot safety",
        category="runtime",
        summary="Make use of detection-avoidance techniques for user automation.",
        description=(
            "Highlights the library features that reduce the likelihood of user automation detection by Discord."
        ),
        parameters=[
            Parameter(
                name="stealth_mode",
                type="boolean",
                required=False,
                description="Enable or disable optional safety behaviors in client usage patterns.",
            )
        ],
        sources=["README.rst L33-L35"],
    )
)

# Messaging and commands
add_operation(
    Operation(
        id="send_message",
        name="Send message",
        category="messaging",
        summary="Dispatch a message to a target channel, often within on_message handlers.",
        description=(
            "Uses the channel.send coroutine to post text responses after filtering author and content constraints."
        ),
        parameters=[
            Parameter(
                name="channel_id",
                type="string",
                required=True,
                description="Identifier of the channel that should receive the message.",
            ),
            Parameter(
                name="content",
                type="string",
                required=True,
                description="Message body to send.",
            ),
            Parameter(
                name="reply_to",
                type="string",
                required=False,
                description="Optional message ID to reply to when constructing a response.",
            ),
        ],
        sources=["docs/quickstart.rst L30-L59"],
    )
)

add_operation(
    Operation(
        id="command_extension",
        name="Command extension",
        category="messaging",
        summary="Build prefix-based commands with the discord.ext.commands extension.",
        description=(
            "Configures a commands.Bot with self_bot=True to register commands that wrap message handling logic."
        ),
        parameters=[
            Parameter(
                name="command_prefix",
                type="string",
                required=True,
                description="Prefix that triggers command parsing.",
            ),
            Parameter(
                name="commands",
                type="array",
                required=True,
                description="List of command descriptors including name and callback reference.",
            ),
        ],
        sources=["README.rst L130-L143"],
    )
)

# Account data and experiments
add_operation(
    Operation(
        id="manage_sessions",
        name="Manage sessions",
        category="account",
        summary="Inspect or refresh active sessions tied to the user account.",
        description=(
            "Covers the session-aware portions of the user API implemented by the library to keep state synchronized."
        ),
        parameters=[
            Parameter(
                name="session_id",
                type="string",
                required=False,
                description="Specific session identifier to query or refresh.",
            ),
            Parameter(
                name="state",
                type="string",
                required=False,
                description="Desired session state (e.g., active, invalidated).",
            ),
        ],
        sources=["README.rst L35-L38"],
    )
)

add_operation(
    Operation(
        id="update_read_states",
        name="Update read states",
        category="account",
        summary="Sync read-state markers across channels and guilds.",
        description=(
            "Represents the read-state APIs that record the latest message a user has seen per channel or conversation."
        ),
        parameters=[
            Parameter(
                name="channel_id",
                type="string",
                required=True,
                description="Channel whose read state is being updated.",
            ),
            Parameter(
                name="last_message_id",
                type="string",
                required=True,
                description="Identifier of the most recent message acknowledged as read.",
            ),
        ],
        sources=["README.rst L37-L39"],
    )
)

add_operation(
    Operation(
        id="manage_connections",
        name="Manage external connections",
        category="account",
        summary="Link or unlink external account connections.",
        description=(
            "Covers connection endpoints for services such as streaming platforms or gaming networks."
        ),
        parameters=[
            Parameter(
                name="service",
                type="string",
                required=True,
                description="External service identifier (e.g., twitch, steam).",
            ),
            Parameter(
                name="action",
                type="string",
                required=True,
                description="Operation to apply to the connection (connect or disconnect).",
            ),
        ],
        sources=["README.rst L39-L40"],
    )
)

add_operation(
    Operation(
        id="manage_relationships",
        name="Manage relationships",
        category="account",
        summary="Add, block, or remove relationships for the user account.",
        description=(
            "Represents the friend/block relationship APIs that are available for user accounts."
        ),
        parameters=[
            Parameter(
                name="user_id",
                type="string",
                required=True,
                description="User identifier involved in the relationship change.",
            ),
            Parameter(
                name="action",
                type="string",
                required=True,
                description="Relationship action such as add, block, or remove.",
            ),
        ],
        sources=["README.rst L40-L41"],
    )
)

add_operation(
    Operation(
        id="experiment_enrollment",
        name="Experiment enrollment",
        category="account",
        summary="Inspect or set experiment buckets exposed to the client.",
        description=(
            "Covers the ability to work with experiments surfaced to the Discord client for user accounts."
        ),
        parameters=[
            Parameter(
                name="experiment_id",
                type="string",
                required=True,
                description="Identifier of the experiment to query or update.",
            ),
            Parameter(
                name="variant",
                type="string",
                required=False,
                description="Experiment variant or bucket value when overriding enrollment.",
            ),
        ],
        sources=["README.rst L41-L42"],
    )
)

add_operation(
    Operation(
        id="update_user_settings",
        name="Update user settings",
        category="account",
        summary="Modify protobuf-backed user settings.",
        description=(
            "Represents the rich settings payloads supported by the library for user accounts."
        ),
        parameters=[
            Parameter(
                name="setting_key",
                type="string",
                required=True,
                description="Settings key to change (e.g., privacy, appearance).",
            ),
            Parameter(
                name="value",
                type="string",
                required=True,
                description="New value for the specified setting in protobuf-compatible form.",
            ),
        ],
        sources=["README.rst L42-L43"],
    )
)

# Applications, commerce, and interactions
add_operation(
    Operation(
        id="manage_application_team",
        name="Manage application or team",
        category="applications",
        summary="Create or update application and team metadata.",
        description=(
            "Reflects the application/team management APIs that support creating apps and inviting collaborators."
        ),
        parameters=[
            Parameter(
                name="application_id",
                type="string",
                required=False,
                description="Identifier of the application to manage (omit when creating).",
            ),
            Parameter(
                name="action",
                type="string",
                required=True,
                description="Operation such as create, update, or invite_member.",
            ),
        ],
        sources=["README.rst L43-L44"],
    )
)

add_operation(
    Operation(
        id="store_entitlements",
        name="Manage store entitlements",
        category="commerce",
        summary="Grant or revoke SKUs and entitlements.",
        description=(
            "Covers the store and SKU management APIs accessible to user accounts for digital goods."
        ),
        parameters=[
            Parameter(
                name="sku_id",
                type="string",
                required=True,
                description="SKU identifier for the entitlement.",
            ),
            Parameter(
                name="entitlement_action",
                type="string",
                required=True,
                description="grant or revoke entitlement permissions.",
            ),
        ],
        sources=["README.rst L44-L45"],
    )
)

add_operation(
    Operation(
        id="billing_and_boosts",
        name="Billing and boosts",
        category="commerce",
        summary="Work with subscriptions, boosts, promotions, and payments.",
        description=(
            "Represents the billing endpoints for managing Nitro subscriptions, server boosts, or promotional credits."
        ),
        parameters=[
            Parameter(
                name="payment_source",
                type="string",
                required=True,
                description="Payment method identifier or token.",
            ),
            Parameter(
                name="plan",
                type="string",
                required=True,
                description="Subscription or promotion plan name.",
            ),
            Parameter(
                name="quantity",
                type="integer",
                required=False,
                description="Number of boosts or seats to purchase.",
            ),
        ],
        sources=["README.rst L44-L45"],
    )
)

add_operation(
    Operation(
        id="invoke_interaction",
        name="Invoke interaction",
        category="interactions",
        summary="Execute slash commands, component interactions, or buttons.",
        description=(
            "Supports sending interaction payloads that drive Discord's interactive components on user accounts."
        ),
        parameters=[
            Parameter(
                name="interaction_type",
                type="string",
                required=True,
                description="Type of interaction (slash_command, button, select).",
            ),
            Parameter(
                name="payload",
                type="object",
                required=True,
                description="Structured interaction payload to send to Discord.",
            ),
        ],
        sources=["README.rst L45-L46"],
    )
)


@app.get("/", include_in_schema=False)
async def serve_index() -> FileResponse:
    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)
    raise HTTPException(status_code=404, detail="index.html not found")


@app.get("/metadata")
async def metadata() -> dict:
    categories: Dict[str, int] = {}
    for op in OPERATIONS.values():
        categories[op.category] = categories.get(op.category, 0) + 1
    return {
        "name": "discord.py-self Programmatic Interface",
        "description": "HTTP surface that maps documented user-account operations to structured endpoints.",
        "operation_count": len(OPERATIONS),
        "categories": categories,
        "documentation": {
            "technical": "docs/technical_documentation.md",
            "source_docs": [
                "README.rst",
                "docs/quickstart.rst",
                "docs/authenticating.rst",
            ],
        },
    }


@app.get("/operations", response_model=List[Operation])
async def list_operations() -> List[Operation]:
    return list(OPERATIONS.values())


@app.get("/operations/{operation_id}", response_model=Operation)
async def get_operation(operation_id: str) -> Operation:
    operation = OPERATIONS.get(operation_id)
    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")
    return operation


@app.get("/categories")
async def list_categories() -> List[dict]:
    categories: Dict[str, List[Operation]] = {}
    for op in OPERATIONS.values():
        categories.setdefault(op.category, []).append(op)
    return [
        {
            "name": name,
            "operation_count": len(ops),
            "operations": [op.id for op in ops],
        }
        for name, ops in sorted(categories.items())
    ]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=False)
