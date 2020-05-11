from sqlconnector import Connector
from dataupdater import DataUpdater
import pandas as pd

capacity_data = pd.read_csv("data/heat_capacity_constants.csv")

for index, row in capacity_data.iterrows():
    DataUpdater.insert_heat_capacity_data(row["Species"], row["A"], row["B"], row["C"], row["D"])
