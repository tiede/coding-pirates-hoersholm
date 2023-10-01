import os
import openai

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# response = openai.Completion.create(
#   model="text-davinci-003",
#   prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI: I'm sorry to hear that. Can you please tell me what subscription you would like to cancel and why? This will help us improve the service in the future.",
#   temperature=0.9,
#   max_tokens=150,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0.6,
#   stop=[" Human:", " AI:"]
# )

# response = openai.Completion.create(
#   model="text-davinci-003",
#   prompt="Help me create a first python program for a 12 year old",
#   temperature=0.9,
#   max_tokens=150,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0.6,
#   stop=[" Human:", " AI:"]
# )

start_message = "How can I help you today?"

messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": start_message},
]

print (start_message)

while(True):
    user_response = input("You: ")
    messages.append({"role": "user", "content": user_response})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    answer = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": answer})
    print (answer)