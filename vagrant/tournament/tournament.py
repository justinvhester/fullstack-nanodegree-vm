#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    # DELETE FROM <table_name> will remove all rows
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(id) FROM players;")
    # fetchone() returns a tuple containing a Long int
    # Use index 0 to return just the integer instead of the tuple
    player_count = c.fetchone()[0]
    conn.close()
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    # Define the SQL query to add a record to the players table
    QUERY = "INSERT INTO players (full_name) VALUES (%s);"
    # Define second argument passed to execute(), which must be a tuple
    DATA = (name, )
    # Second arg "DATA" will replace the %s inside of QUERY
    c.execute(QUERY, DATA)
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    # Use results of plyr_rcrds view to retrieve the information
    c.execute("SELECT * FROM plyr_rcrds")
    current_standings = c.fetchall()
    conn.close()
    return current_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    QUERY = "INSERT INTO matches (win, loss) VALUES (%s, %s);"
    DATA = (winner, loser)
    c.execute(QUERY, DATA)
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    stnds = playerStandings()
    pCount = countPlayers()
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM possible_matches;")
    psblMtchs = c.fetchall()
    conn.close()
    # List comprehension will create a list of tuples each containing
    # info of the 'next two' players from the stnds list
    #On the first loop through stnds[0] is the top rated player
    pairs =  [(stnds[pInfo][0], stnds[pInfo][1],
               #add 1 to the index of stnds to get the very next player
               stnds[pInfo + 1][0], stnds[pInfo + 1][1])
             # Loop through only the number of currently registered
             # players, and only for even numbers coming out of xrange
             for pInfo in xrange(pCount) if pInfo%2 == 0 ]
    #TODO: break list comprehension up into smaller steps so checking
    # psblMtchs for an available pair is easier to do before adding the tuple to pairs.
    return pairs


