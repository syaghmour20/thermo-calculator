from dataupdater import DataUpdater
import pandas as pd

property_data = pd.read_csv("data/pure_species_properties.csv")

for index, row in property_data.iterrows():
    DataUpdater.insert_pure_property_data(row["Species"], row["MolarMass"], row["Omega"], row["Tc"], 
            row["Pc"], row["Zc"], row["Vc"], row["Tn"])
