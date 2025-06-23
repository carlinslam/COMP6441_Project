from linkedin_api import Linkedin
import json
import os

# Initialize the LinkedIn API using your li_at cookie only
api = Linkedin(li_at_cookie="AQEFAQ8BAAAAABYsq9MAAAGWkJYWzwAAAZekTQtIVgAAsnVybjpsaTplbnRlcnByaXNlQXV0aFRva2VuOmVKeGpaQUFCK2RzMklFcTRlMVU2aUdaZXZlUWlJNGhScm1kekRjeUlQRmJCeDhBTUFLNmdDR3M9XnVybjpsaTplbnRlcnByaXNlUHJvZmlsZToodXJuOmxpOmVudGVycHJpc2VBY2NvdW50OjIwODc3NDAsMzI3OTIwMjMxKV51cm46bGk6bWVtYmVyOjExOTE3MzIyMzclDmCpVHYJCMOxj2gpwuEENZcfemr0hY6hL54yLnlghKOULMt9U71lpeudv08CocQlqVZdPyNV5wYvMvUIoy2pOlFSKK38N0PtielMACNgQ17WwRtXlWeDncFQUO-wvVGE9HGOQ3CmmNCxP9gBbd802T8mbE8GNgXzx29QkQPfy4YROuBg9INd6CKUAD74EPLal40T")
    # Extract public identifier from URL
    username = profile_url.strip('/').split('/')[-1]

    profile = api.get_profile(username)

    employee_name = f"{profile.get('firstName', '')} {profile.get('lastName', '')}".strip()
    headline = profile.get("headline", "N/A")
    location = profile.get("geoLocationName", "N/A")

    # Get current company if available
    experiences = profile.get("experience", [])
    company = experiences[0].get("companyName", "N/A") if experiences else "N/A"

    data = {
        "employee_name": employee_name,
        "headline": headline,
        "location": location,
        "linkedin_url": profile_url,
        "company_name": company,
        "public_context": "Recent updates and internal events from company news."
    }

    # Save to profiles folder
    filename = f"profiles/{company.replace(' ', '_')}_{employee_name.replace(' ', '_')}.json"
    os.makedirs("profiles", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n✅ Saved profile to {filename}")
    return data

if __name__ == "__main__":
    profile_link = input("Paste LinkedIn profile URL: ").strip()
    extract_profile_info(profile_link)
