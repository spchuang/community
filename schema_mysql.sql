/*
Table schema definition
http://farm2.staticflickr.com/1296/533233247_d8ac5afbec_o.jpg
scalabele: http://20bits.com/article/data-management-facebook-style
*/
CREATE DATABASE community;
USE community;
CREATE TABLE users(
   id INTEGER(11) NOT NULL AUTO_INCREMENT, 
   first_name VARCHAR(20)     NOT NULL,
   last_name  VARCHAR(20)     NOT NULL,
   user_name  VARCHAR(30)     NOT NULL, 
   password   CHAR(60) BINARY NOT NULL,
   email      VARCHAR(100)    NOT NULL,
   gender     TINYINT(2)      NOT NULL,
   permission TINYINT(3)      NOT NULL DEFAULT 0,
   PRIMARY KEY (id),
   Unique(email),
   Unique(user_name)
  /*
   TODO: add more fields for user profiles like about me, birthday, and other shit
  */
);

CREATE TABLE communities(
   id          INTEGER(11)     NOT NULL AUTO_INCREMENT, 
   name        VARCHAR(50)     NOT NULL,
   description VARCHAR(300),           
   is_public   TINYINT(2)      NOT NULL DEFAULT 0,
   PRIMARY KEY (id)
);

CREATE TABLE user_in_community(
   id             INTEGER(11)     NOT NULL AUTO_INCREMENT, 
   user_id        INTEGER(11)     NOT NULL,
   community_id  INTEGER(11)     NOT NULL,
   PRIMARY KEY (id),
   Unique(user_id, community_id),
   FOREIGN KEY (user_id) REFERENCES users(id),
   FOREIGN KEY (community_id) REFERENCES communities(id)
);
