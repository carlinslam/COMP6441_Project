from linkedin_api import Linkedin
import json
import os

# Initialize the LinkedIn API using your li_at cookie only
api = Linkedin(cookie_dict={
    'li_at': 'li_sugr=147c42be-9b64-4273-8fcd-bc118ebdd721; bcookie="v=2&6f9b5543-c892-499c-8749-adc92fd7fbbc"; bscookie="v=1&202301181218157c83ac51-84d6-4c4d-8b0f-1dd09a20462aAQGGatdhP4SaAwewP0v6C2vl1Qcq6k8N"; li_theme=light; li_theme_set=app; aam_uuid=07354309644296683743460957382301983448; VID=V_2024_07_05_03_17754480; li_rm=AQHn2Ruy1Fc11QAAAZCBYDWEqeXfZJ03Ucdrjqnw9cfyyhQqWRjQx_MHMUa1vgN7dap1zCXKeFRbVRrN055V6e3YXZJQUPaUnxMRRQJXQCB2uQAjM9XdK5h2qJb_VCdc-5azcgfePq1MSDfHZ5F58ON2Ec9nXnTyks_icfafdkXRxOERqT7zFOUCaqFKt1_HSyuN5Z6W35K72T2wO3Qu6oVRn7LE03sHhjKF9xlSiuNpP3xoWW5nbYZrp6a6SgS6Y9qAMjwJL-HZD-svaw4eFS9dFhCbimn3DZ88jDq_AyEm_I7SwhqVvUEQ_EzIEciL5RDyEM7RqsqlvFJgc4o; visit=v=1&M; g_state={"i_l":0}; _uetvid=c50549203a8111ef80089bcf15461267; timezone=Australia/Sydney; G_ENABLED_IDPS=google; liap=true; JSESSIONID="ajax:2380764737971379563"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; dfpfpt=884baca3f3f349dc9d49b6fde841a04f; s_cc=true; lil-lang=en_US; li_ep_auth_context=AGxhcHA9bGVhcm5pbmcsYWlkPTIwODc3NDAsaWlkPTYxNTgwNDk3LHBpZD0zMjc5MjAyMzEsZXhwPTE3NTY3MjcwMjQ4MTYsY3VyPXRydWUsc2lkPTE1MDYxNzkwODYsY2lkPTE5OTk1MTg5MzQBrLORGrFKu71Xelqt19ufdHCYQCo; PLAY_LANG=en; lang=v=2&lang=en-US; s_plt=4.45; s_pltp=www.linkedin.com%2Flearning%2Fid-redacted%2Fthe-goals-of-information-security; s_sq=%5B%5BB%5D%5D; s_ips=1064; gpv_pn=www.linkedin.com%2Flearning%2Fid-redacted%2Fquiz%2Furn%3Ali%3AlearningApiAssessment%3Aid-redacted; s_tp=1064; s_ppv=www.linkedin.com%2Flearning%2Fid-redacted%2Fquiz%2Furn%253Ali%253AlearningApiAssessment%253Aid-redacted%2C100%2C100%2C1064%2C1%2C1; s_tslv=1748953517131; _gcl_au=1.1.528342953.1743511917.998413764.1749529948.1749530017; li_at=AQEFAQ8BAAAAABYsq9MAAAGWkJYWzwAAAZekTQtIVgAAsnVybjpsaTplbnRlcnByaXNlQXV0aFRva2VuOmVKeGpaQUFCK2RzMklFcTRlMVU2aUdaZXZlUWlJNGhScm1kekRjeUlQRmJCeDhBTUFLNmdDR3M9XnVybjpsaTplbnRlcnByaXNlUHJvZmlsZToodXJuOmxpOmVudGVycHJpc2VBY2NvdW50OjIwODc3NDAsMzI3OTIwMjMxKV51cm46bGk6bWVtYmVyOjExOTE3MzIyMzclDmCpVHYJCMOxj2gpwuEENZcfemr0hY6hL54yLnlghKOULMt9U71lpeudv08CocQlqVZdPyNV5wYvMvUIoy2pOlFSKK38N0PtielMACNgQ17WwRtXlWeDncFQUO-wvVGE9HGOQ3CmmNCxP9gBbd802T8mbE8GNgXzx29QkQPfy4YROuBg9INd6CKUAD74EPLal40T; AnalyticsSyncHistory=AQLfCe8VNYksUAAAAZeNJv9oeNTaqK2NBJRzjFIllDvfiBO3eCbUeulQC67dt5DcfhqEQzP_fzQl7_6_fGd_gA; lms_ads=AQGq7WPQ6ZdQDAAAAZeNJwEQyBJH1ZIigi6wSq27KJPn1zD1Tn9kuZW97yNhe9dJjEd1aLIjX7i9UKQA-rsRpY6CWB4CrLfw; lms_analytics=AQGq7WPQ6ZdQDAAAAZeNJwEQyBJH1ZIigi6wSq27KJPn1zD1Tn9kuZW97yNhe9dJjEd1aLIjX7i9UKQA-rsRpY6CWB4CrLfw; __cf_bm=etzoja.cDnREwUVhp7Lga0gOGG.neSmIyJZZEndkixs-1750641214-1.0.1.1-_XhoUSOJib7lwcPS0QpAqUBMjbDcgV0OxKz8bYkoiTmOFLw.YR.MPpWCy2Ms2UjaTMEtsDSL01.T3V9NWmJzmPK2lgg_dvrqa9LiUqy3eyk; _guid=cfe1ec55-ab10-453c-8180-4d7f564c253c; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C20263%7CMCMID%7C07914830864122971813515311685048127763%7CMCAAMLH-1751246021%7C11%7CMCAAMB-1751246021%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1750648421s%7CNONE%7CMCCIDH%7C2000779970%7CvVersion%7C5.1.1; fptctx2=taBcrIH61PuCVH7eNCyH0HyAAKgSb15ZEqidLg30r8NE37zMH%252fWcQgiomXclqud%252fHeIC2gQPy0n13xuZ2fIXwQI7e%252bQzrabKcE%252bZUkeYSYgka4w%252fMeUHdJWfjy6nfn5TGYkJE7Iis3TkiqQSLV3NVPUkc4V2JEPvloMa6uBU%252boY9CrZqH398PbqT%252bCQKPAa6pb0aKqEzgGL1AYCyiOojYiNotxwy%252f%252b4I5uTV2VSmA0noWD4Jq%252b1mWYh5c7Z4rn9zc%252beHhcswLLGCufqoC3THESsniiL4u%252ftR%252bElFD%252b7NY%252fyk2JXz%252bxt4OHZJz1tWJMKoobdeDwrVZuNsEJxTV%252fo63QjrCyHvTLh%252bxivsHIDF%252f4A%253d; UserMatchHistory=AQJUWTvn4vtXegAAAZeaXK28PCZjqpmywdWKahFbXLQSGZDfXyhPJYuFEtGVFKKIyrFMvpNwLjqyORlnzlLSntSgP5_EmP1sR27yiIKBpWusgUh6pkPMc2e04FeN4Y4FT5z0TnBejix5nol79ouqKZ7drxHe-Ktp52jylaYwtQJmYo2EOI8dLTGcd7Kvgghcl7zdSLEdUgp91oQpGPNHZQX8bPS8DvYweYhCY0LA9ELxxu-MpeRkbu1BDmiz4PAa2zjJ78AZdrLpW5GL1jet_YHXKIoxr3EV7I5D2hZxltFpIX6VSZP7B59EWW_31BYAGTz8GdI-pOkx9I48YC7Zu1GcsE9b2O6LioKVs3giB4-WyLMdWQ; lidc="b=OB37:s=O:r=O:a=O:p=O:g=4855:u=239:x=1:i=1750641457:t=1750665695:v=2:sig=AQGrkd7eqvjPzc07082I4SdgiF2K3Osi'
})

def extract_profile_info(profile_url):
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
