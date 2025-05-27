# from dotenv import load_dotenv
# load_dotenv()

# from google import genai
# import os

# # Initialize client with your API key
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# # Send a request to the Gemini model
# response = client.models.generate_content(
#     model="gemini-2.0-flash", 
#     contents="Explain how AI works in a few words"
# )

# # Output the response
# print(response.text)

from src.pdf import process_pdf
from src.scanner import process_cover_letter

if __name__ == "__main__":
    file_path = "example.pdf"
    try:
        content = process_pdf(file_path)
        print("✅ Extracted Text:\n", content)

        redacted, skills = process_cover_letter(content)

        print("\n🔒 Redacted Cover Letter:\n", redacted)
        print("\n🧠 Extracted Skills:\n", skills)

    except Exception as e:
        print("❌ Error:", e)

