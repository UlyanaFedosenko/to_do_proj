FROM python:3.10 AS base

COPY requirements ./requirements

RUN pip install -r ./requirements/requirements.txt

COPY db ./db
FROM base AS migration
COPY alembic ./alembic
COPY alembic.ini ./

CMD ["alembic", "upgrade", "head"]

FROM base AS server
COPY app.py ./

CMD ["python", "app.py"]
