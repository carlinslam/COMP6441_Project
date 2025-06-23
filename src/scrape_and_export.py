import json
from datetime import datetime
import os

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

def list_profiles():
    return [f for f in os.listdir("profiles") if f.endswith(".json")]

def list_templates():
    return [f for f in os.listdir("prompts") if f.endswith(".txt")]

if __name__ == "__main__":
    print("== LLM Payload Prompt Generator ==")

    # Step 1: Choose a profile
    profiles = list_profiles()
    print("\nAvailable Profiles:")
    for i, p in enumerate(profiles):
        print(f"{i+1}. {p}")
    profile_choice = int(input("Select profile number: ")) - 1
    profile_file = f"profiles/{profiles[profile_choice]}"

    # Step 2: Choose a prompt template
    templates = list_templates()
    print("\nAvailable Prompt Templates:")
    for i, t in enumerate(templates):
        print(f"{i+1}. {t}")
    template_choice = int(input("Select template number: ")) - 1
    template_file = f"prompts/{templates[template_choice]}"

    # Step 3: Input scenario and tone
    scenario = input("\nEnter scenario (e.g., HR policy update, fake invoice): ").strip()
    tone = input("Enter tone (e.g., formal, urgent, friendly): ").strip()

    # Step 4: Generate prompt
    prompt = build_prompt(template_file, profile_file, scenario, tone)

    # Step 5: Save to output file
    profile_name = profiles[profile_choice].replace(".json", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_filename = f"{profile_name}_{scenario.replace(' ', '_')}_{timestamp}.txt"
    output_path = os.path.join("generated_payloads", output_filename)

    with open(output_path, "w") as f:
        f.write("== Prompt to use in ChatGPT ==\n\n")
        f.write(prompt)
        f.write("\n\n== End of prompt ==")

    print(f"\n✅ Prompt saved to: {output_path}")
