# Open Card Table

Open Card Table is an open-source, rules-light card-table simulator for running digital proxy decks in trading card games such as Magic: The Gathering.

The project is designed around manual play rather than automatic rules enforcement. Players decide whether a play is legal and resolve game effects; the application manages card instances, zones, ownership, control, and shared game state.

The long-term goal is to support fully digital play as well as mixed physical/digital play, including private player views, shared battlefield views, deck and catalog integration, persistence, and multiplayer synchronization.

## Current status

Open Card Table has completed its initial foundation milestone (**M0**) and the core card-domain implementation for **M1**.

The current implementation includes:

- A FastAPI backend running locally through Uvicorn.
- A React + TypeScript frontend running locally through Vite.
- A working frontend-to-backend health check.
- A server-authoritative in-memory card/game-state model.
- Shared card definitions and distinct card instances.
- Player-scoped and shared zones.
- Initial card placement and movement between zones.
- Card tap/untap state.
- Ownership and controller identity fields.
- UUID-based card-instance creation.
- Focused unit tests and an M1 acceptance test.

The current backend test suite contains **41 passing tests**.

M1 intentionally remains rules-light and in-memory. Catalog integration, deck import, persistence, WebSockets, multiplayer sessions, authentication, and automatic game-rule enforcement remain deferred to later milestones.

## Architecture

Open Card Table uses a **server-authoritative architecture**. The backend owns the official game state, while clients display that state and request changes.

### Core domain model

The M1 domain model separates descriptive card data from live game state:

- **CardDefinition** — shared descriptive information for a card definition.
- **CardInstance** — one unique in-game card object with its own instance ID, owner, controller, and mutable instance state.
- **Player** — player identity and display information.
- **Zone** — the modeled kind of card zone.
- **ZoneContainer** — owns the ordered collection of card instances in a zone.
- **GameState** — owns players, zone containers, authoritative card location, placement, movement, and state operations.

Card location is not stored independently on `CardInstance`. Instead, **membership in a `ZoneContainer` is the authoritative location**.

The current game-state structure is conceptually:

```text
game_zones
├── "shared"
│   ├── battlefield
│   └── command
├── player-001
│   ├── library
│   ├── hand
│   ├── graveyard
│   └── exile
└── player-002
    ├── library
    ├── hand
    ├── graveyard
    └── exile
```

`GameState` decides where a card belongs. `ZoneContainer` owns the collection mechanics (`add`, `remove`, and membership checks), keeping the game-state layer insulated from the underlying list implementation.

Normal card creation uses UUID-backed instance IDs. A newly created card may exist temporarily outside the game state; once placed, normal `GameState` operations maintain a single authoritative zone membership.

Ownership, control, and location are separate concepts:

- `owner_id` identifies the player who owns the card instance.
- `controller_id` identifies the player currently controlling it.
- zone membership identifies where the card currently is.

M1 does not yet implement gameplay that changes controller or ownership.

### Backend

The backend currently uses:

- Python
- FastAPI
- Pydantic
- Uvicorn
- pytest
- HTTPX / Starlette test client

The backend will continue to own authoritative application and game state. Future milestones are expected to add persistence, catalog access, sessions, multiplayer synchronization, and additional query APIs.

The application intentionally remains rules-light. Players are responsible for determining whether plays are legal and for resolving game effects.

### Frontend

The frontend currently uses:

- React
- TypeScript
- Vite
- ESLint

The current client provides the M0 connectivity view and verifies that the browser can reach the running FastAPI backend.

Future frontend milestones are expected to add:

- player card-table view
- private hand view
- shared battlefield
- card movement controls
- life and status controls
- host controls
- spectator views

### Development communication

During local development:

- React/Vite runs on `http://localhost:5173`
- FastAPI/Uvicorn runs on `http://127.0.0.1:8000`
- Vite proxies requests beginning with `/api` to the FastAPI backend

For example, the frontend requests:

```text
/api/health
```

and Vite forwards that request to:

```text
http://127.0.0.1:8000/api/health
```

## Repository structure

The repository is currently organized approximately as:

