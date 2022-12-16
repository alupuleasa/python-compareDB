# Module Imports
import mariadb
import sys
import dumper

# Connect to MariaDB Platform
class dbConnect:
    def __init__(self, DB):
        try:
            conn = mariadb.connect(
                user=DB['user'],
                password=DB['password'],
                host=DB['host'],
                port=DB['port'],
                database=DB['name']
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        else:
            self.conn = conn
    def executeQuery(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()
