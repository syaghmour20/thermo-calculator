import mysql.connector

class Connector:
    """Used to create connections to the MySQL database on the localhost."""

    def make_connection(database):
        """Creates a connection to the MySQL server based on the given database name."""
        
        host = "localhost"
        user = "root"
        password = "WH3N23AT"
        
        # Catch exceptions for any errors that may arise from connecting to database
        conn = None
        try:
             conn = mysql.connector.connect(host=host, database=database, user=user,
                    password=password)
        except mysql.connector.Error as e:
            print("Error code:", e.errno)
            print("SQLSTATE value: " + e.sqlstate)
            print("Error message: " + e.msg)
            print("Error: ",  e)

        return conn

    def close_connection(conn):
        """Closes a previously established connection to a MySQL database."""
        
        if (conn.is_connected()):
            conn.close()
        else:
            print("Connection either already closed or never connected.")

        return


