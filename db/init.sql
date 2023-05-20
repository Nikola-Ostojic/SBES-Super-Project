CREATE USER 'sbes'@'localhost' IDENTIFIED BY 'sbesftn';

create database if not exists sbesproject;
use sbesproject;

ALTER DATABASE sbesproject CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

GRANT ALL PRIVILEGES ON sbesproject.* TO 'sbes'@'localhost';
