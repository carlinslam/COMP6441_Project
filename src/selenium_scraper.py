import time
import json
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_linkedin_profile(url, cookies_json='cookies.json'):
    # Setup headless Chrome
    opts = Options()
    opts.add_argument("--headless=new")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=opts)


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

    # Extract name, headline, location, company
    name = driver.find_element("css selector", ".text-heading-xlarge").text
    headline = driver.find_element("css selector", ".text-body-medium.break-words").text
    location = driver.find_element("css selector", ".text-body-small.inline.t-black--light.break-words").text

    exp = driver.find_elements("css selector", "#experience-section .pv-entity__company-name")[0].text

    data = {
        "employee_name": name,
        "headline": headline,
        "location": location,
        "linkedin_url": url,
        "company_name": exp,
        "public_context": ""
    }

    driver.quit()
    return data

if __name__ == "__main__":
    link = input("Paste LinkedIn URL: ").strip()
    profile = get_linkedin_profile(link)
    os.makedirs("profiles", exist_ok=True)
    fname = f"profiles/{profile['company_name']}_{profile['employee_name']}.json"
    with open(fname, "w") as f:
        json.dump(profile, f, indent=2)
    print("✅ Saved profile:", fname)
