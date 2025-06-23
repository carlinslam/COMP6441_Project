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

        print(f"Visiting profile: {url}")
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Name
        try:
            name_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'inline') and contains(@class, 'break-words')]")))
            name = name_elem.text.strip()
        except:
            name = "N/A"

        # Headline
        try:
            headline = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text.strip()
        except:
            headline = "N/A"

        # Location
        try:
            location = driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline.t-black--light.break-words").text.strip()
        except:
            location = "N/A"

        # Job Title
        try:
            job_title = driver.find_element(By.XPATH, "//div[contains(@class, 'align-items-center')]//span[@aria-hidden='true']").text.strip()
        except:
            job_title = "N/A"

        # Company Name
        try:
            company_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 't-14') and contains(@class, 't-normal')]/span[@aria-hidden='true']")))
            company_name = company_elem.text.split("·")[0].strip()
        except:
            company_name = "N/A"

        data = {
            "employee_name": name,
            "headline": headline,
            "location": location,
            "job_title": job_title,
            "company_name": company_name,
            "linkedin_url": url,
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
