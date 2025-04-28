from gpt_pilot.core.llm.openai_client import OpenAIClient

client = OpenAIClient()

print("💬 What do you want to build?")
prompt = input("> ")

response = client(prompt)
print("\n🧠 GPT Pilot says:\n", response)