```text
open-card-table/
├── .github/
│   └── copilot-instructions.md
├── docs/
│   ├── Open_Card_Table_Project_Plan.docx
│   ├── Open_Card_Table_M0_Day_One_Task_List_Updated.docx
│   └── M1_tasks.docx
├── OpenCardTable.Client/
├── OpenCardTable.Server/
│   ├── app/
│   │   ├── game/
│   │   │   ├── game_state.py
│   │   │   ├── zone.py
│   │   │   └── zone_container.py
│   │   ├── models/
│   │   │   ├── card_definition.py
│   │   │   ├── card_instance.py
│   │   │   └── player.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_card_definition.py
│   │   ├── test_card_instance.py
│   │   ├── test_game_state.py
│   │   ├── test_health.py
│   │   ├── test_m1_acceptance.py
│   │   ├── test_player.py
│   │   └── test_zone_container.py
│   ├── OpenCardTable.Server.pyproj
│   └── run_server.py
├── OpenCardTable.sln
├── requirements.txt
├── Show-Tree.ps1
├── README.md
└── LICENSE
```

## Development setup

### Requirements

The current development environment uses:

- Visual Studio Community 2022
- Python 3.13
- Node.js 22
- npm
- Git

### Python environment

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Running the backend

From the backend project directory:

```powershell
cd .\OpenCardTable.Server
python .\run_server.py
```

The backend runs at:

```text
http://127.0.0.1:8000
```

The current health endpoint is:

```text
http://127.0.0.1:8000/api/health
```

Expected response:

```json
{
  "name": "Open Card Table",
  "status": "ok",
  "version": "0.0.1"
}
```

### Running the frontend

In a separate terminal, from the client project root:

```powershell
npm install
npm run dev
```

The Vite development server normally runs at:

```text
http://localhost:5173
```

With both frontend and backend running, the page should report:

```text
Server: Connected
Application: Open Card Table
Version: 0.0.1
```

If the backend is stopped, the frontend should report:

```text
Server: Disconnected
```

## Running tests

From the repository root:

```powershell
pytest
```

The current suite covers:

- card-definition validation
- card-instance construction and state
- generated instance IDs
- player validation
- zone-container behavior
- game-state creation and zone initialization
- initial card placement
- card movement across player and shared zones
- movement invariants such as object identity, ownership, and total zoned-card count
- tap/untap state
- invalid move/placement cases
- FastAPI health behavior
- the M1 acceptance scenario

At the current M1 checkpoint, the suite contains **41 passing tests**.

## Development workflow

Changes should remain small and scoped to the current milestone.

For each change:

1. Define an observable result.
2. Identify affected files and tests.
3. Implement only the required behavior.
4. Run automated tests.
5. Perform relevant manual verification.
6. Review the change and architecture impact.
7. Commit with a descriptive message.

The project uses milestone task lists as explicit implementation requirements. Tests are added as behavior becomes sufficiently understood, with increasing use of test-first expectations where practical.

## Extensibility and future direction

The architecture is intended to support catalog-neutral card data and rules-light gameplay.

The core card-definition, card-instance, and state model is intended to remain catalog-neutral and rules-light. The current `Zone` enum is deliberately MTG-first (`library`, `hand`, `battlefield`, `graveyard`, `exile`, and `command`) and should be treated as the first game-specific vocabulary layered onto that generic core. Supporting other games may require translating their zone concepts or making the zone vocabulary configurable later.

Future work may include:

- catalog integration such as Scryfall
- deck import and deck-building workflows
- game-state query APIs such as lookup by card instance ID
- persistence with SQLite / SQLAlchemy / Alembic
- WebSocket-based synchronization
- multiplayer sessions
- card-table UI and direct manipulation
- custom cards and non-catalog card definitions
- sandboxed user-defined helpers or scripts for unusual mechanics, calculations, randomization, and visual interactions

These capabilities are intentionally deferred until the underlying domain and transport layers justify them.

## AI-assisted development

Open Card Table is developed with AI-assisted tooling.

GitHub Copilot is used inside Visual Studio for scoped implementation assistance, code completion, explanations, and test scaffolding.

ChatGPT is used for project planning, architecture review, pair-programming support, documentation drafting, code review, language reference, and scope control.

All generated or suggested code is reviewed and accepted by the developer before being incorporated into the project.
