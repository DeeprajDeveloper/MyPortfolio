query = r"Select * from table WHERE"

json_payload = {
    "col1": 1,
    "col2": 2
}

for key, item in json_payload.items():
    query = rf"{query} {key} = {item} AND"
print(query[:-4])
