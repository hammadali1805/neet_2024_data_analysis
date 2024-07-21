import pandas as pd
import tabula
import os
from multiprocessing import Pool


def list_files_in_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        file_list = [file[:-4] for file in files if os.path.isfile(os.path.join(folder_path, file))]
        return file_list
    except Exception as e:
        print(f"Error: {e}")
        return []

folder_path = './data'
files = list_files_in_folder(folder_path)

# Function to convert PDF to a single-column CSV
def pdf_to_single_column_csv(pdf_file, csv_file):
    # Read PDF file and extract tables
    tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
    
    if tables:
        # Combine all extracted tables into one DataFrame
        combined_df = pd.concat(tables, ignore_index=True)

        # Reshape DataFrame to a long format with 'Sr_no' and 'Marks' columns
        long_df = pd.DataFrame()

        for i in range(0, len(combined_df.columns), 2):
            temp_df = combined_df.iloc[:, i:i+2].copy()
            temp_df.columns = ['STUDENT SERIAL NUMBER', 'MARKS']
            long_df = pd.concat([long_df, temp_df], ignore_index=True)
        
        # Drop rows where both 'Sr_no' and 'Marks' are NaN
        long_df.dropna(subset=['STUDENT SERIAL NUMBER', 'MARKS'], how='all', inplace=True)
        long_df['CENTER CODE'] = pdf_file[5:-4] 

        # Save the reshaped DataFrame to a CSV file
        long_df.to_csv(csv_file, index=False)
        print(f"CSV file '{csv_file}' created successfully.")
    else:
        print(f"No tables found in the PDF {pdf_file}.")

def process_file(file):
    pdf_file = f'data/{file}.pdf'     # Replace with your PDF file path
    csv_file = f'data_csv/{file}.csv' # Replace with desired CSV output path
    pdf_to_single_column_csv(pdf_file, csv_file)

# Example usage:
if __name__ == "__main__":
    
    # Using multiprocessing Pool to parallelize the process
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(process_file, files)

