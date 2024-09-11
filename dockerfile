# Use the official Apache Airflow image as the base
FROM apache/airflow:2.10.0-python3.12

# Switch to root user to install dnf packages
USER root
RUN dnf -y update \
  && dnf -y install vim tzdata \
  && dnf clean all

# Install Python dependencies (like mysql-connector-python)
RUN pip install --no-cache-dir mysql-connector-python

# Create necessary directories and set permissions
RUN mkdir -p /opt/airflow/logs /opt/airflow/dags /opt/airflow/plugins

# Switch back to the airflow user
USER airflow

# Set the entrypoint for Airflow
ENTRYPOINT ["/bin/bash", "-c"]
