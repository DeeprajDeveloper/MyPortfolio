import sqlite3 as sql
import traceback

# region DML-functions
# This section contain functions that perform DML (Data Manipulation - INSERT/UPDATE/DELETE) Operation


def dml_execute_script(database: str, sql_script: str) -> None:
    sqlite_connection = sql.connect(database=database)
    try:
        sqlite_connection.executescript(sql_script)
        sqlite_connection.commit()
    except sql.Error as error:
        print(f"Error Message: {str(error)}")
        raise error
    finally:
        sqlite_connection.close()
# endregion

# region DQL-functions
# This section contain functions that perform DQL (Data Query - SELECT) Operation


def dql_check_if_exists(database: str, sql_script: str) -> bool:
    status: bool
    sqlite_connection = sql.connect(database=database)
    try:
        sqlite_cursor = sqlite_connection.cursor()
        sqlite_cursor.execute(sql_script)
        data_extract = sqlite_cursor.fetchone()
        if data_extract is not None:
            status = True if data_extract[0] >= 1 else False
        else:
            status = False
        return status
    except sql.Error as error:
        print(f"Error Message: {str(error)}")
        return False
    finally:
        sqlite_connection.close()


def dql_fetch_all_rows(database: str, sql_script: str, return_list=True) -> list:
    """
    Returns SQL Statement execution results as a LIST by default.
    When return_list is set to False, this returns the SQL Statement execution results as a LIST of TUPLES

    :param database: SQLITE database file path
    :param sql_script: SQL Statement to be executed
    :param return_list: Boolean. default TRUE
    :return: LIST / LIST of TUPLES
    """
    sql_data: list
    sqlite_connection = sql.connect(database=database)

    if return_list:
        sqlite_connection.row_factory = lambda cursor, row: row[0]

    try:
        sqlite_cursor = sqlite_connection.cursor()
        sqlite_cursor.execute(sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")
        raise err
    finally:
        sqlite_connection.close()


def dql_fetch_all_rows_for_one_input(database: str, sql_script: str, data_input: str, return_list=True) -> list:
    """
    Returns SQL Statement execution results after replacing the '?' with the data_input as a LIST by default.
    When return_list is set to False, this returns the SQL Statement execution results as a LIST of TUPLES

    :param database: SQLITE database file path
    :param sql_script: SQL Statement to be executed
    :param data_input: text input to replace the '?' in the SQL Statement
    :param return_list: Boolean. default TRUE
    :return: LIST / LIST of TUPLES
    """

    sqlite_connection = sql.connect(database=database)

    if return_list:
        sqlite_connection.row_factory = lambda cursor, row: row[0]

    try:
        sqlite_cursor = sqlite_connection.cursor()
        updated_sql_script = sql_script.replace('?searchValue', str(data_input))
        sqlite_cursor.execute(updated_sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")
        raise err
    finally:
        sqlite_connection.close()


def dql_fetch_one_row_for_one_input(database: str, sql_script: str, data_input: str) -> list:
    """
    Returns SQL Statement execution results after replacing the '?' with the data_input as one item by default.
    When return_list is set to False, this returns the SQL Statement execution results as a LIST of TUPLES

    :param database: SQLITE database file path
    :param sql_script: SQL Statement to be executed
    :param data_input: text input to replace the '?searchValue' in the SQL Statement
    :return: One item
    """

    sqlite_connection = sql.connect(database=database)
    sqlite_connection.row_factory = lambda cursor, row: row[0]

    try:
        sqlite_cursor = sqlite_connection.cursor()
        updated_sql_script = sql_script.replace('?searchValue', str(data_input))
        sqlite_cursor.execute(updated_sql_script)
        sql_data = sqlite_cursor.fetchone()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")
        raise err
    finally:
        sqlite_connection.close()

# endregion

# region DML-DQL-functions
# This section contain functions that perform can perform both DML (Data Manipulation - INSERT/UPDATE/DELETE) & DQL (Data Query - SELECT) Operation


def dml_dql_execute_parameterized_script(database: str, sql_script: str, data_input_list: dict) -> list:
    """
    Executes a DML where the SQL Script contains parameters (such as 'var1', 'var2', etc. preceding with an 'question mark').
    Returns a BOOLEAN true/false depending on the statement execution.

    :param database: SQLITE database file path
    :param sql_script: SQL Statement to be executed that contains parameters/variables
    :param data_input_list: a dictionary/json input that contains a key-value pair for the variables
    :return:
    """

    sqlite_connection = sql.connect(database=database)
    sqlite_connection.row_factory = lambda cursor, row: row[0]
    updated_sql_script = sql_script
    try:
        sqlite_cursor = sqlite_connection.cursor()
        for key, value in data_input_list.items():
            updated_sql_script = updated_sql_script.replace(key, str(value))
        sqlite_cursor.executescript(updated_sql_script)
        sql_data = sqlite_cursor.fetchall()
        return sql_data
    except Exception as err:
        error_code = f"{type(err).__name__}: {str(err)}"
        error_stack_trace = traceback.format_exc()
        print(f"{error_code}\n{error_stack_trace}")
    finally:
        sqlite_connection.close()
# endregion


def query_builder_from_payload(base_query: str, json_payload: dict, data_mapping: dict) -> str:
    result_query: str = rf"{base_query} WHERE"
    for key, item in json_payload.items():
        result_query += rf"{data_mapping[key]} = {item} AND"
    return result_query[:-4]
