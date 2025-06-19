import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

account = os.getenv("SNOWFLAKE_ACCOUNT")
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
role = os.getenv("SNOWFLAKE_ROLE")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")
stage = os.getenv("SNOWFLAKE_STAGE")
json_folder = "data/json"

def upload_to_internal_stage():
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        role=role,
        warehouse=warehouse,
        database=database,
        schema=schema
    )
    cs = conn.cursor()

    try:
        # Loop through each file in the json folder
        for file in os.listdir(json_folder):
            if file.endswith(".json"):
                full_path = os.path.abspath(os.path.join(json_folder, file))
                with open(full_path, 'rb') as f:
                    contents = f.read()

                print(f"⏳ Uploading {file} to @{stage}...")
                cs.execute(
                    f"PUT file://{full_path} @{stage} OVERWRITE = TRUE"
                )
                print(f"✅ {file} uploaded successfully.")

        # Optional: List the stage contents
        print("\n📂 Files in stage:")
        cs.execute(f"LIST @{stage}")
        for row in cs.fetchall():
            print(" -", row[0])

    finally:
        cs.close()
        conn.close()

if __name__ == "__main__":
    upload_to_internal_stage()


"""import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

account = os.getenv("SNOWFLAKE_ACCOUNT")
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
role = os.getenv("SNOWFLAKE_ROLE")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")
stage = f"@{os.getenv('SNOWFLAKE_STAGE')}"

json_folder = "data/json"

def upload_to_stage():
    for file in os.listdir(json_folder):
        if file.endswith(".json"):
            full_path = os.path.abspath(os.path.join(json_folder, file))
            query = f'PUT file://{full_path} {stage} OVERWRITE=TRUE;'

            command = [
                "snowsql",
                "-a", account,
                "-u", user,
                "-p", password,
                "-r", role,
                "-w", warehouse,
                "-d", database,
                "-s", schema,
                "-q", query
            ]

            print(f"\n⏳ Uploading {file} to {stage}...")
            result = subprocess.run(command, capture_output=True, text=True)

            print("🔍 STDOUT:")
            print(result.stdout)
            print("🐛 STDERR:")
            print(result.stderr)

            if result.returncode != 0:
                print(f"❌ Upload failed for {file}")
            else:
                print(f"✅ Upload succeeded for {file}")

if __name__ == "__main__":
    upload_to_stage()
"""