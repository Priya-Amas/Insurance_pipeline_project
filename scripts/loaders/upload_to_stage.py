import os
import snowflake.connector
from dotenv import load_dotenv
from scripts.utils.logger import setup_logger

logger = setup_logger("upload_to_stage")

load_dotenv()

# Load Snowflake credentials from .env
=======

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
    try:
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
        logger.info("✅ Connected to Snowflake.")

        try:
            for file in os.listdir(json_folder):
                if not file.endswith(".json"):
                    continue

                full_path = os.path.abspath(os.path.join(json_folder, file))
                try:
                    # Check if file already exists in stage
                    cs.execute(f"LIST @{stage}/{file}")
                    existing = cs.fetchall()
                    if existing:
                        logger.info(f"🗑️ File {file} already exists in stage, skipping.")
                        continue
                except snowflake.connector.errors.ProgrammingError as e:
                    if "does not exist" in str(e):
                        logger.info(f"ℹ️ File {file} not found in stage. Proceeding to upload.")
                    else:
                        logger.error(f"❌ Error checking existence of {file}.", exc_info=True)
                        continue

                try:
                    logger.info(f"⏳ Uploading {file} from {full_path} to @{stage}...")
                    cs.execute(f"PUT file://{full_path} @{stage} OVERWRITE=TRUE")
                    logger.info(f"✅ {file} uploaded successfully.")
                except Exception as e:
                    logger.error(f"❌ Upload failed for {file}", exc_info=True)

        finally:
            try:
                logger.info("📂 Listing contents of the stage:")
                cs.execute(f"LIST @{stage}")
                for row in cs.fetchall():
                    logger.info(" - %s", row[0])
            except Exception:
                logger.error("❌ Error listing files in stage.", exc_info=True)
            cs.close()
            conn.close()
            logger.info("🔒 Snowflake connection closed.")

    except Exception:
        logger.error("❌ Could not connect to Snowflake.", exc_info=True)

=======
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