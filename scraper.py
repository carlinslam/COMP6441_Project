# scraper.py
import os
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

def search_linkedin_profiles(company_name, role_keywords="HR OR Finance"):
    query = f"site:linkedin.com/in {company_name} {role_keywords}"
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    people = []
    for result in results.get("organic_results", []):
        people.append({
            "name": result.get("title", "Unknown"),
            "profile_link": result.get("link", "N/A")
        })
    return people

def scrape_company_website(domain):
    try:
        url = f"https://www.{domain}/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return [p.get_text(strip=True) for p in soup.find_all("p")[:10]]
    except Exception as e:
        return [f"Error scraping site: {e}"]

def get_news_headlines(company_name):
    query = f"{company_name} site:reuters.com OR site:bloomberg.com"
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return [r["title"] for r in results.get("organic_results", [])]

def infer_scenario_tone(text_block):
    joined = " ".join(text_block).lower()
    if "cybersecurity" in joined or "data breach" in joined:
        return "IT security alert", "Urgent"
    elif "layoff" in joined or "freeze" in joined or "benefits" in joined:
        return "HR policy update", "Formal"
    elif "invoice" in joined or "payment" in joined:
        return "Finance document request", "Urgent"
    return "Internal comms update", "Friendly"

def run_scraper(company):
    print(f"\n🔍 Searching LinkedIn for {company} employees...")
    people = search_linkedin_profiles(company)
    for p in people[:3]:
        print(f"- {p['name']}: {p['profile_link']}")

    print(f"\n🌐 Scraping https://{company.lower()}.com...")
    website_text = scrape_company_website(company.lower())

    print(f"\n📰 Getting recent headlines...")
    headlines = get_news_headlines(company)

    combined = website_text + headlines
    scenario, tone = infer_scenario_tone(combined)

    print(f"\n📌 Inferred scenario: {scenario}")
    print(f"📌 Inferred tone: {tone}")
    print(f"\n📋 Context (top 5 lines):")
    for line in combined[:5]:
        print(f"- {line}")

# Run test
if __name__ == "__main__":
    company = input("Enter company name (e.g., Tesla): ").strip()
    run_scraper(company)
