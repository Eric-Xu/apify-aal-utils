from datetime import date, datetime
from typing import Dict, List

from google.cloud.bigquery.client import Client


def _list_to_insert_values(items: List) -> str:
    """
    >>> _list_to_insert_values(['a', 2, True, 'b', datetime.now()])
    "'a', 2, True, 'b', '2024-06-16 23:24:22.715454'"
    """
    temp = list()
    for item in items:
        if type(item) == str or type(item) == date or type(item) == datetime:
            temp.append(f"'{item}'")
        elif item is None:
            temp.append("NULL")
        else:
            temp.append(f"{item}")
    result = ", ".join(temp)
    return result


def _dicts_to_insert_values(dicts: List[Dict]) -> str:
    """
    dicts = [
        {
            "str": "a",
            "int": 1,
            "bool": True,
            "datetime": datetime.now(),
        },
        {
            "str": "b",
            "int": 2,
            "bool": False,
            "date": datetime.now().date(),
        },
    ]
    >>> _dicts_to_insert_values(dicts)
    "('a', 1, True, '2024-06-16 23:37:20.011264'), ('b', 2, False, '2024-06-16')"
    """
    result_temp = list()
    for d in dicts:
        values_str = _list_to_insert_values(list(d.values()))
        result_temp.append(f"({values_str})")
    log_result = "\n".join(result_temp)
    print(f"Updated values:\n{log_result}")
    result = ", ".join(result_temp)
    return result


def _compose_insert_stmt(table_ref: str, records: List[Dict]) -> str:
    """
    https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#insert_statement

    INSERT dataset.inventory (product, quantity)
    VALUES
        ('top load washer', 10),
        ('front load washer', 20),
        ('oven', 5)
    """
    columns: str = ", ".join(records[0].keys())
    values_str: str = _dicts_to_insert_values(records)
    insert_statement = f"INSERT {table_ref} ({columns}) VALUES {values_str}"
    print(insert_statement)
    return insert_statement


def insert_records(client: Client, table_ref: str, records: List[Dict]) -> int:
    insert_statement = _compose_insert_stmt(table_ref, records)
    insert_job = client.query(insert_statement)
    insert_job.result()  # Waits for the query to finish
    affected_rows: int | None = insert_job.num_dml_affected_rows
    affected_rows = affected_rows if affected_rows else 0
    print(f"Number of affected rows: {affected_rows}")
    return affected_rows
