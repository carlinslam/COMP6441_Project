import json
from datetime import datetime

def build_prompt(template_path, profile_path, scenario, tone):
    with open(template_path, 'r') as f:
        template = f.read()
    with open(profile_path, 'r') as f:
        profile = json.load(f)

    prompt = template.format(
        company_name=profile["company_name"],
        employee_name=profile["employee_name"],
        public_context=profile["public_context"],
        scenario=scenario,
        tone=tone
    )
    return prompt

if __name__ == "__main__":
    # CONFIGURATION — adjust for any target
    template_file = "prompts/phishing_invoice_template.txt"
    profile_file = "profiles/airbnb.json"
    scenario = "Fake invoice from a new vendor"
    tone = "Urgent"

    # Generate and save prompt
    prompt = build_prompt(template_file, profile_file, scenario, tone)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_file = f"generated_payloads/airbnb_invoice_{timestamp}.txt"
    with open(output_file, 'w') as f:
        f.write("== Prompt to use in ChatGPT ==\n\n")
        f.write(prompt)
        f.write("\n\n== End of prompt ==")

    print(f"✅ Prompt written to {output_file}")

