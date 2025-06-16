# llm_payload_generator
# LLM-Augmented Social Engineering Payload Generator

This is a red team tool that uses prompt engineering and public data to generate realistic phishing payloads with ChatGPT.

⚠️ Educational use only — DO NOT use without written consent from the target.

## How It Works

1. Define a company profile in `/profiles`
2. Choose a scenario and tone
3. Use a prompt template from `/prompts`
4. Run the script to generate a prompt file
5. Copy/paste the output into [ChatGPT](https://chat.openai.com)

## Example Usage

```bash
python src/generator.py
