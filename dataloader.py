import mysql.connector
from sqlconnector import Connector
import sys

class DataLoader:
    """This class is used to load data from the database to the program."""

    def load_heat_capacity_data(species):
        """This method loads data from a single species."""
        
        # Make connection to database
        conn = Connector.make_connection("chme_schema")
        cursor = conn.cursor(prepared=True)
        
        # Execute query to select data from database
        query = "select a, b, c, d from HeatCapacityValues where species = %s"
        
        data = None
        try:
            cursor.execute(query, (species,))
            data = cursor.fetchone()
        except:
            Connector.handle_exception(e)
            sys.exit()

        # Close connections
        Connector.close_connection(cursor)
        Connector.close_connection(conn)

        if data is None: 
            print("No data for " + species + " in database.")
            return None
        else:
            return data

    def load_pure_property_data(species):
        """This method loads data from PureSpeciesProperties for a single species."""

        # Make connection to database
        conn = Connector.make_connection("chme_schema")
        cursor = conn.cursor(prepared=True)

        # Execute query to select data from database
        query = "select molarMass, omega, Tc, Pc, Zc, Vc, Tn from PureSpeciesProperties where species = %s"
        
        data = None
        try:
            cursor.execute(query, (species,))
            data = cursor.fetchone()
        except:
            Connector.handle_exception(e)
            sys.exit()

        # Close connections
        Connector.close_connection(cursor)
        Connector.close_connection(conn)

        if data is None:
            print("No data for " + species + " in database.")
            return None
        else:
            return data
