# Use the correct PostgreSQL base image
FROM postgres:16-alpine

# Install Python, pip, and PostgreSQL client
RUN apk add --no-cache \
    python3 \
    py3-pip \
    postgresql-client

# Ensure that python3 is the default python
RUN ln -sf python3 /usr/bin/python

# Ensure that psql is available in the PATH
RUN ln -sf /usr/bin/psql /usr/local/bin/psql

# Copy your Python script
COPY elt_script.py .

# Set the entrypoint to run your script
CMD ["python", "elt_script.py"]


