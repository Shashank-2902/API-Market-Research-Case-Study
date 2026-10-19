# API Market Research: Data Collection and Database Handling

A student project that tracks price, availability and vendor offers for Arduino
UNO components. It collects data from the Nexar API, stores it in SQLite and
visualises it with R. The whole pipeline can run in a Docker container, once or
on a daily schedule.

The project was done for the case study "Intelligent Systems in Production" at
Deggendorf Institute of Technology, supervised by Prof. Tim Weber.

## What it does

1. Searches the Nexar API for the part (`generic_search.py`).
2. Fetches total availability and per-seller prices for each result.
3. Stores parts, availability and prices in SQLite, one snapshot per day
   (`parse_data.py`).
4. Builds HTML tables and PNG plots of prices and availability over time
   (`visualization.R`).

## Project structure

```
main.py                  runs the data collection
generic_search.py        part search against the Nexar GraphQL API
parse_data.py            writes collected data into SQLite
create_sql_table.py      creates the database and its tables
shared_auth.py           Nexar API authentication
visualization.R          tables and plots, written to output/
run_scripts.sh           runs main.py, then visualization.R
Dockerfile               one-off run in a container
Dockerfile _cronjob      same image, scheduled daily at 10:00 with cron
Dbtable.ipynb            notebook for inspecting the database
electronic_parts.db      collected data
```

The database has three tables: `Parts`, `Prices` and `Availabilty`. The last
name keeps its original spelling so that it matches the existing database file.

## Requirements

- Python 3 with `requests`
- R with DBI, RSQLite, gt, dplyr, ggplot2, viridis and gridExtra
- A Nexar API client ID and secret (https://nexar.com)
- Docker, if you want to run it in a container

## Run locally

```bash
pip install -r requirements.txt

export NEXAR_CLIENT_ID=your_client_id
export NEXAR_CLIENT_SECRET=your_client_secret

python create_sql_table.py     # first run only
python main.py
Rscript visualization.R
```

On Windows PowerShell, set the variables with `$env:NEXAR_CLIENT_ID = "..."`.

## Run with Docker

```bash
docker build -t <docker_user>/nexar_api:latest .
docker run -it --rm -e NEXAR_CLIENT_ID=... -e NEXAR_CLIENT_SECRET=... \
  -v "/path/to/output":/app/output <docker_user>/nexar_api:latest
```

The tables and plots are written to the mounted `output` folder. A prebuilt
image is on Docker Hub: https://hub.docker.com/r/shashanksakhala/nexar_api

```bash
docker pull shashanksakhala/nexar_api:latest
```

For a daily run, build from `Dockerfile _cronjob` instead. It starts cron and
runs `run_scripts.sh` every day at 10:00.

## Known gaps

- `main.py` imports `fetch_availability` and `fetch_pricing` from
  `detailed_queries.py`, which is not in this repository. Add that module
  before running the pipeline.
- The plots in `visualization.R` are written for the part with MPN `A000066`.
