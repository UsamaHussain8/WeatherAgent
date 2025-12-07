from openai import OpenAI
import json
from tools.func_tools import get_weather
from dotenv import load_dotenv

load_dotenv()
openai_chat_client = OpenAI()

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

SYSTEM_PROMPT = """
    You are a helpful assistant. You can also use tools provided to you to get real-time information.
    For example, if a user asks you about the weather details for their city, you can use the get_weather tool
    to get the current weather details and respond to them accordingly.
    So lets say the user asks "What is the weather like in Islamabad?", you can use the get_weather tool,
    use Islamabad as argument for that tool, call the tool and use the output to generate the response.
"""



def get_weather_report(query: str):
    """
    The get_weather_report function will first call the LLM and the LLM will realize that it needs to make a tool call.
    Once it does that, it returns the entire history (the input and the tool call result). It stops right there.
    For getting the results in a proper format, summarized by the LLM, store all the previous inputs and the responses.
    Then provide all that context to the LLM in another LLM call. 
    For this reason its crucial to store the previous exchange, otherwise it will return error when finding previous call and its response.
    The previous context can be stored by specifying store parameter in the create function as True (default val)
    """
    input_list = [
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": query}
    ]
    tool_response = openai_chat_client.responses.create(
        model="gpt-5",
        input=input_list,
        tools=tools,
        store=True
    )

    # Save function call outputs for subsequent requests
    input_list += tool_response.output

    for item in tool_response.output:
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

    model_tool_response = openai_chat_client.responses.create(
    model="gpt-5",
    instructions="Respond only with the weather information returned by the tool: get_weather.",
    tools=tools,
    input=input_list,
    )
    return model_tool_response