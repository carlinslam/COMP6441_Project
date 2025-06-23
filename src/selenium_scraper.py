from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, os, time

def get_linkedin_profile(url, cookies_json='cookies.json'):
    print("🟡 Launching headless Chrome...")

    opts = Options()
    opts.add_argument("--headless=new")  # Comment this for manual login
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)

    try:
        driver.get("https://www.linkedin.com")

        # Step 1: Load cookies or perform manual login
        if os.path.exists(cookies_json):
            print("🟡 Loading saved cookies...")
            try:
                with open(cookies_json, "r") as f:
                    cookies = json.load(f)
                    for cookie in cookies:
                        if "sameSite" in cookie and cookie["sameSite"] == "None":
                            cookie["sameSite"] = "Strict"  # workaround for compatibility
                        driver.add_cookie(cookie)
                driver.refresh()
                time.sleep(3)
            except Exception as e:
                print("⚠️ Failed to apply cookies. Manual login required.")
                os.remove(cookies_json)
                return get_linkedin_profile(url, cookies_json)
        else:
            print("🔒 Manual login required — headless mode may need to be disabled.")
            driver.get("https://www.linkedin.com/login")
            input("🔑 Press Enter once logged in...")
            json.dump(driver.get_cookies(), open(cookies_json, "w"))
            print("✅ Cookies saved to:", cookies_json)

        # Step 2: Visit profile URL
        print(f"🔍 Visiting profile: {url}")
        driver.get(url)
        time.sleep(5)
        wait = WebDriverWait(driver, 10)

        # Step 3: Scrape information
        def safe_text(selector, by=By.CSS_SELECTOR):
            try:
                return driver.find_element(by, selector).text.strip()
            except:
                return "N/A"

        name = safe_text(".text-heading-xlarge")
        headline = safe_text(".text-body-medium.break-words")
        location = safe_text(".text-body-small.inline.t-black--light.break-words")
        company_name = safe_text("section.pv-profile-section.experience-section ul li span[aria-hidden='true']")

        data = {
            "employee_name": name,
            "headline": headline,
            "location": location,
            "linkedin_url": url,
            "company_name": company_name,
            "public_context": ""
        }

        print("✅ Scraping complete.")
        return data

    finally:
        driver.quit()
        print("🛑 Browser closed.")

if __name__ == "__main__":
    print("🔗 LinkedIn Profile Scraper")
    link = input("Paste LinkedIn URL: ").strip()
    profile = get_linkedin_profile(link)
    os.makedirs("profiles", exist_ok=True)
    fname = f"profiles/{profile['company_name'].replace(' ', '_')}_{profile['employee_name'].replace(' ', '_')}.json"
    with open(fname, "w") as f:
        json.dump(profile, f, indent=2)
    print("📁 Profile saved to:", fname)
