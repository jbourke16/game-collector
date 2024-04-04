CREATE DATABASE gamecollector;

CREATE USER game_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE gamecollector TO game_admin;