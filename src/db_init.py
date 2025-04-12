import lib


lib.exec_query("create table if not exists users (id int primary key, building varchar(64));")
lib.exec_query("create table if not exists feedbacks (timestamp datetime default current_timestamp primary key, feedback text);")

