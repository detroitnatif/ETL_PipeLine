import subprocess
import time
import os

def wait_for_postgres(host, max_tries=5, delay_seconds=10):
    retries = 0
    while retries < max_tries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host],
                check=True,
                capture_output=True,
                text=True
            )
            if "accepting connections" in result.stdout:
                print("Successfully Connected")
                return True
        except subprocess.CalledProcessError:
            retries += 1
            print(f'Error connecting, trying {retries} of {max_tries}')
            time.sleep(delay_seconds)
    
    print("Max retries reached")
    return False

if not wait_for_postgres(host='source_postgres'):
    exit(1)

print("Starting ELT")

source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'source_postgres'
}

destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'destination_postgres'  # Corrected typo here
}

# Dump data from source database
dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'  # No password prompt (relies on PGPASSWORD)
]

subprocess_env = os.environ.copy()
subprocess_env["PGPASSWORD"] = source_config['password']

# Run the pg_dump command with the environment variable
subprocess.run(dump_command, env=subprocess_env, check=True)

# Load data into destination database
load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],  # Use -U instead of -u
    '-d', destination_config['dbname'],
    '-a', '-f', 'data_dump.sql',
]

subprocess_env = dict(PGPASSWORD=destination_config['password'])

subprocess.run(load_command, env=subprocess_env, check=True)

print("Ending script")
