drop table if exists entries;
drop table if exists user;
drop table if exists community;
drop table if exists user_community;

create table entries (
	id integer primary key autoincrement,
	title text not null,
	text text not null
);
create table user(
	id integer primary key autoincrement,
	first_name text not null,
	last_name text not null,
	user_name text not null,
	password text not null,
	email text not null
);

create table community(
	id integer primary key autoincrement,
	name text not null,
	description text not null
);

create table user_community(
	user_id integer,
	community_id integer,
	
	FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(community_id) REFERENCES community(id)
);