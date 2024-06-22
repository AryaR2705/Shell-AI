import pandas as pd
import numpy as np

# Load all the datasets
demand = pd.read_csv('demand.csv')
vehicles = pd.read_csv('vehicles.csv')
vehicles_fuels = pd.read_csv('vehicles_fuels.csv')
fuels = pd.read_csv('fuels.csv')
carbon_emission = pd.read_csv('carbon_emission.csv')
cost_profiles = pd.read_csv('cost_profiles.csv')

# Create a list to store the rows for the final DataFrame
final_rows = []

# Define all size and distance bucket combinations
size_buckets = ['S1', 'S2', 'S3', 'S4']
distance_buckets = ['D1', 'D2', 'D3', 'D4']

# Process each year from 2023 to 2038
for year in range(2023, 2039):
    # Filter data for the current year
    year_demand = demand[demand['Year'] == year]
    year_vehicles = vehicles[vehicles['Year'] == year]
    year_fuels = fuels[fuels['Year'] == year]
    year_carbon_limit = carbon_emission[carbon_emission['Year'] == year]['Carbon emission CO2/kg'].values[0]
    
    # Process each size and distance bucket combination
    for size in size_buckets:
        for distance in distance_buckets:
            # Find the demand for this combination
            combination_demand = year_demand[(year_demand['Size'] == size) & (year_demand['Distance'] == distance)]['Demand (km)'].sum()
            
            # Find suitable vehicles for this combination
            suitable_vehicles = year_vehicles[(year_vehicles['Size'] == size) & (year_vehicles['Distance'] >= distance)]
            
            # If no suitable vehicles, continue to next combination
            if suitable_vehicles.empty:
                continue
            
            # Loop through each suitable vehicle
            for _, vehicle in suitable_vehicles.iterrows():
                # Check if vehicle ID has been bought before
                if not any((row['Type'] == 'Buy' and row['ID'] == vehicle['ID']) for row in final_rows):
                    # Add a 'Buy' operation for this vehicle if not already in fleet
                    final_rows.append({
                        'Year': year,  # Assuming this is the current year
                        'ID': vehicle['ID'],
                        'Num_Vehicles': 1,  # Buying one vehicle
                        'Type': 'Buy',
                        'Fuel': 'Electricity',  # Assuming a default or based on available data
                        'Distance_bucket': distance,
                        'Distance_per_vehicle(km)': 0.0,  # No distance yet
                        'Purchase_Year': year  # Purchase in the current year
                    })
                
                # Get fuel info for this vehicle
                vehicle_fuel = vehicles_fuels[vehicles_fuels['ID'] == vehicle['ID']]
                if not vehicle_fuel.empty:
                    fuel_type = vehicle_fuel['Fuel'].values[0]
                    fuel_consumption = vehicle_fuel['Consumption (unit_fuel/km)'].values[0]
                else:
                    fuel_type = 'Unknown'
                    fuel_consumption = 0.0
                
                # Calculate number of vehicles needed to meet demand
                yearly_range = vehicle['Yearly range (km)']
                num_vehicles = max(1, int(np.ceil(combination_demand / yearly_range)))
                
                # Calculate distance per vehicle
                distance_per_vehicle = min(yearly_range, combination_demand / num_vehicles)
                
                # Determine the purchase year of the vehicle
                purchase_year = year
                
                # Ensure vehicle is sold by the end of its 10th year
                if purchase_year + 10 <= 2038:
                    final_rows.append({
                        'Year': year,
                        'ID': vehicle['ID'],
                        'Num_Vehicles': num_vehicles,
                        'Type': 'Buy',
                        'Fuel': fuel_type,
                        'Distance_bucket': distance,
                        'Distance_per_vehicle(km)': 0.0,  # Since it's a buy operation, no distance yet
                        'Purchase_Year': purchase_year
                    })
                    
                    final_rows.append({
                        'Year': purchase_year + 10,
                        'ID': vehicle['ID'],
                        'Num_Vehicles': 1,  # Selling one vehicle at a time
                        'Type': 'Sell',
                        'Fuel': '',
                        'Distance_bucket': '',
                        'Distance_per_vehicle(km)': 0.0,
                        'Purchase_Year': purchase_year
                    })

                # Use operation
                final_rows.append({
                    'Year': year,
                    'ID': vehicle['ID'],
                    'Num_Vehicles': num_vehicles,
                    'Type': 'Use',
                    'Fuel': fuel_type,
                    'Distance_bucket': distance,
                    'Distance_per_vehicle(km)': distance_per_vehicle,
                    'Purchase_Year': purchase_year
                })

# Create the final DataFrame
final_df = pd.DataFrame(final_rows)

# Save the final DataFrame to a CSV file
final_df.to_csv('final.csv', index=False)

print("final.csv has been generated.")
