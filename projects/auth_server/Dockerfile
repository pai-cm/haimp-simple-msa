FROM python:3.11

WORKDIR app/

RUN pip install poetry

COPY scripts/ scripts/
COPY src/__init__.py src/__init__.py
COPY webapp/__init__.py webapp/__init__.py

COPY poetry.lock pyproject.toml README.md ./

RUN poetry config virtualenvs.create false
RUN poetry install

COPY src/ src/
COPY webapp/ webapp/

ENTRYPOINT ["python", "-m", "uvicorn", "webapp.app:create_app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]