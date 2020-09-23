-- Database: budgetingapp

-- DROP DATABASE budgetingapp;

CREATE DATABASE budgetingapp
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE USER budgetingappuser WITH password 'password';

ALTER ROLE budgetingappuser SET client_encoding TO 'utf8';
ALTER ROLE budgetingappuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE budgetingappuser SET timezone to 'UTC'; 
ALTER ROLE budgetingappuser CREATEDB;

GRANT ALL PRIVILEGES ON DATABASE budgetingapp TO budgetingappuser;


