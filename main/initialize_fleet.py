def initialize_fleet(year_vehicles, final_rows, year):
    fleet_size = {}
    available_vehicles = {}

    for vehicle_id in year_vehicles['ID'].values:
        fleet_size[vehicle_id] = sum(row['Num_Vehicles'] for row in final_rows 
                                     if row['Year'] < year and row['ID'] == vehicle_id and row['Type'] == 'Buy') - \
                                 sum(row['Num_Vehicles'] for row in final_rows 
                                     if row['Year'] < year and row['ID'] == vehicle_id and row['Type'] == 'Sell')
        available_vehicles[vehicle_id] = fleet_size[vehicle_id] - \
                                         sum(row['Num_Vehicles'] for row in final_rows 
                                             if row['Year'] == year and row['ID'] == vehicle_id and row['Type'] == 'Use')
    return fleet_size, available_vehicles
