import subprocess
import time


def wait_for_postgres(host, max_tries=5, delay_seconds=5):
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
        except subprocess.CalledProcessError as e:
            print("Error connecting")
            retries += 1
            print(f'trying {retries} of {max_tries}')
        
        print("max retries")
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
    'host:': 'destination_db',
}

dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-u', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'

]

subprocess_env = dict(PGPASSWORD=source_config['password'])