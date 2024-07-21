import pandas as pd
import os

def combine_csv_files(directory, file_pattern):
    """
    Combines multiple CSV files from a directory into a single DataFrame.
    
    Parameters:
    directory (str): The directory containing the CSV files.
    file_pattern (str): The pattern of the file names to match (e.g., 'df_chunk_*.csv').
    
    Returns:
    pd.DataFrame: Combined DataFrame from all the CSV files.
    """
    # List all files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.startswith(file_pattern)]
    
    # Sort files to maintain order
    files.sort()

    # Combine all files into a single DataFrame
    combined_df = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)
    
    return combined_df

# Usage example:
directory = './data2024'
file_pattern = 'df_chunk_'
combined_df = combine_csv_files(directory, file_pattern)

print("DataFrames combined successfully.")
print(combined_df.shape)
