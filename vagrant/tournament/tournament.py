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
    c.execute("select count(id) from players;")
    player_count = c.fetchall()
    return int(player_count[0][0])
    conn.close()


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    QUERY = "INSERT INTO players (full_name) VALUES (%s);"
    DATA = (name, )
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
    #haha    return (('1', 'Melpomene Murray', 0, 0), ('2', 'Randy Schwartz', 0, 0))
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM players ORDER BY wins desc;")
    current_standings = c.fetchall()
    return current_standings
    conn.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    updt_win_rcrd = "UPDATE players SET wins = wins+1, matches = matches+1 WHERE id = %s;"
    WNR = (winner, )
    c.execute(updt_win_rcrd, WNR)
    updt_lose_rcrd = "UPDATE players SET matches = matches+1 WHERE id = %s;"
    LSR = (loser, )
    c.execute(updt_lose_rcrd, LSR)
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
#TODO:Pull out all player records to determine closest match in wins column
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, full_name, wins FROM players;")
    = c.fetchall()

#TODO:Sanity check pairings to verify each id appears only once
#TODO:Return a list of tuples per above
    return 
    conn.close()
#    return [(34, "Jay Leno", 36, "David Letterman"), (33, "Jimmy Fallon", 35, "Jimmy Kimmel")]

if __name__ == '__main__':
    countPlayers()
    print "DONE!"

