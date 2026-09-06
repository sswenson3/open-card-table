# Open Card Table — Copilot Instructions

## Project purpose
Open Card Table is an open-source, manual card-game simulator.

The first supported game is Magic: The Gathering, but the core game engine should remain catalog-neutral and rules-light.

Players are responsible for legal play and effect resolution. The software manages card identity, zones, visibility, ownership, control, state, and synchronization.

## Current architecture
- Backend: Python + FastAPI
- Development server: Uvicorn
- Frontend: React + TypeScript
- Frontend tooling: Vite
- Testing: pytest for backend, Vitest/Testing Library later for frontend
- Persistence later: SQLite with SQLAlchemy/Alembic
- Catalog integration later: Scryfall via HTTPX
- Real-time synchronization later: WebSockets

The Python server is authoritative for game state.

## Current milestone
The project is currently in M0 / Day One foundation work.

Keep changes narrowly scoped to the current task.

Do not introduce future functionality unless explicitly requested.

## M0 scope exclusions
Do not implement:
- Scryfall integration
- card definitions or card instances
- deck parsing/import
- game zones or shuffle/draw logic
- persistence/database code
- WebSockets
- multiplayer
- tablet/private-hand views
- authentication
- session persistence
- drag-and-drop card interfaces
- production packaging

## Coding practices
### Python
- Target Python 3.13.
- Use type annotations for public functions and meaningful internal APIs.
- Prefer small, explicit functions.
- Follow standard Python naming conventions.
- Avoid unnecessary abstractions.
- Keep FastAPI route handlers thin as application complexity grows.
- Add or update pytest tests for behavior changes.

### TypeScript / React
- Use TypeScript rather than plain JavaScript.
- Prefer explicit types for API contracts and important state.
- Use functional React components.
- Keep components small and focused.
- Avoid unnecessary state and dependencies.
- Do not add UI frameworks unless explicitly approved.

## API practices
- HTTP API routes live under `/api`.
- The server owns authoritative application state.
- Clients request actions; they do not become the source of truth.
- Return predictable structured responses.
- Validate behavior with automated tests.

## Testing expectations
- Test observable behavior, not implementation details.
- Verify complete API response contracts when appropriate.
- Protect invariants such as card identity, zone membership, visibility, and state recovery when those features are introduced.
- Do not hide or ignore failing tests.

## Repository hygiene
Do not commit:
- `.venv`
- `node_modules`
- `.vs`
- Python caches
- test caches
- credentials or secrets
- downloaded card-image caches
- bulk catalog data

## Implementation behavior
Before making a change:
1. Identify the smallest change that satisfies the requested behavior.
2. Preserve the current architecture.
3. Avoid speculative abstractions.
4. Include tests when behavior changes.
5. Do not silently expand scope.

If a request conflicts with these project instructions, point out the conflict rather than implementing around it.