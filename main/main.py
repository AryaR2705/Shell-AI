import pandas as pd
from load_data import load_datasets
from initialize_fleet import initialize_fleet
from update_fleet import update_fleet
from process_combinations import process_combinations

def main():
    # Load all the datasets
    demand, vehicles, vehicles_fuels, fuels, carbon_emission, cost_profiles = load_datasets()

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
        
        # Initialize fleet size and available vehicles for this year
        fleet_size, available_vehicles = initialize_fleet(year_vehicles, final_rows, year)
        
        # Update fleet size and sell count for this year
        max_sell, sell_count = update_fleet(final_rows, fleet_size, year, year_vehicles)
        
        # Process each size and distance bucket combination
        final_rows, available_vehicles = process_combinations(year, year_demand, year_vehicles, vehicles_fuels, final_rows, size_buckets, distance_buckets, fleet_size, available_vehicles, max_sell, sell_count)

    # Create the final DataFrame
    final_df = pd.DataFrame(final_rows)

    # Ensure Num_Vehicles is greater than or equal to 0
    final_df['Num_Vehicles'] = final_df['Num_Vehicles'].clip(lower=0)

    # Save the final DataFrame to a CSV file
    final_df.to_csv('final.csv', index=False)

    print("final.csv has been generated.")

if __name__ == "__main__":
    main()
