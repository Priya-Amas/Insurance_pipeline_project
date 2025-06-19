import os
import snowflake.connector
from dotenv import load_dotenv
from scripts.utils.logger import setup_logger

logger = setup_logger("upload_to_stage")


# Load Snowflake credentials from .env

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
        raise

if __name__ == "__main__": 
    upload_to_internal_stage()
    logger.info("Script executed successfully.")
else:
    logger.info("Script imported as a module, not executed directly.")
    # This allows the script to be used in Airflow without executing the main function.
    # In Airflow, the function will be called by the PythonOperator.    
    # If you want to run this script directly, uncomment the line below:
    # upload_to_internal_stage()    

