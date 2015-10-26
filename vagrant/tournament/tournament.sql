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
    full_name text
-- May be better to separate out the wins and matches data to it's own table
-- or view per 'normalized design' in lesson 4
--    wins integer DEFAULT 0,
--    matches integer DEFAULT 0
    );

CREATE TABLE matches (
-- Column one will hold the id of the winner
    win integer references players (id),
-- Column one will hold the id of the loser
    loss integer references players (id),
-- Players will not play each other twice, so the two player combination will be unique
    primary key (win, loss)
    );
