from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time, json

# REPLACE THIS with your actual li_at cookie
LI_AT_COOKIE = "AQEFAQ8BAAAAABYsq9MAAAGWkJYWzwAAAZekTQtIVgAAsnVybjpsaTplbnRlcnByaXNlQXV0aFRva2VuOmVKeGpaQUFCK2RzMklFcTRlMVU2aUdaZXZlUWlJNGhScm1kekRjeUlQRmJCeDhBTUFLNmdDR3M9XnVybjpsaTplbnRlcnByaXNlUHJvZmlsZToodXJuOmxpOmVudGVycHJpc2VBY2NvdW50OjIwODc3NDAsMzI3OTIwMjMxKV51cm46bGk6bWVtYmVyOjExOTE3MzIyMzclDmCpVHYJCMOxj2gpwuEENZcfemr0hY6hL54yLnlghKOULMt9U71lpeudv08CocQlqVZdPyNV5wYvMvUIoy2pOlFSKK38N0PtielMACNgQ17WwRtXlWeDncFQUO-wvVGE9HGOQ3CmmNCxP9gBbd802T8mbE8GNgXzx29QkQPfy4YROuBg9INd6CKUAD74EPLal40T"

def get_linkedin_profile(url):
    print("Launching headless Chrome...")

    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    try:
        # Step 1: Add li_at cookie
        driver.get("https://www.linkedin.com")
        driver.add_cookie({
            "name": "li_at",
            "value": LI_AT_COOKIE,
            "domain": ".linkedin.com",
            "path": "/",
            "secure": True,
            "httpOnly": True
        })
        driver.refresh()
        time.sleep(2)

        # Step 2: Go to profile
        print(f"Visiting profile: {url}")
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Step 3: Extract fields
        try:
            name_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge")))
            name = name_elem.text.strip()
        except:
            name = "N/A"

        try:
            headline = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text.strip()
        except:
            headline = "N/A"

        try:
            location = driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline.t-black--light.break-words").text.strip()
        except:
            location = "N/A"

        try:
            experience_section = driver.find_element(By.ID, "experience")
            company_elem = experience_section.find_element(By.CSS_SELECTOR, "span.t-14.t-normal")
            company_name = company_elem.text.strip()
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

        print("Scraping complete.")
        return data

    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    print("LinkedIn Profile Scraper")
    link = input("Paste LinkedIn URL: ").strip()
    profile = get_linkedin_profile(link)
    os.makedirs("profiles", exist_ok=True)

    company = profile['company_name'].replace(' ', '_') if profile['company_name'] != "N/A" else "unknown_company"
    name = profile['employee_name'].replace(' ', '_') if profile['employee_name'] != "N/A" else "unknown_person"
    fname = f"profiles/{company}_{name}.json"

    with open(fname, "w") as f:
        json.dump(profile, f, indent=2)

    print("Profile saved to:", fname)
