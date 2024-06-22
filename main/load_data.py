import pandas as pd

def load_datasets():
    demand = pd.read_csv('demand.csv')
    vehicles = pd.read_csv('vehicles.csv')
    vehicles_fuels = pd.read_csv('vehicles_fuels.csv')
    fuels = pd.read_csv('fuels.csv')
    carbon_emission = pd.read_csv('carbon_emission.csv')
    cost_profiles = pd.read_csv('cost_profiles.csv')
    
    return demand, vehicles, vehicles_fuels, fuels, carbon_emission, cost_profiles
    