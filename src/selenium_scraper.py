import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_linkedin_profile(url, cookies_json='cookies.json'):
    # Setup headless Chrome
    opts = Options()


    # Use Service object (Selenium 4.6+)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)

    # Load cookies if available
    if os.path.exists(cookies_json):
        driver.get("https://www.linkedin.com")
        for cookie in json.load(open(cookies_json)):
            driver.add_cookie(cookie)
    else:
        print("Please login manually to LinkedIn in this Chrome instance.")
        driver.get("https://www.linkedin.com/login")
        input("Press Enter once logged in...")
        json.dump(driver.get_cookies(), open(cookies_json, "w"))
        print("👉 Cookies saved to", cookies_json)

    driver.get(url)
    time.sleep(5)  # wait for page load

    # Extract profile data
    name = driver.find_element("css selector", ".text-heading-xlarge").text
    headline = driver.find_element("css selector", ".text-body-medium.break-words").text
    location = driver.find_element("css selector", ".text-body-small.inline.t-black--light.break-words").text

    exp_elements = driver.find_elements("css selector", "#experience-section .pv-entity__company-name")
    company = exp_elements[0].text if exp_elements else "N/A"

    data = {
        "employee_name": name,
        "headline": headline,
        "location": location,
        "linkedin_url": url,
        "company_name": company,
        "public_context": ""
    }

    driver.quit()
    return data

if __name__ == "__main__":
    link = input("Paste LinkedIn URL: ").strip()
    profile = get_linkedin_profile(link)
    os.makedirs("profiles", exist_ok=True)
    fname = f"profiles/{profile['company_name'].replace(' ', '_')}_{profile['employee_name'].replace(' ', '_')}.json"
    with open(fname, "w") as f:
        json.dump(profile, f, indent=2)
    print("✅ Saved profile:", fname)
