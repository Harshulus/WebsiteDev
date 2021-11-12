import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg="static/db/database.db"):
        self.conn = sqlite3.connect(database_arg, check_same_thread=False)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0,
            muted INTEGER DEFAULT 0
        )""")

        # Add our admin user
        # self.add_user('admin', admin_password, admin=1)
        # self.add_user('user', 'user', admin=0)
        # self.add_user('Billy', 'user', admin=0)
        self.commit()

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, admin=0, muted=0):
        sql_cmd = """
                INSERT INTO Users (username, password, admin, muted)
                VALUES('{username}', '{password}', {admin}, {muted})
            """

        sql_cmd = sql_cmd.format(username=username, password=password, admin=admin, muted=muted)

        self.execute(sql_cmd)
        self.commit()
        return True

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, password=password)

        # If our query returns
        self.execute(sql_query)
        val = self.cur.fetchone()
        if val != None:
            return True
        else:
            return False

#-----------------------------------------------------------------------------

    # Check register credentials
    def check_register(self, username):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)

        # If our query returns
        self.execute(sql_query)
        val = self.cur.fetchone()
        if val == None:
            return True
        else:
            return False

    #-----------------------------------------------------------------------------

    # Return all users
    def get_all_users(self):
        sql_query = """
                SELECT username 
                FROM Users
            """

        # If our query returns
        self.execute(sql_query)
        val = self.cur.fetchall()
        ls = []
        for user in val:
            ls.append(user[0])
        # print(ls)
        return ls

    #-----------------------------------------------------------------------------

    # Return all muted users
    def get_muted_users(self):
        sql_query = """
                SELECT username 
                FROM Users
                WHERE muted = '1'
            """

        # If our query returns
        self.execute(sql_query)
        val = self.cur.fetchall()
        ls = []
        for user in val:
            ls.append(user[0])
        return ls
    
    #-----------------------------------------------------------------------------

    # Return all unmuted users
    def get_unmuted_users(self):
        sql_query = """
                SELECT username 
                FROM Users
                WHERE muted = '0'
            """

        # If our query returns
        self.execute(sql_query)
        val = self.cur.fetchall()
        ls = []
        for user in val:
            ls.append(user[0])
        return ls

    #-----------------------------------------------------------------------------

    # Check if user is an admin
    def check_if_admin(self, username):
        sql_query = """
                SELECT admin
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)

        # If our query returns
        self.execute(sql_query)
        val = self.cur.fetchone()
        if val[0] == 1:
            return True
        else:
            return False

    #-----------------------------------------------------------------------------

    # Mutes the user
    def mute_user(self, username):
        sql_cmd = """
                UPDATE Users
                SET muted = 1
                WHERE username = '{username}'
            """

        sql_cmd = sql_cmd.format(username=username)

        self.execute(sql_cmd)
        self.commit()
        return True

    #-----------------------------------------------------------------------------

    # Unmutes the user
    def unmute_user(self, username):
        sql_cmd = """
                UPDATE Users
                SET muted = 0
                WHERE username = '{username}'
            """

        sql_cmd = sql_cmd.format(username=username)

        self.execute(sql_cmd)
        self.commit()
        return True

    #-----------------------------------------------------------------------------

    # Check if user is muted
    def check_muted(self, username):
        sql_query = """
                SELECT muted
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)

        # If our query returns
        self.execute(sql_query)
        val = self.cur.fetchone()
        if val[0] == 1:
            return True
        else:
            return False

    #-----------------------------------------------------------------------------

    # Remove a user from the database
    def remove_user(self, username):
        sql_cmd = """
                DELETE FROM Users
                WHERE username = '{username}'
            """

        sql_cmd = sql_cmd.format(username=username)

        self.execute(sql_cmd)
        self.commit()
        return True

        
