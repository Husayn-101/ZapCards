"""
A module to find questions for a given topic from the internet.

This implementation uses the Google Gemini API to generate flashcards.
"""
import json
from typing import List, Dict, Any

import google.generativeai as genai
from google.generativeai.types import generation_types

from config import GEMINI_API_KEY

def find_questions_for_topic(topic: str, count: int = 10, difficulty: str = "Medium") -> Dict[str, Any]:
    """
    Generates a new deck with questions and answers related to a topic.
    Uses the Google Gemini API.

    Args:
        topic: The topic to generate questions for (e.g., "Solar System").
        count: The number of questions to generate.

    Returns:
        A dictionary representing a new deck, or None if it fails.
        Example:
        {
            "name": "Solar System",
            "description": "Auto-generated deck about the Solar System.",
            "cards": [
                {"front": "Which planet is known as the Red Planet?", "back": "Mars"},
                ...
            ]
        }
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: Gemini API key is not configured in config.py.")
        return None

    print(f"Generating {count} questions for topic '{topic}' using Gemini API...")

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # List available models for debugging
        try:
            models = genai.list_models()
            print("Available models:")
            for model_info in models:
                if 'generateContent' in model_info.supported_generation_methods:
                    print(f"  - {model_info.name}")
        except Exception as e:
            print(f"Could not list models: {e}")
        
        model = genai.GenerativeModel('gemini-2.0-flash')

        difficulty_instructions = {
            "Easy": "Make the questions basic and straightforward, suitable for beginners.",
            "Medium": "Make the questions moderately challenging, requiring some knowledge of the topic.",
            "Hard": "Make the questions advanced and detailed, requiring deep understanding of the topic."
        }
        
        prompt = f"""
        You are a helpful assistant that creates study materials.
        Generate a flashcard deck about the topic: "{topic}".
        
        DIFFICULTY LEVEL: {difficulty}
        {difficulty_instructions.get(difficulty, difficulty_instructions["Medium"])}

        The deck should have a creative and relevant name and a short, one-sentence description.
        Create exactly {count} flashcards. Each card must have a "front" (the question) and a "back" (the correct answer).
        Also include 3 plausible but incorrect "distractors" for each question to make good multiple choice questions.

        Provide the output as a single, valid JSON object with the following structure:
        {{
          "name": "Deck Name",
          "description": "Deck description.",
          "cards": [
            {{
              "front": "Question 1", 
              "back": "Correct Answer 1",
              "distractors": ["Wrong Answer A", "Wrong Answer B", "Wrong Answer C"]
            }},
            {{
              "front": "Question 2", 
              "back": "Correct Answer 2",
              "distractors": ["Wrong Answer A", "Wrong Answer B", "Wrong Answer C"]
            }}
          ]
        }}
        Make sure the distractors are plausible but clearly wrong answers related to the topic.
        Do not include any text or formatting outside of this JSON object.
        """

        response = model.generate_content(
            prompt,
            generation_config=generation_types.GenerationConfig(
                # Controls randomness. Lower is more predictable.
                temperature=0.7 
            )
        )

        # Clean up the response to extract only the JSON part
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        print(f"API Response: {cleaned_response[:500]}...")  # Show first 500 chars
        deck_data = json.loads(cleaned_response)
        
        print(f"Parsed deck data: {deck_data}")
        
        # Basic validation
        if "name" in deck_data and "cards" in deck_data:
            print("Successfully generated deck from API.")
            # Check if cards have distractors
            for i, card in enumerate(deck_data["cards"][:3]):  # Check first 3 cards
                print(f"Card {i}: {card}")
            return deck_data
        else:
            print("API response was not in the expected format.")
            return None

    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return None