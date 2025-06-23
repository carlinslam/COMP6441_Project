from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, os, time

def get_linkedin_profile(url, cookies_json='cookies.json'):
    # Set up Chrome options
    opts = Options()
    opts.add_argument("--headless=new")  # set to comment this out for manual login
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)

    # Load cookies
    driver.get("https://www.linkedin.com")
    if os.path.exists(cookies_json):
        with open(cookies_json, "r") as f:
            cookies = json.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
    else:
        print("Please login manually to LinkedIn in this Chrome instance.")
        driver.get("https://www.linkedin.com/login")
        input("Press Enter once logged in...")
        with open(cookies_json, "w") as f:
            json.dump(driver.get_cookies(), f)
        print("👉 Cookies saved to", cookies_json)

    # Go to profile
    driver.get(url)
    time.sleep(5)

    wait = WebDriverWait(driver, 10)
    try:
        name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".text-heading-xlarge"))).text
    except:
        name = "N/A"
    try:
        headline = driver.find_element(By.CSS_SELECTOR, ".text-body-medium.break-words").text
    except:
        headline = "N/A"
    try:
        location = driver.find_element(By.CSS_SELECTOR, ".text-body-small.inline.t-black--light.break-words").text
    except:
        location = "N/A"
    try:
        # Try to extract first company experience from the experience section
        company_el = driver.find_element(By.CSS_SELECTOR, "section.pv-profile-section.experience-section ul li span[aria-hidden='true']")
        company_name = company_el.text
    except:
        company_name = "N/A"

    data = {
        "employee_name": name,
        "headline": headline,
        "location": location,
        "linkedin_url": url,
        "company_name": company_name,
        "public_context": ""
    }

    driver.quit()
    return data
