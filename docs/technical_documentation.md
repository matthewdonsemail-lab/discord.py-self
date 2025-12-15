# Programmatic interface for discord.py-self

This document translates the existing user-facing documentation into a machine-friendly catalog of operations and the HTTP endpoints that expose them. It highlights how the library is authenticated, how a client lifecycle is driven, and which user-account features are implemented.

## System overview

- **Library purpose:** A modern, async-first API wrapper for the Discord user API with wide coverage of user-account specific functionality, including sessions, read states, relationships, experiments, settings, commerce, and interactions.【F:README.rst†L17-L46】
- **Authentication model:** Tokens from the Discord client are required; the library currently expects the user to obtain the token manually via the developer console or captured request headers.【F:docs/authenticating.rst†L11-L30】
- **Core usage pattern:** Create a `discord.Client`, register event callbacks (e.g., `on_ready`, `on_message`), send messages, and run the client with the user token. The command extension can automate message-handling workflows.【F:docs/quickstart.rst†L22-L61】【F:README.rst†L130-L143】

## Operation catalogue

Each operation below corresponds to an actionable capability of the library. The HTTP API in `server.py` mirrors these operations so they can be inspected or called programmatically.

### Authentication and runtime
- **authenticate_with_token:** Document how to retrieve and supply the user token for subsequent calls. Parameters: `acquisition_method` (console snippet vs. manual header extraction), `token` (string).【F:docs/authenticating.rst†L11-L30】
- **create_client_session:** Create a `discord.Client` instance to manage the connection lifecycle. Parameters: `intents` (optional), `status_tracking` (boolean to request session-aware behaviors).【F:docs/quickstart.rst†L22-L61】【F:README.rst†L35-L38】
- **register_event_handler:** Attach callbacks such as `on_ready` and `on_message` for lifecycle and message dispatch. Parameters: `event` (string), `callback_name` (string).【F:docs/quickstart.rst†L26-L53】
- **run_client:** Launch the client with the user token and reconnect semantics appropriate for user accounts. Parameters: `token` (string), `reconnect` (boolean).【F:docs/quickstart.rst†L38-L61】
- **handle_rate_limits:** Emphasize the built-in rate limit handling that avoids 429 responses. Parameters: `policy` (string describing default adaptive policy).【F:README.rst†L30-L33】
- **self_bot_safety:** Leverage detection-avoidance improvements for user automation. Parameters: `stealth_mode` (boolean).【F:README.rst†L33-L35】

### Messaging and commands
- **send_message:** Dispatch a message to a channel, commonly from within `on_message` handlers. Parameters: `channel_id` (string), `content` (string), `reply_to` (optional message ID).【F:docs/quickstart.rst†L30-L59】
- **command_extension:** Use `discord.ext.commands` with `self_bot=True` to register prefix commands. Parameters: `command_prefix` (string), `commands` (list of `{name, callback}`).【F:README.rst†L130-L143】

### Account data and experiments
- **manage_sessions:** Inspect or refresh active sessions for the user account. Parameters: `session_id` (string), `state` (enum).【F:README.rst†L35-L38】
- **update_read_states:** Sync read-state markers across guilds or DMs. Parameters: `channel_id` (string), `last_message_id` (string).【F:README.rst†L37-L39】
- **manage_connections:** Link or unlink external connections (e.g., Twitch, Steam). Parameters: `service` (string), `action` (connect/disconnect).【F:README.rst†L39-L40】
- **manage_relationships:** Create or remove friend/blocked relationships. Parameters: `user_id` (string), `action` (add/block/remove).【F:README.rst†L40-L41】
- **experiment_enrollment:** Query or update experiment buckets exposed to the client. Parameters: `experiment_id` (string), `variant` (string).【F:README.rst†L41-L42】
- **update_user_settings:** Apply protobuf-backed user settings changes. Parameters: `setting_key` (string), `value` (variant).【F:README.rst†L42-L43】

### Applications, commerce, and interactions
- **manage_application_team:** Create or modify application/team resources. Parameters: `application_id` (string), `action` (create/update/invite).【F:README.rst†L43-L44】
- **store_entitlements:** Manage store items, SKUs, or entitlements. Parameters: `sku_id` (string), `entitlement_action` (grant/revoke).【F:README.rst†L44-L45】
- **billing_and_boosts:** Handle billing flows such as subscriptions, boosts, promotions, or payments. Parameters: `payment_source` (string), `plan` (string), `quantity` (integer).【F:README.rst†L44-L45】
- **invoke_interaction:** Execute interactive components like slash commands or buttons. Parameters: `interaction_type` (string), `payload` (object).【F:README.rst†L45-L46】

## HTTP API surface

The accompanying `server.py` exposes this catalogue through JSON endpoints:

- `GET /metadata` — high-level system description, versioning hints, and documentation references.
- `GET /operations` — returns the full list of operations with categories, parameter schemas, and source citations.
- `GET /operations/{operation_id}` — fetch one operation by identifier.
- `GET /categories` — summarize operations grouped by category with counts.
- `GET /openapi.json` — auto-generated OpenAPI document for the service, consumed by `index.html` for an interactive view.

These endpoints are designed for programmatic inspection as well as interactive browsing via the bundled `index.html` interface.

## Deployment notes

Running `python server.py` launches a FastAPI+Uvicorn server bound to port 8080. The provided `railway.json` config uses the same entrypoint, adds a health check on `/metadata`, and is ready for deployment on Railway.
