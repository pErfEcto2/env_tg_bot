import lib


lib.exec_query("create table if not exists users (id bigint primary key, building_id bigint);")
lib.exec_query("create table if not exists waste_collection_points (id bigint primary key, address text);")
lib.exec_query("create table if not exists feedbacks (timestamp datetime default current_timestamp primary key, feedback text);")

