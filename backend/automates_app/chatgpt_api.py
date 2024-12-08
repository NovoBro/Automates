# backend/automates_app/chatgpt_api.py

import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("CHAT_GPT_API_KEY")


class ChatGPTAPI:
    def generateDescription(self, description, audience, style, tone, hashtags):
        try:
            # Create a prompt string based on input data
            prompt = f"""
            You are a post creator for LinkedIn. Based on the provided input, generate a detailed LinkedIn post.
            Description: {description}
            Audience: {audience}
            Style: {style}
            Tone: {tone}
            Hashtags: {hashtags}
            """

            # Corrected method to use `ChatCompletion.create` for newer OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use gpt-4 or gpt-3.5-turbo if preferred
                messages=[
                    {"role": "system", "content": "You are a post creator for LinkedIn."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )

            # Extract the generated description from the response
            generated_description = response['choices'][0]['message']['content'].strip()

            return generated_description

        except Exception as e:
            # Handle any errors that occur and return the exception message
            return f"Error: {str(e)}"