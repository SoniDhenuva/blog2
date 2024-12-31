import requests

class AI:
    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/text-generation-v1:generateText?key=AIzaSyC6NFPqfHQSACtkt3-gou52RlbbQWOibFo" # ERROR WHOW DO I FIND THE API URL?!

    def get_decision(self, prompt):
        """
        Make a decision based on the prompt using the API.
        prompt: The input text or question that the AI is generating a response for.
        """
        # Prepare the API request with the prompt
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "prompt": {
                "text": prompt  # Ensuring the prompt is passed in the correct format
            },
            "maxOutputTokens": 100  # Adjust based on your needs
        }

        response = self.call_api(data, headers)
        return response

    def call_api(self, data, headers):
        """
        Make the actual API call and return the generated text from the API.
        """
        try:
            response = requests.post(self.api_url, json=data, headers=headers)
            if response.status_code == 200:
                return response.json().get("generatedText", "No generated text found.")
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


# Initialize AI with your API key
ai = AI("RobotAI", "AIzaSyC6NFPqfHQSACtkt3-gou52RlbbQWOibFo")

# Test with a structured prompt
prompt = "How can we improve traffic flow in a busy city?"

decision = ai.get_decision(prompt)
print(f"AI Decision on Traffic Management: {decision}")
