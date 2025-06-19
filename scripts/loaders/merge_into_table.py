import os
from dotenv import load_dotenv
import snowflake.connector

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
        # ✅ Step 1: Create target table
        print("📦 Creating insurance_policies table...")
        cs.execute("""
            CREATE OR REPLACE TABLE insurance_policies (
                policy_id        NUMBER,
                customer_name    STRING,
                premium_amount   FLOAT,
                status           STRING,
                created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # ✅ Step 2: Load into temporary staging table
        print("📥 Loading JSON into temporary raw table...")
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

        # ✅ Step 3: Merge into final table
        print("🔀 Deduplicating and merging into insurance_policies...")
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
        print("✅ Merge completed.")

        # ✅ Optional: View results
        cs.execute("SELECT * FROM insurance_policies;")
        print("\n📊 Loaded Policies:")
        for row in cs.fetchall():
            print(row)

    finally:
        cs.close()
        conn.close()

if __name__ == "__main__":
    merge_data_from_stage()
#     subprocess.run(["snowsql", "-q", query, "-o", "output_format=csv"])
#             if result.returncode == 0:
#                 print(f"✅ {file} uploaded successfully.")
#             else:
#                 print(f"❌ Failed to upload {file}: {result.stderr}") 