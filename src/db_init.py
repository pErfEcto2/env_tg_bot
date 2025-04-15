import lib


lib.exec_query("create table if not exists users (id bigint primary key, building_id bigint);")
lib.exec_query("create table if not exists buildings (id bigint primary key, address text);")
lib.exec_query("create table if not exists feedbacks (timestamp datetime default current_timestamp primary key, feedback text);")
lib.exec_query("create table if not exists plastic (id bigint primary key, building_id bigint, description text, address text, lat real, lon real);")
lib.exec_query("create table if not exists metall (id bigint primary key, building_id bigint, description text, address text, lat real, lon real);")
lib.exec_query("create table if not exists caps (id bigint primary key, building_id bigint, description text, address text, lat real, lon real);")
lib.exec_query("create table if not exists battaries (id bigint primary key, building_id bigint, description text, address text, lat real, lon real);")

