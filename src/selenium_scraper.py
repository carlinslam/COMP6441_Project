from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time, json
import ollama

# REPLACE THIS with your actual li_at cookie
LI_AT_COOKIE = input("Paste your LinkedIn li_at cookie: ").strip()


def generate_email(data):
    name = data.get("employee_name", "there")
    job = data.get("job_title", "your role")
    company = data.get("company_name", "your company")

    print("\n--- Custom Email Prompt Generator ---")
    topic = input("What is the topic/focus of the email? (e.g., cybersecurity, AI innovation): ").strip()
    purpose = input("What is the purpose of this email? (e.g., invite to speak, reset password, HR update): ").strip()
    call_to_action = input("What is the final request? (e.g., confirm availability, click a link, open a document): ").strip()
    tone = input("What tone do you want the email to use? (e.g., professional, urgent, friendly): ").strip()
    event = input("Optional – name of event or occasion (or press Enter to skip): ").strip()

    event_text = f" at {event}" if event else ""

    # Construct prompt dynamically based on user inputs
    prompt = f"""
You are a {tone} corporate communicator. Write an email to {name}, a {job} at {company}, regarding {topic}{event_text}. 
The purpose of the email is to {purpose}. Conclude the email with a clear, polite instruction asking them to {call_to_action}.
"""

    # Query Ollama
    response = ollama.chat(
        model='llama3',
        messages=[
            {"role": "system", "content": "You are a professional email writer skilled in business communication."},
            {"role": "user", "content": prompt}
        ]
    )

    email_body = response['message']['content']

    # Save the email to a file
    safe_name = name.replace(" ", "_").replace("(", "").replace(")", "")
    email_dir = "generated_emails"
    os.makedirs(email_dir, exist_ok=True)

    email_path = f"{email_dir}/custom_email_{safe_name}.txt"
    with open(email_path, "w") as f:
        f.write(email_body)

    print("\nEmail generated successfully.")
    print("Email saved to:", email_path)


    
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
    print("LinkedIn Profile Scraper + Email Generator")
    link = input("Paste LinkedIn URL: ").strip()
    
    try:
        profile_data = get_linkedin_profile(link)
    except Exception as e:
        print("Failed to scrape profile:", e)
        exit(1)

    # Save profile JSON
    os.makedirs("profiles", exist_ok=True)
    company = profile_data.get('company_name') or "unknown_company"
    name = profile_data.get('employee_name') or "unknown_person"

    company = company.replace(' ', '_').replace('/', '_')
    name = name.replace(' ', '_').replace('/', '_')

    os.makedirs("profiles", exist_ok=True)
    fname = f"profiles/{company}_{name}.json"


    with open(fname, "w") as f:
        json.dump(profile_data, f, indent=2)

    print("Profile saved to:", fname)

    # Generate email
    generate_email(profile_data)
