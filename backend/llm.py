from openai import OpenAI
import dotenv 

# Obtain environment variables
env_vars = dotenv.dotenv_values()
API_KEY = env_vars['OPENAI_API_KEY']
SYSTEM_PROMPT = env_vars['CHAT_SYSTEM_PROMPT']

# Client to send requests to OpenAI API
client = OpenAI(
  api_key=API_KEY
)

'''
    Defines a method to send a prompt to an OpenAI LLM. The LLM responds in-character as LeBron James (but in the context of being a therapist).
'''
def get_response(prompt: str):
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=False,
    messages=[
        {
            "role": "developer", 
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    )

    return completion

if __name__ == "__main__":
    prompt = "I've been feeling a bit down about school lately. What should I do?"
    response = get_response(prompt=prompt)
    message = response.choices[0].message.content
    chat_id = response.id

    print("Chat ID:", chat_id)
    print("Chat response:", message)
    