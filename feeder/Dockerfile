FROM python:3.12-slim-bookworm

ARG AIRFLOW_VERSION=3.1.1
ARG PYTHON_VERSION=3.12

# Disable example DAGs and default connections
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=False
ENV AIRFLOW__CORE__LOAD_EXAMPLES_FROM_PROVIDERS=False

ENV AIRFLOW_HOME=/opt/airflow
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

WORKDIR /opt/airflow
COPY . .

RUN pip install "apache-airflow[celery]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}" && \
    pip install "structlog==25.4.0" && \
    pip install -r dags_requirements.txt && \
    playwright install-deps

EXPOSE 8080

CMD ["airflow", "standalone"]