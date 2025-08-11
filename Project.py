from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# --- Interactive Inputs ---
print("📚 Welcome to the Interactive Web Scraper!")
url = input("Enter the website URL (e.g., http://books.toscrape.com/): ").strip()
pages_to_scrape = int(input("How many pages do you want to scrape? (e.g., 3): "))
output_file = input("Enter the output CSV file name (without .csv): ").strip() + ".csv"

# --- Setup Selenium (Headless Mode) ---
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without browser window
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(url)
time.sleep(2)

# --- Data Lists ---
titles, prices, availabilities = [], [], []

# --- Scraping Loop ---
for page in range(1, pages_to_scrape + 1):
    print(f"🔍 Scraping page {page}...")
    
    books = driver.find_elements(By.CLASS_NAME, "product_pod")
    for book in books:
        title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
        price = book.find_element(By.CLASS_NAME, "price_color").text
        availability = book.find_element(By.CLASS_NAME, "availability").text.strip()
        
        titles.append(title)
        prices.append(price)
        availabilities.append(availability)
    
    try:
        next_button = driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
        next_button.click()
        time.sleep(2)
    except:
        print("⚠️ No more pages found.")
        break

driver.quit()

# --- Save to CSV ---
df = pd.DataFrame({"Title": titles, "Price": prices, "Availability": availabilities})
df.to_csv(output_file, index=False)

print(f"✅ Scraping completed! Data saved to {output_file}")
