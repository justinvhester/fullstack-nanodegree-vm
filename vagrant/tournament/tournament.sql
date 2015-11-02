-- Table definitions for the tournament project.

-- Create the database and connect to it
CREATE DATABASE tournament;

\c tournament

-- Create the players table, storing only a unique ID and full_name
CREATE TABLE players (
    id serial primary key,
    full_name text
    );

-- Create the matches table to record results of all matches
CREATE TABLE matches (
-- Column one will hold the id of the winner
    win integer references players (id),
-- Column two will hold the id of the loser
    loss integer references players (id),
-- Players will not play each other twice, so the two player combination will be unique
    primary key (win, loss)
    );

-- Create a view to provide player records (id, full_name, wins, matches)
CREATE VIEW plyr_rcrds AS
    SELECT
        players.id,
        players.full_name,
        count(matches.win) AS wins,
-- subquery to get the count of players.id from both the win and loss column
        (SELECT count(*) FROM matches
            WHERE players.id = matches.win
            OR players.id = matches.loss) AS matches
-- left join in case the player has zero wins, still want to return 0
    FROM players LEFT JOIN matches
    ON players.id = matches.win
    GROUP BY players.id
-- show most players with most wins at top, then order by id
    ORDER BY wins DESC, id;


