import os
import pytest
from unittest import mock
from scripts.loaders import upload_to_stage

@mock.patch("scripts.loaders.upload_to_stage.os.listdir", return_value=["test.json"])
@mock.patch("scripts.loaders.upload_to_stage.snowflake.connector.connect")
def test_upload_to_stage(mock_connect, mock_listdir):
    # Mock connection and cursor
    mock_conn = mock.Mock()
    mock_cursor = mock.Mock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Simulate file not existing initially, then return a list for final LIST command
    mock_cursor.fetchall.side_effect = [
        [],  # for LIST @{stage}/test.json (file doesn't exist)
        [("insurance_stage/test.json.gz",)]  # for final LIST @{stage}
    ]

    # Call the function
    upload_to_stage.upload_to_internal_stage()

    # Check PUT command was issued
    put_calls = [call for call in mock_cursor.execute.call_args_list if "PUT" in str(call)]
    assert len(put_calls) > 0, "Expected at least one PUT command to be executed"

    # Check LIST command was called at least once
    list_calls = [call for call in mock_cursor.execute.call_args_list if "LIST" in str(call)]
    assert len(list_calls) >= 2, "Expected at least two LIST commands (existence check + final listing)"

    # Optional: verify specific queries
    expected_file = "test.json"
    expected_put_call = f"PUT file://{os.path.abspath(os.path.join('data/json', expected_file))} @{os.getenv('SNOWFLAKE_STAGE')} OVERWRITE=TRUE"
    assert any(expected_put_call in str(call) for call in put_calls), "Expected PUT command not found"
    # Verify that the final LIST command was executed
    final_list_call = f"LIST @{os.getenv('SNOWFLAKE_STAGE')}"
    assert any(final_list_call in str(call) for call in list_calls), "Expected final LIST command not found"
# Ensure the mock was called with the correct file path
    mock_cursor.execute.assert_any_call(expected_put_call)  