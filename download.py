import requests
import pandas as pd

# codes = pd.read_excel('nta.xlsx')['Code'].to_list()
count = 0
codes = pd.read_csv('scraped_data.csv')['CENTER COODE'].unique().tolist()

for i in codes:
    url = f'https://neetfs.ntaonline.in/NEET_2024_Result/{i}.pdf'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_name = f'data/{i}.pdf'
        with open(file_name, 'wb') as file:
            file.write(response.content)
        count += 1
    else:
        print(response.status_code)
        print(f"Error for center code {i}")

print(count)
