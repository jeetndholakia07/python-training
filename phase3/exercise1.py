import base64
import sqlfluff
import json

def encode_base64(string: str):
    return base64.b64encode(string.encode("ascii")).decode("ascii")

def decode_base64(string: str):
    return base64.b64decode(string.encode("ascii")).decode("ascii")

def formatSQL(queryObj: dict[str]):
    query = queryObj.get("query_statement")
    if query is None:
        raise ValueError("Invalid JSON format.")
    sql_query = decode_base64(query)
    print(f"Original sql statement: \n{sql_query}")
    formatted_query = sqlfluff.fix(sql_query, dialect="snowflake")
    print(f"Formatted sql statement: \n{formatted_query}")
    return encode_base64(formatted_query)

try:
    with open("sql.json", "r") as file:
        sql_dict = json.load(file)
        formatted_sql = formatSQL(sql_dict)
        temp_dict = {"query_statement": formatted_sql}
        with open("output.json", "w") as writer:
            json.dump(temp_dict, writer, indent=4)
        print("SQL formatting successfully completed")

except (FileNotFoundError, OSError, ValueError) as e:
    print("Error:", e)