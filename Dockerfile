FROM python:3.10 AS base

WORKDIR /app

COPY . /app

RUN pip install -r ./requirements/requirements.txt

CMD ["alembic", "upgrade", "head"]


CMD ["python", "app.py"]
