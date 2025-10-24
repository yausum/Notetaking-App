"""
LLM Integration Module
Provides functions to interact with OpenAI API for note enhancement
"""
# Import libraries
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


token = os.environ.get("GITHUB_TOKEN")
endpoint = os.environ.get("OPENAI_ENDPOINT", "https://models.github.ai/inference")
model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

# A function to call an LLM model and return the response
def call_llm_model(messages, temperature=1.0, top_p=1.0, model_name=None):
    """
    Call the LLM model with given messages and parameters.
    
    Args:
        messages (list): List of message dictionaries with 'role' and 'content'
        temperature (float): Sampling temperature (0-2). Higher = more random
        top_p (float): Nucleus sampling parameter (0-1)
        model_name (str): Optional model override
        
    Returns:
        str: The model's response content
    """
    if not token:
        raise ValueError("API token not found. Please set GITHUB_TOKEN or OPENAI_API_KEY in .env file")
    
    client = OpenAI(base_url=endpoint, api_key=token)
    
    response = client.chat.completions.create(
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        model=model_name or model
    )
    
    return response.choices[0].message.content


# A function to translate to target language
def translate_text(text, target_language="Chinese"):
    """
    Translate text to target language using LLM.
    
    Args:
        text (str): Text to translate
        target_language (str): Target language (default: Chinese)
        
    Returns:
        str: Translated text
    """
    messages = [
        {
            "role": "system",
            "content": f"You are a professional translator. Translate the following text to {target_language}. Only return the translated text, no explanations."
        },
        {
            "role": "user",
            "content": text
        }
    ]
    
    return call_llm_model(messages, temperature=0.3)


# A function to summarize note content
def summarize_note(content, max_length=100):
    """
    Generate a concise summary of note content.
    
    Args:
        content (str): Note content to summarize
        max_length (int): Maximum length of summary in words
        
    Returns:
        str: Summary of the note
    """
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant that creates concise summaries. Summarize the following text in no more than {max_length} words."
        },
        {
            "role": "user",
            "content": content
        }
    ]
    
    return call_llm_model(messages, temperature=0.5)


# A function to generate tags from note content
def generate_tags(title, content, max_tags=5):
    """
    Automatically generate relevant tags for a note.
    
    Args:
        title (str): Note title
        content (str): Note content
        max_tags (int): Maximum number of tags to generate
        
    Returns:
        str: Comma-separated tags
    """
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant that generates relevant tags. Based on the title and content, generate up to {max_tags} relevant tags. Return only the tags separated by commas, no explanations."
        },
        {
            "role": "user",
            "content": f"Title: {title}\n\nContent: {content}"
        }
    ]
    
    return call_llm_model(messages, temperature=0.7)


# A function to improve note content
def improve_note(content):
    """
    Improve and enhance note content with better formatting and clarity.
    
    Args:
        content (str): Original note content
        
    Returns:
        str: Improved note content
    """
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that improves note content. Make the text clearer, better organized, and more readable while preserving the original meaning and information. Fix grammar and spelling errors."
        },
        {
            "role": "user",
            "content": content
        }
    ]
    
    return call_llm_model(messages, temperature=0.5)


# A function to answer questions about notes
def ask_about_note(note_content, question):
    """
    Answer questions about a specific note using LLM.
    
    Args:
        note_content (str): The content of the note
        question (str): The question to ask
        
    Returns:
        str: Answer to the question
    """
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that answers questions about notes. Provide clear and concise answers based on the note content provided."
        },
        {
            "role": "user",
            "content": f"Note content:\n{note_content}\n\nQuestion: {question}"
        }
    ]
    
    return call_llm_model(messages, temperature=0.7)


# Run the main function if this script is executed
if __name__ == "__main__":
    print("="*50)
    print("LLM Integration Test")
    print("="*50)
    
    # Check if API token is configured
    if not token:
        print("❌ Error: API token not found!")
        print("Please create a .env file with GITHUB_TOKEN or OPENAI_API_KEY")
        exit(1)
    
    print(f"✓ API token found")
    print(f"✓ Endpoint: {endpoint}")
    print(f"✓ Model: {model}")
    print()
    
    # Test translation
    print("Testing translation...")
    try:
        test_text = "Hello, this is a test note."
        translated = translate_text(test_text, "Chinese")
        print(f"Original: {test_text}")
        print(f"Translated: {translated}")
        print("✓ Translation test passed")
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
    
    print()
    
    # Test summarization
    print("Testing summarization...")
    try:
        test_content = "This is a long note about Python programming. Python is a versatile language used for web development, data science, automation, and more. It has a clean syntax and a large ecosystem of libraries."
        summary = summarize_note(test_content, max_length=20)
        print(f"Original: {test_content}")
        print(f"Summary: {summary}")
        print("✓ Summarization test passed")
    except Exception as e:
        print(f"❌ Summarization test failed: {e}")
    
    print()
    
    # Test tag generation
    print("Testing tag generation...")
    try:
        tags = generate_tags("Python Tutorial", "Learn Python programming basics", max_tags=3)
        print(f"Generated tags: {tags}")
        print("✓ Tag generation test passed")
    except Exception as e:
        print(f"❌ Tag generation test failed: {e}")
    
    print()
    print("="*50)
    print("All tests completed!")
    print("="*50)
