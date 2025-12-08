from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from openai_tool_caller.openai_caller import get_weather_report, SYSTEM_PROMPT
from tools.func_tools import get_weather_tool

load_dotenv()

chat_model = init_chat_model("gpt-5")


SYSTEM_PROMPT = """
    You are a helpful assistant. You can also use tools provided to you to get real-time information.
    For example, if a user asks you about the weather details for their city, you can use the get_weather tool
    to get the current weather details and respond to them accordingly.
    So lets say the user asks "What is the weather like in Islamabad?", you can use the get_weather tool,
    use Islamabad as argument for that tool, call the tool and use the output to generate the response.
    Return only the final output and not all the steps you followed.
"""

def main():
    query = "What is the weather like right now in Islamabad, Seoul, Madrid and Espoo?"
    #model_response = get_weather_report("What is the weather like right now in Islamabad, Seoul, Madrid and Espoo?")
    #print("\n\n\nFinal output:")
    #print("\n\n" + model_response.output_text)  

    # create an agent
    weather_agent = create_agent(
        model=chat_model,
        tools=[get_weather_tool],
        system_prompt=SYSTEM_PROMPT 
    )
    result = weather_agent.invoke(
        {
            "messages": [
                {'role': "user", "content": query}
            ]
        }
    )
    print(result['messages'][-1].content)

if __name__ == "__main__":
    main()
