CREATE USER 'sbes'@'localhost' IDENTIFIED BY 'sbesftn';

create database if not exists sbesproject;
use sbesproject;

GRANT ALL PRIVILEGES ON sbesproject.* TO 'sbes'@'localhost';
