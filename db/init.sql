CREATE USER 'sbes'@'localhost' IDENTIFIED BY 'sbesftn';

create database if not exists sbesproject;
use sbesproject;

GRANT ALL PRIVILEGES ON sbesproject.* TO 'sbes'@'localhost';

ALTER DATABASE sbesproject CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE users (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Username varchar(255) UNIQUE,
    Password varchar(255)
);

INSERT INTO users (Username, Password) VALUES ('ftn', 'sbesadminftn')

