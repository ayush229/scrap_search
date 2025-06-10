import requests
import json

class LLMInteraction:
    def __init__(self, api_key: str, model: str = "llama3-70b-8192", base_url: str = "https://api.groq.com/openai/v1/chat/completions"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_ai_response(self, user_query: str, context: str):
        """
        Sends the user query and matched context to the LLAMA API
        and returns the beautified response.
        """
        # Construct the prompt to ensure the AI strictly uses the provided context
        prompt = f"""
You are an AI assistant. Your task is to answer the user's query STRICTLY based on the provided context.
If the answer cannot be found in the context, please state that explicitly and do not make up information.

Context:
{context}

User Query:
{user_query}

Answer:
"""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1, # Keep temperature low for factual responses based on context
            "max_tokens": 500 # Adjust as needed
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status() # Raise an exception for HTTP errors
            
            response_json = response.json()
            if "choices" in response_json and len(response_json["choices"]) > 0:
                return response_json["choices"][0]["message"]["content"].strip()
            else:
                return "No response from AI."

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Groq API: {e}")
            return "Error communicating with AI service."
        except json.JSONDecodeError:
            print(f"Failed to decode JSON response from Groq API: {response.text}")
            return "Error processing AI response."
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred with AI interaction."