# Open Card Table

Open Card Table is a card-deck and battlefield simulator for running digital proxy decks in popular trading card games such as Magic: The Gathering.

Its purpose is to support smooth, manual manipulation and use of cards in either a fully digital play environment or alongside a physical opposing deck. The application is intended to provide private hand views and controls, along with a shared battlefield display for zones, cards, and related game state.

The system is also intended to support importing existing cards from descriptive or catalog data and creating custom cards for games or decks that are not covered by an external catalog.

## Extensibility and custom mechanics

The architecture should eventually allow sandboxed user-defined helpers or scripts for unusual card mechanics, calculations, randomization, and visual interactions that are impractical to model as fixed core features.

## Current status

Open Card Table is currently in **M0 / Day One foundation development**.

The current implementation establishes the basic development environment and verifies one end-to-end vertical slice:

- A FastAPI backend runs locally through Uvicorn.
- A React + TypeScript frontend runs locally through Vite.
- The frontend calls the backend health endpoint.
- The UI shows connected and disconnected server states.
- A pytest test verifies the complete health endpoint response.

M0 intentionally stops at this foundation. Card models, deck import, game zones, catalog integration, persistence, WebSockets, multiplayer, and tablet-specific views are deferred to later milestones.

## Architecture

Open Card Table uses a server-authoritative architecture.

### Backend

The backend is implemented with:

- Python
- FastAPI
- Uvicorn
- pytest
- HTTPX

The backend will own authoritative application and game state. As the project grows, it will be responsible for operations such as session management, card state, zones, visibility, persistence, catalog access, and synchronization between clients.

The application is intended to remain rules-light. Players are responsible for determining whether a play is legal and for resolving game effects. The software manages the digital state of cards and the play environment.

### Frontend

The frontend is implemented with:

- React
- TypeScript
- Vite
- ESLint

React provides the browser-based user interface. During development, Vite serves the frontend and rebuilds it automatically as source files change.

Future frontend views are expected to include:

- full player view
- private hand view
- shared battlefield
- life and status controls
- host controls
- spectator views

### Development communication

During development:

- React/Vite runs on `http://localhost:5173`
- FastAPI/Uvicorn runs on `http://127.0.0.1:8000`
- Vite proxies requests beginning with `/api` to the FastAPI backend

For example, the frontend requests:

```text
/api/health

and Vite forwards that request to:

```text
http://127.0.0.1:8000/api/health

### Repository Structure
AS of M0 

open-card-table/
├── .github/
│   └── copilot-instructions.md
├── docs/
│   ├── Open_Card_Table_Project_Plan.docx
│   └── Open_Card_Table_M0_Day_One_Task_List_Updated.docx
├── OpenCardTable.Client/
├── OpenCardTable.Server/
│   ├── app/
│   │   └── main.py
│   ├── tests/
│   │   └── test_health.py
│   ├── OpenCardTable.Server.pyproj
│   └── run_server.py
├── OpenCardTable.sln
├── requirements.txt
├── Show-Tree.ps1
├── README.md
└── LICENSE


### Development Setup
#### Requirements

The current development environment uses:

Visual Studio Community 2022
Python 3.13
Node.js 22
npm
Git

#### Python environment

From the repository root:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

#### Running the backend
cd .\OpenCardTable.Server
python .\run_server.py

The backend runs at:

http://127.0.0.1:8000

The current health endpoint is:

http://127.0.0.1:8000/api/health

Expected response:

{
  "name": "Open Card Table",
  "status": "ok",
  "version": "0.0.1"
}


#### Running the frontend

In a separate terminal:

cd .\OpenCardTable.Client
npm install
npm run dev

The Vite development server normally runs at:

http://localhost:5173

With both frontend and backend running, the page should report:

Server: Connected
Application: Open Card Table
Version: 0.0.1

If the backend is stopped, the frontend should report:

Server: Disconnected

### Running tests

From the backend project directory:

python -m pytest

The current M0 test verifies:

HTTP status 200
application name
health status
application version
Development workflow

Changes should be kept small and scoped to the current milestone.

#Development Workflow 
For each change:

* Define an observable result.
* Identify affected files and tests.
* Implement only the required behavior.
* Run automated tests.
* Perform the relevant manual verification.
* Review the change.
* Commit with a descriptive message.


### AI-assisted development

Open Card Table is developed with AI-assisted tooling.

GitHub Copilot is used inside Visual Studio for scoped implementation assistance, code completion, explanations, and test scaffolding.

ChatGPT is used for project planning, architecture review, pair-programming support, documentation drafting, code review, language reference, and scope control.

All generated or suggested code is reviewed and accepted by the developer before being incorporated into the project.


