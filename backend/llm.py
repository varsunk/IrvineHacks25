from openai import OpenAI
from openai.types.chat import ChatCompletion
import dotenv 

# Obtain environment variables
env_vars = dotenv.dotenv_values()
API_KEY = env_vars['OPENAI_API_KEY']
SYSTEM_PROMPT = env_vars['CHAT_SYSTEM_PROMPT']
CONV_HISTORY_LIMIT = int(env_vars['CONVERSATION_HISTORY_MSG_LIMIT'])

# Client to send requests to OpenAI API
client = OpenAI(
  api_key=API_KEY
)

'''
    Defines a method to send chat history and a prompt to an OpenAI LLM. The LLM responds in-character as LeBron James (but in the context of being a therapist).
'''
def get_response(history: list[dict[str, str]], prompt: str) -> ChatCompletion:
    # TODO: optionally protect against prompts that cause the LLM to not respond to messages?
    
    messages = construct_chat_history(history, prompt)

    # testing
    # for msg in messages:
    #     print(msg)
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=False,
        messages=messages
    )

    response = completion.choices[0].message.content
    hist_record = [
        {
            "role": "user",
            "content": prompt
        },
        {
            "role": "assistant",
            "content": response
        }
    ]

    return response, hist_record

'''
    Defines a method to construct chat history to feed into LLM, accounting for our conversation message limit
'''
def construct_chat_history(history: list[dict[str, str]], prompt: str):
    messages = []
    messages.append({
        "role": "developer",
        "content": SYSTEM_PROMPT
    })
    messages += [msg for msg in history[-CONV_HISTORY_LIMIT*2:]]
    messages.append({
        "role": "user",
        "content": prompt
    })

    return messages


# testing purposes
# if __name__ == "__main__":
#     prompt = "I've been feeling a bit down about school lately. What should I do?"
#     response, hist_record = get_response(history=[], prompt=prompt)

#     print()
#     print("Chat response:", response)
#     print()
#     print("Hist record:")
#     for msg in hist_record:
#         print(msg)

    # # test history generation
    # hist = []
    # for i in range(10):
    #     messages = construct_chat_history(history=hist, prompt=prompt)
    #     hist += [
    #         {
    #             "role": "user",
    #             "content": prompt
    #         },
    #         {
    #             "role": "assistant",
    #             "content": response
    #         }
    #     ]
    #     print(f"Messages (#{i} loop):\n")
    #     for msg in messages:
    #         print(msg)