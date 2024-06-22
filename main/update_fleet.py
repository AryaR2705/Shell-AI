import numpy as np

def update_fleet(final_rows, fleet_size, year, year_vehicles):
    max_sell = {vehicle_id: max(0, int(np.floor(fleet_size.get(vehicle_id, 0) * 0.2))) 
                for vehicle_id in year_vehicles['ID'].values}
    
    sell_count = {vehicle_id: 0 for vehicle_id in year_vehicles['ID'].values}
    
    return max_sell, sell_count
