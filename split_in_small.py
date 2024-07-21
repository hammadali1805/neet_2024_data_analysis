import pandas as pd

# Assuming df is your original DataFrame
df = pd.read_csv("allData.csv")
# Splitting into 10 smaller DataFrames
num_chunks = 10
chunk_size = len(df) // num_chunks

# Creating chunks
chunks = [df[i*chunk_size:(i+1)*chunk_size] for i in range(num_chunks)]

# For the last chunk, include the remaining rows
chunks.append(df[num_chunks*chunk_size:])

# Optionally, you can store these chunks in separate files
for i, chunk in enumerate(chunks):
    chunk.to_csv(f'data2024/df_chunk_{i+1}.csv', index=False, header=True)  # Save each chunk to a CSV file

print("DataFrames split into 10 smaller files successfully.")
