import mysql.connector
from sqlconnector import Connector

class DataUpdater:
    """This class acts as a means to update data in the MySQL database."""
    
    def check_value(conn, cursor, species, table):
        """Checks table ot see if the species being entered already exists in database."""

        # Execute query to select all species from database
        if table == "HeatCapacityValues":
            query = "select species from HeatCapacityValues"
        elif table == "PureSpeciesProperties":
            query = "select species from PureSpeciesProperties"
        else:
            return False

        cursor.execute(query)
        speciesList = cursor.fetchall()

        # Loop through list of species to see if name already exists
        for s in speciesList:
            if s[0] == species:
                return True
        return False

    def insert_heat_capacity_data(species, a, b, c, d):
        """Inserts data into the HeatCapacityValues table in the database."""

        # Establish a connection to the database
        conn = Connector.make_connection("chme_schema")
        cursor = conn.cursor(prepared=True)
        
        if not DataUpdater.check_value(conn, cursor, species, "HeatCapacityValues"):
            # Create insertion query and execute to the database
            query = "insert into HeatCapacityValues(species, a, b, c, d) values (%s, %s, %s, %s, %s)"
            vals = (species, a, b, c, d)
            cursor.execute(query, vals)
            conn.commit()
            
            # Close cursor and connection
            cursor.close()
            Connector.close_connection(conn)
        else:
            print("Species already exists in database.")

        return

    def insert_pure_property_data(species, molarMass, omega, tc, pc, zc, vc, tn):
        """Inserts data into the PureSpeciesProperties table in the database."""

        # Establish a connection to the database
        conn = Connector.make_connection("chme_schema")
        cursor = conn.cursor(prepared=True)

        if not DataUpdater.check_value(conn, cursor, species, "PureSpeciesProperties"):
            # Create insertion query and execute to the database
            query = "insert into PureSpeciesProperties(species, molarMass, omega, Tc, Pc, Zc, Vc, Tn) \
                    values (%s, %s, %s, %s, %s, %s, %s, %s)" 
            vals = (species, molarMass, omega, tc, pc, zc, vc, tn)
            cursor.execute(query, vals)
            conn.commit()

            # Close cursor and connection
            cursor.close()
            Connector.close_connection(conn)
        else: 
            print("Species already exists in database.")

        return
