import pandas as pd

df =  pd.read_csv("combined_data.csv")
df2 = pd.read_csv("scraped_data.csv")

merged = pd.merge(df,df2, on="CENTER CODE")

merged.to_csv("allData.csv", index=False)