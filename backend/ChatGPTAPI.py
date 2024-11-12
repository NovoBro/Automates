import models
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatGPTAPI():
  def generateDescription(draft):
    return draft.getUserDescription()
    try:
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            max_tokens=150, 
            temperature=0.7, 
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

