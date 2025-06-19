import pytest
from unittest import mock
from scripts.loaders import merge_into_table


@mock.patch("scripts.loaders.merge_into_table.snowflake.connector.connect")
def test_merge_data_from_stage(mock_connect):
    # Mock Snowflake connection and cursor
    mock_conn = mock.Mock()
    mock_cursor = mock.Mock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Simulate fetched results for SELECT * FROM insurance_policies
    mock_cursor.fetchall.return_value = [
        (101, "John Doe", 300.0, "Active", "2025-06-19 12:00:00")
    ]

    # Run the merge function
    merge_into_table.merge_data_from_stage()

    # Gather executed SQL statements
    executed_statements = [str(call.args[0]) for call in mock_cursor.execute.call_args_list]

    # Assertions
    assert any("CREATE OR REPLACE TABLE insurance_policies" in stmt for stmt in executed_statements), \
        "❌ Expected CREATE TABLE statement not found."

    assert any("COPY INTO insurance_raw_stage" in stmt for stmt in executed_statements), \
        "❌ Expected COPY INTO staging table not executed."

    assert any("MERGE INTO insurance_policies" in stmt for stmt in executed_statements), \
        "❌ Expected MERGE INTO statement not executed."

    assert mock_cursor.fetchall.called, "❌ Expected fetchall() to retrieve final merged results."
    assert mock_conn.close.called, "❌ Expected Snowflake connection to be closed after execution."