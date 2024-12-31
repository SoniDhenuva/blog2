import os
import google.generativeai as genai



api_key = 'AIzaSyC6NFPqfHQSACtkt3-gou52RlbbQWOibFo'  # Replace with your actual API key
genai.configure(api_key=api_key)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-thinking-exp-1219",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

user_input = input("You: ")

response = chat_session.send_message(user_input)



print(response.text)