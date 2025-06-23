from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import os

def scrape_linkedin_profile(url):
    # Set up headless Chrome
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    print(f"🌐 Visiting {url}")
    driver.get(url)
    time.sleep(3)  # Let content load

    try:
        full_name = driver.find_element(By.TAG_NAME, "h1").text
    except:
        full_name = "N/A"

    try:
        headline = driver.find_element(By.CLASS_NAME, "text-body-medium").text
    except:
        headline = "N/A"

    try:
        location = driver.find_element(By.CLASS_NAME, "text-body-small").text
    except:
        location = "N/A"

    profile_data = {
        "employee_name": full_name,
        "headline": headline,
        "location": location,
        "linkedin_url": url
    }

    driver.quit()
    return profile_data

def save_profile_json(profile_data, company_name):
    os.makedirs("profiles", exist_ok=True)
    name_safe = profile_data["employee_name"].replace(" ", "_").replace(".", "")
    filename = f"profiles/{company_name}_{name_safe}.json"

    # Add dummy context for now
    profile_data["company_name"] = company_name
    profile_data["public_context"] = "Recent updates and internal events from company news."

    with open(filename, "w") as f:
        json.dump(profile_data, f, indent=2)

    print(f"✅ Profile saved to {filename}")

if __name__ == "__main__":
    linkedin_url = input("Paste LinkedIn profile URL: ").strip()
    company_name = input("Enter company name: ").strip()
    
    profile = scrape_linkedin_profile(linkedin_url)
    save_profile_json(profile, company_name)
