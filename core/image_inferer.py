import requests

from core.image_to_base64_converter import image_to_base64
from core.ingestion_pipe import ingest_data_to_store


class VLLMVisionClient:
    """Client for calling vLLM Vision API endpoint"""

    def __init__(self, base_url="https://s7z2ms3wud6hm6-8000.proxy.runpod.net"):
        self.base_url = base_url.rstrip('/')
        self.endpoint = f"{self.base_url}/v1/chat/completions"

    def chat_with_image_url(self, text_prompt, image_url, model="Qwen/Qwen3-VL-8B-Instruct"):
        """
        Send a chat request with an image URL

        Args:
            text_prompt (str): Text prompt/question about the image
            image_url (str): URL of the image (http/https)
            model (str): Model name

        Returns:
            dict: API response
        """
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            return None

    def chat_with_local_image(self, text_prompt, image_path, model="Qwen/Qwen3-VL-8B-Instruct"):
        """
        Send a chat request with a local image file

        Args:
            text_prompt (str): Text prompt/question about the image
            image_path (str): Path to local image file
            model (str): Model name

        Returns:
            dict: API response
        """
        # Convert image to base64
        image_data_uri = image_to_base64(image_path)

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_data_uri}
                        }
                    ]
                }
            ]
        }

        print(self.endpoint)
        # print(payload)

        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            return None

    def extract_response_text(self, response):
        """Extract the text content from API response"""
        if response and "choices" in response:
            return response["choices"][0]["message"]["content"]
        return None


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = VLLMVisionClient()

    # Example 1: Query with image URL
    # print("Example 1: Using image URL")
    #
    # response = client.chat_with_image_url(
    #     text_prompt="Extract all the information from the image in paragraph manner. No markdown or No markup or no bullet points.",
    #     image_url='your image URL here!'
    # )
    #
    # if response:
    #     text_response = client.extract_response_text(response)
    #     print("Response:", text_response)
    #
    #     # calling ingestion pipeline
    #     ingest_data_to_store(text_response)
    #
    # print("\n" + "=" * 50 + "\n")

    # Example 2: Query with local image
    print("Example 2: Using local image")
    response = client.chat_with_local_image(
        text_prompt="Extract all the information from the image in paragraph manner. No markdown or No markup or no bullet points.",
        image_path='output_images/0000773840-25-000105_page_7.png'
    )

    if response:
        text_response = client.extract_response_text(response)
        print("Response:", text_response)

        # calling ingestion pipeline
        ingest_data_to_store(text_response)

    print("\n" + "=" * 50 + "\n")
