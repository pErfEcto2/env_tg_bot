import lib


lib.exec_query("create table if not exists users (id bigint primary key, building_id bigint, count bigint);")
lib.exec_query("create table if not exists buildings (id bigint primary key, address text);")
lib.exec_query("create table if not exists feedbacks (timestamp datetime default current_timestamp primary key, feedback text);")

for name in ["plastic", "metall", "caps", "battaries", "paper"]:
    lib.exec_query(f"create table if not exists {name} (id bigint primary key, building_id bigint, description text, address text, lat real, lon real);")

