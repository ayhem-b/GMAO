# GMAO — Web-Based Maintenance Management System

A Django **GMAO** (*Gestion de Maintenance Assistée par Ordinateur* — CMMS) for industrial maintenance: work orders, technician interventions, spare-parts stock and a **live machine-status dashboard fed directly by a Siemens S7-1200 PLC** over Snap7. Built as my capstone project at **Lear Corporation Tunisia** for the Licence in Electrical Engineering at ISET Bizerte (June 2025).

## Features

- **Work orders** — created automatically when the PLC reports a fault, or manually; status workflow (default → in progress → done); assignment to a technician
- **Interventions** — technician portal to log received/end time, fault category and a *what / why / where* breakdown, spare parts used
- **Machine monitoring** — each machine's state (running / default) updated live from PLC inputs, with visual indicators
- **Admin dashboard** — Chart.js KPIs: downtime, interventions per machine and per period, breakdown history
- **Spare parts** — part number, stock quantity, consumption per intervention
- **Users** — admin (chef) and technician roles, login, user management
- **SMS alerts** — triggered from the PLC side on machine status changes

## Architecture

```
 Siemens S7-1200 ──(Snap7, read I0.x inputs every 300 ms)──► plc_manager.py ──HTTP POST /update-inputs/──► Django
        ▲                                                           │                                      │
        └────────────(Snap7, write M0.x from the write queue)───────┘                        PostgreSQL ◄──┴──► browser (Bootstrap + Chart.js)
```

`backend/plc_manager.py` runs a background thread that polls the PLC's digital inputs, pushes the snapshot to Django, and drains a queue of memory-bit writes (acknowledge, reset) coming back from the web UI. `plc_manager_instance.py` holds the single shared instance.

## Tech stack

| Layer | Tools |
|---|---|
| Backend | Python, Django 5 |
| Frontend | Django templates, Bootstrap 5, Chart.js |
| Database | PostgreSQL (psycopg2) |
| PLC link | python-snap7 → Siemens S7-1200 |
| Deployment | Local network (LAN) on the plant floor |

## Getting started

```bash
git clone https://github.com/ayhem-b/GMAO.git
cd GMAO
python3 -m venv env && source env/bin/activate      # Windows: env\Scripts\activate
pip install -r requirements.txt
pip install python-snap7 requests                   # only needed for the PLC bridge
```

Configuration is read from environment variables (see `.env.example`): `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`. Create the PostgreSQL database named in `DB_NAME`, then:

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/. To connect a PLC, set its IP in `plc_manager.py` (default `192.168.10.5`) and start the manager from a Django shell or at app start-up via `plc_manager_instance.py`.

## Project layout

```
backend/
├── main/            settings, root urls, update-inputs endpoint
├── maintenance/     Machine, WorkOrder, Intervention, SparePart models, views, templates
├── users/           authentication, roles, admin pages, static assets (css/js/img)
├── plc_manager.py   Snap7 polling + write queue
└── manage.py
requirements.txt
```

## Roadmap

- Token authentication for the `/update-inputs/` endpoint
- Push updates (WebSocket) instead of periodic page refresh
- PDF export of intervention reports
- Docker Compose for one-command deployment

## License

MIT.

---
*Ayhem Belkhamsa — industrial automation engineer, Bizerte, Tunisia · [portfolio](https://ayhem-b.github.io/Ayhem-portfolio/)*
