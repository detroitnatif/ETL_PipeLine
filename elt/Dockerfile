# Use the correct PostgreSQL base image
FROM postgres:16-alpine

# Install Python and PostgreSQL client
RUN apk add --no-cache \
    python3 \
    py3-pip \
    postgresql-client

# Set python3 as default python
RUN ln -sf python3 /usr/bin/python

# Copy your Python script
COPY elt_script.py .

# Set the entrypoint to run your script
CMD ["python", "elt_script.py"]


