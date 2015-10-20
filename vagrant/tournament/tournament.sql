-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament

CREATE TABLE players (
    id serial primary key,
    full_name text,
    wins integer DEFAULT 0,
    matches integer DEFAULT 0
    );

CREATE TABLE matches (
--    p1 integer,
--    p2 integer,
    win integer,
    loss integer,
    primary key (win, loss)
    );
