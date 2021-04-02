# Web Traffic ETL

The web traffic ETL extracts web traffic data from When I Work CSVs, pivots the page time spent data by user and web page path, and loads it into a CSV

## Getting Started

- To set your local environment up, execute `make`
- To run the ETL locally, execute `make run`
- To run the ETL's automated unit tests, execute `make test`

## Environment Variables

This application allows for environment configurations to be set via environment variables

| Name                      | Example                                                 |
| ------------------------- | ------------------------------------------------------- |
| WEB_TRAFFIC_DATA_ROOT_URL | "https://public.wiwdata.com/engineering-challenge/data" |
