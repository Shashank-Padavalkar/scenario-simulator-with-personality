import json
from google import genai
from google.genai import types
from backend.rag.retrieval import retrieve_context
from backend.models.schemas import ScenarioResponse
from backend.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash-lite"  # Use strong reasoning model since structured output is needed.

system_instruction = """
You are an expert decision analyst. Using the provided context, generate a structured decision simulation for the user's scenario.
Do not hallucinate. If the context is missing, use your general knowledge but prioritize the given context.
Respond ONLY with a valid JSON strictly matching the specified structure. Do not include markdown code block syntax (```json...```).
"""

def simulate_scenario(scenario: str, category: str = None) -> ScenarioResponse:
    # 1. Retrieve context
    context_chunks = retrieve_context(scenario, n_results=3)
    context_text = "\\n\\n".join(context_chunks) if context_chunks else "No specific context found."
    
    # 2. Construct prompt
    prompt = f"""
    Context:
    {context_text}
    
    User Scenario to analyze:
    {scenario}
    
    Category: {category if category else 'General'}
    """
    
    # 3. Call Gemini
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=ScenarioResponse,
                temperature=0.4,
            ),
        )
        
        # Load string as JSON. The model is forced to output JSON matching the schema.
        data = json.loads(response.text)
        return ScenarioResponse(**data)
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        # Fallback in case of parsing errors
        return ScenarioResponse(
            best_case="Error generating response",
            worst_case="Error generating response",
            most_likely=f"An error occurred: {str(e)}",
            risks=["Error"],
            recommendations=["Please check the backend logs and your API key."]
        )
