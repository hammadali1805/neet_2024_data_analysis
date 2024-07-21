from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)

# Path to the ChromeDriver executable
webdriver_service = Service(r"C:\Users\hamma\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Update this path

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

try:
    # Navigate to the website
    driver.get('https://neet.ntaonline.in/frontend/web/common-scorecard/index')  # Replace with the target website URL

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'scorecardData')))

    # Set the number of entries to display to 500
    select = Select(driver.find_element(By.NAME, 'scorecardData_length'))
    select.select_by_value('500')
    
    # Wait for the page to reload with new settings
    time.sleep(2)  # Adjust sleep duration if necessary

    # Function to extract data from the current page

    # Initialize data list
    data = []
    for i in range(10):
        for page in range(i):
            element = driver.find_element(By.XPATH, f"//a[@data-dt-idx='8']")
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(2)
            element.click()
            time.sleep(2)

        element = driver.find_element(By.ID, 'scorecardData')
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

        rows = driver.find_elements(By.CSS_SELECTOR, '#scorecardData tbody tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            data.append([col.text for col in cols])

finally:
    # Close the browser
    driver.quit()



# Convert data to DataFrame
df = pd.DataFrame(data, columns=['Sr.No.', 'CENTER STATE', 'CENTER CITY', 'CENTER NAME', 'CENTER CODE', 'View Result'])
df = df.drop(['Sr.No.', 'View Result'], axis=1)
# Save data to CSV
df.to_csv('scraped_data.csv', index=False)

print("Data has been saved to scraped_data.csv")