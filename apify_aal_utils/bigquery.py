from datetime import date, datetime
from typing import Dict, List

from google.cloud.bigquery.client import Client


def sql_where(_dict: Dict, grouping="AND") -> str:
    """
    Converts a dictionary into a SQL WHERE clause. Use the optional grouping argument
    to define the exact gouping of the individual keys.

    _dict = {
        "str_field": "a",
        "int_field": 1,
        "bool_field": True,
        "date_field": datetime.now().date(),
        "null_field": None,
    }
    >>> sql_where(_dict)
    "WHERE str_field = 'a' AND int_field = 1 AND bool_field = True AND date_field = '2024-06-16' AND null_field = NULL"
    """
    if not _dict:
        raise ValueError("The WHERE dictionary argument cannot be empty.")
    if grouping.lower() not in ["and", "or"]:
        raise ValueError(
            "The WHERE clause's Grouping Value must be either 'AND' or 'OR'."
        )

    temp = list()
    for k, v in _dict.items():
        if type(v) == str or type(v) == date or type(v) == datetime:
            temp.append(f"{k} = '{v}'")
        elif v is None:
            temp.append(f"{k} = NULL")
        else:
            temp.append(f"{k} = {v}")
    result = f" {grouping} ".join(temp)
    result = f"WHERE {result}"
    return result


def _list_to_insert_values(items: List) -> str:
    """
    _list = ['a', 2, True, 'b', datetime.now()]
    >>> _list_to_insert_values(_list)
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
    result = ", ".join(result_temp)
    return result


def _compose_insert_stmt(table_ref: str, records: List[Dict]) -> str:
    """
    https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#insert_statement

    INSERT dataset.inventory (product, price, quantity)
    VALUES
        ('top load washer', 499.99, 10),
        ('front load washer', 899.99 20),
        ('oven', 1099.00, 5)
    """
    columns: str = ", ".join(records[0].keys())
    values_str: str = _dicts_to_insert_values(records)
    insert_statement = f"INSERT {table_ref} ({columns}) VALUES {values_str}"
    print(f"Insert Statement:\n{insert_statement}")
    return insert_statement


def insert_records(client: Client, table_ref: str, records: List[Dict]) -> int:
    insert_statement = _compose_insert_stmt(table_ref, records)
    insert_job = client.query(insert_statement)
    insert_job.result()  # Waits for the query to finish
    affected_rows: int | None = insert_job.num_dml_affected_rows
    affected_rows = affected_rows if affected_rows else 0
    print(f"Number of affected rows: {affected_rows}")
    return affected_rows


def _dict_to_update_set_values(_dict: Dict) -> str:
    """
    _dict = {
        "str_field": "a",
        "int_field": 1,
        "bool_field": True,
        "date_field": datetime.now().date(),
        "null_field": None,
    }
    >>> _dict_to_update_set_values(_dict)
    "str_field = 'a', int_field = 1, bool_field = True, date_field = '2024-06-16', null_field = NULL"
    """
    temp = list()
    for k, v in _dict.items():
        if type(v) == str or type(v) == date or type(v) == datetime:
            temp.append(f"{k} = '{v}'")
        elif v is None:
            temp.append(f"{k} = NULL")
        else:
            temp.append(f"{k} = {v}")
    result = ", ".join(temp)
    return result


def _compose_update_stmt(table_ref: str, record: Dict, where_clause: str) -> str:
    """
    https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#update_statement

    UPDATE dataset.inventory
    SET price = 999.99,
        quantity = NULL
    WHERE product = 'oven'
    """
    set_values_str: str = _dict_to_update_set_values(record)
    where_clause = where_clause.removeprefix("where").strip()
    where_clause = where_clause.replace('"', "'")
    update_statement = f"UPDATE {table_ref} SET {set_values_str} WHERE {where_clause}"
    print(update_statement)
    return update_statement


def update_record(
    client: Client, table_ref: str, record: Dict, where_clause: str
) -> int:
    update_statement = _compose_update_stmt(table_ref, record, where_clause)
    update_job = client.query(update_statement)
    update_job.result()  # Waits for the query to finish
    affected_rows: int | None = update_job.num_dml_affected_rows
    affected_rows = affected_rows if affected_rows else 0
    print(f"Number of affected rows: {affected_rows}")
    return affected_rows
