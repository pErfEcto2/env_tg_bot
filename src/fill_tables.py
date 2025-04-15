import csv
import sqlite3
import config


data = dict()
for file_name in ["metall", "caps", "battaries", "plastic", "buildings"]:
    with open("src/data/" + file_name + ".csv", "r") as f:
        for row in csv.reader(f):
            if data.get(file_name) is None:
                data[file_name] = []
            data[file_name].append([int(row[0]), *list(map(lambda x: "'" + x + "'", row[1:]))])

with sqlite3.connect(config.DB_NAME) as con:
    cur = con.cursor()
    for table in data:
        cur.execute(f"delete from {table}")

        for i, row in enumerate(data[table]):
            if table != "buildings":
                cur.execute(f"insert into {table} values ({i}, {row[0]}, {",".join(row[1:])}, null, null)")
            else:
                cur.execute(f"insert into {table} values ({row[0]}, {",".join(row[1:])})")
        
        con.commit()

