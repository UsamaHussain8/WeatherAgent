from openai import OpenAI
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
import json

load_dotenv()
openai_chat_client = OpenAI()
chat_model = init_chat_model("gpt-5")


SYSTEM_PROMPT = """
    You are a helpful assistant. You can also use tools provided to you to get real-time information.
    For example, if a user asks you about the weather details for their city, you can use the get_weather tool
    to get the current weather details and respond to them accordingly.
    So lets say the user asks "What is the weather like in Islamabad?", you can use the get_weather tool,
    use Islamabad as argument for that tool, call the tool and use the output to generate the response.
"""

def get_weather(city):
    city_str: str = json.loads(city).get('city')
    print(city_str)
    url = f"https://wttr.in/{city_str.lower()}?format=%C+%t" 
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather outlook for {city_str} is: {response.text}"

    return f"Something went wrong when fetching weather details for {city_str}"

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for the city passed in as parameter.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city for which the user wants to know the weather",
                },
            },
            "required": ["city"],
        },
    },
]

def get_response(query: str):
    input_list = [
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": query}
    ]
    response = openai_chat_client.responses.create(
        model="gpt-5",
        input=input_list,
        tools=tools
    )

    # Save function call outputs for subsequent requests
    input_list += response.output

    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_weather":
               # Execute the function logic for get_weather
                weather = get_weather(item.arguments)
                
                # Provide function call results to the model
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                        "city": weather
                    })
                })
    
    print("Final Input: ")
    print(input_list)

    response = openai_chat_client.responses.create(
    model="gpt-5",
    instructions="Respond only with the weather information returned by the tool: get_weather.",
    tools=tools,
    input=input_list,
    )
    return response

def main():
    model_response = get_response("What is the weather like right now in Islamabad, Lahore and Karachi?")
    print("\n\n\nFinal output:")
    # print(model_response.model_dump_json(indent=2))
    print("\n\n" + model_response.output_text)  

if __name__ == "__main__":
    main()
