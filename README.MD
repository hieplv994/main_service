# Main Service

## Getting Started

### Prerequisites

- Python 3.10
- Poetry
- PostgreSQL

### Installation

1. create a virtual environment
```
python -m venv venv
source venv/bin/activate
```
2. install dependencies
```
pip install -r requirements.txt
```
3. docker-compose up
```
docker-compose up
```
4. run locally
```
uvicorn src.main:app --reload
```
5. Execute database in docker
```
docker ps
docker exec -it main_service-db-1 psql -U postgres -d main_service
```
6. Execute database in aws
```
psql -h <host> -p 5432 -U <user> -d <database>
```
