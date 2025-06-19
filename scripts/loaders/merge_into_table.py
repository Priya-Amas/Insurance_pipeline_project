import os
from dotenv import load_dotenv
import snowflake.connector
from scripts.utils.logger import setup_logger

logger = setup_logger("merge_into_table")

# Load credentials from .env
load_dotenv()

account = os.getenv("SNOWFLAKE_ACCOUNT")
user = os.getenv("SNOWFLAKE_USER")
password = os.getenv("SNOWFLAKE_PASSWORD")
role = os.getenv("SNOWFLAKE_ROLE")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
database = os.getenv("SNOWFLAKE_DATABASE")
schema = os.getenv("SNOWFLAKE_SCHEMA")
stage = os.getenv("SNOWFLAKE_STAGE")

def merge_data_from_stage():
    try:
        # ✅ Connect to Snowflake
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

        # ✅ Step 1: Create target table
        try:
            logger.info("📦 Creating `insurance_policies` table...")
            cs.execute("""
                CREATE OR REPLACE TABLE insurance_policies (
                    policy_id        NUMBER,
                    customer_name    STRING,
                    premium_amount   FLOAT,
                    status           STRING,
                    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        except Exception:
            logger.error("❌ Failed to create target table.", exc_info=True)
            raise

        # ✅ Step 2: Load data into temporary table
        try:
            logger.info("📥 Loading JSON into temporary raw staging table...")
            cs.execute("""
                CREATE OR REPLACE TEMP TABLE insurance_raw_stage (
                    v VARIANT
                );
            """)
            cs.execute(f"""
                COPY INTO insurance_raw_stage
                FROM @{stage}
                FILE_FORMAT = (TYPE = 'JSON')
                ON_ERROR = 'CONTINUE';
            """)
        except Exception:
            logger.error("❌ Failed to copy data into staging table.", exc_info=True)
            raise

        # ✅ Step 3: Merge into final table
        try:
            logger.info("🔀 Merging staged data into `insurance_policies` table...")
            cs.execute("""
                MERGE INTO insurance_policies AS target
                USING (
                    SELECT 
                        v:policy_id::NUMBER        AS policy_id,
                        v:customer_name::STRING    AS customer_name,
                        v:premium_amount::FLOAT    AS premium_amount,
                        v:status::STRING           AS status
                    FROM insurance_raw_stage
                ) AS source
                ON target.policy_id = source.policy_id
                WHEN MATCHED THEN UPDATE SET
                    customer_name = source.customer_name,
                    premium_amount = source.premium_amount,
                    status = source.status
                WHEN NOT MATCHED THEN INSERT (
                    policy_id, customer_name, premium_amount, status
                ) VALUES (
                    source.policy_id, source.customer_name, source.premium_amount, source.status
                );
            """)
            logger.info("✅ Merge completed successfully.")
        except Exception:
            logger.error("❌ Failed during merge operation.", exc_info=True)
            raise

        # ✅ Step 4: View results (optional)
        try:
            logger.info("📊 Preview of merged records:")
            cs.execute("SELECT * FROM insurance_policies;")
            for row in cs.fetchall():
                logger.info(row)
        except Exception:
            logger.error("❌ Failed to fetch merged records.", exc_info=True)

    except Exception as e:
        logger.error("🚨 An error occurred during the merge process.", exc_info=True)
        raise e

    finally:
        try:
            cs.close()
            conn.close()
            logger.info("🔒 Snowflake connection closed.")
        except Exception:
            logger.error("❌ Error while closing connection.", exc_info=True)


if __name__ == "__main__":
    merge_data_from_stage()
