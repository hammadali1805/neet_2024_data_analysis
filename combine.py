import os
import pandas as pd
from multiprocessing import Pool

def read_csv_file(file_path):
    """Read a CSV file and return a DataFrame."""
    df = pd.read_csv(file_path)
    return df

def get_files_list(directory, extension='.csv'):
    """Get a list of file paths with the specified extension in the given directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]

if __name__ == '__main__':
    csv_directory = './data_csv'  # Directory containing the CSV files
    
    files = get_files_list(csv_directory)
    
    # Using multiprocessing Pool to parallelize the reading of CSV files
    with Pool(processes=os.cpu_count()) as pool:
        dataframes = pool.map(read_csv_file, files)
    
    # Concatenate all the DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Optional: Save the combined DataFrame to a CSV file
    combined_df.to_csv('combined_data.csv', index=False)
    
    # Print the first few rows of the combined DataFrame to verify
    print(combined_df.head())
