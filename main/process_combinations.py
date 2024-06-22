import numpy as np

def process_combinations(year, year_demand, year_vehicles, vehicles_fuels, final_rows, size_buckets, distance_buckets, fleet_size, available_vehicles, max_sell, sell_count):
    for size in size_buckets:
        for distance in distance_buckets:
            combination_demand = year_demand[(year_demand['Size'] == size) & (year_demand['Distance'] == distance)]['Demand (km)'].sum()
            
            suitable_vehicles = year_vehicles[(year_vehicles['Size'] == size) & (year_vehicles['Distance'] == distance)]
            
            if suitable_vehicles.empty or combination_demand == 0:
                final_rows.append({
                    'Year': year,
                    'ID': 'N/A',
                    'Num_Vehicles': 0,
                    'Type': 'N/A',
                    'Fuel': 'N/A',
                    'Distance_bucket': f"{size}_{distance}",
                    'Distance_per_vehicle(km)': 0.0,
                    'Purchase_Year': year
                })
                continue
            
            for _, vehicle in suitable_vehicles.iterrows():
                if not any((row['Type'] == 'Buy' and row['ID'] == vehicle['ID']) for row in final_rows):
                    final_rows.append({
                        'Year': year,
                        'ID': vehicle['ID'],
                        'Num_Vehicles': 1,
                        'Type': 'Buy',
                        'Fuel': 'Electricity',
                        'Distance_bucket': f"{size}_{distance}",
                        'Distance_per_vehicle(km)': 0.0,
                        'Purchase_Year': year
                    })
                    available_vehicles[vehicle['ID']] = available_vehicles.get(vehicle['ID'], 0) + 1
                
                vehicle_fuel = vehicles_fuels[vehicles_fuels['ID'] == vehicle['ID']]
                if not vehicle_fuel.empty:
                    fuel_type = vehicle_fuel['Fuel'].values[0]
                    fuel_consumption = vehicle_fuel['Consumption (unit_fuel/km)'].values[0]
                else:
                    fuel_type = 'Unknown'
                    fuel_consumption = 0.0
                
                purchase_year = year
                if purchase_year + 10 <= 2038:
                    vehicles_to_sell = min(1, max_sell[vehicle['ID']] - sell_count[vehicle['ID']])
                    if vehicles_to_sell > 0:
                        final_rows.append({
                            'Year': purchase_year + 10,
                            'ID': vehicle['ID'],
                            'Num_Vehicles': vehicles_to_sell,
                            'Type': 'Sell',
                            'Fuel': '',
                            'Distance_bucket': f"{size}_{distance}",
                            'Distance_per_vehicle(km)': 0.0,
                            'Purchase_Year': purchase_year
                        })
                        sell_count[vehicle['ID']] += vehicles_to_sell
                
                yearly_range = vehicle['Yearly range (km)']
                num_vehicles_needed = max(1, int(np.ceil(combination_demand / yearly_range)))
                
                num_vehicles_to_use = min(num_vehicles_needed, available_vehicles.get(vehicle['ID'], 0))
                
                if num_vehicles_to_use > 0:
                    distance_per_vehicle = min(yearly_range, combination_demand / num_vehicles_to_use)
                    
                    final_rows.append({
                        'Year': year,
                        'ID': vehicle['ID'],
                        'Num_Vehicles': num_vehicles_to_use,
                        'Type': 'Use',
                        'Fuel': fuel_type,
                        'Distance_bucket': f"{size}_{distance}",
                        'Distance_per_vehicle(km)': distance_per_vehicle,
                        'Purchase_Year': purchase_year
                    })
                    
                    available_vehicles[vehicle['ID']] -= num_vehicles_to_use
                    combination_demand -= num_vehicles_to_use * distance_per_vehicle

    return final_rows, available_vehicles
