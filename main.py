from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from openai_tool_caller.openai_caller import get_weather_report

load_dotenv()

chat_model = init_chat_model("gpt-5")

def main():
    model_response = get_weather_report("What is the weather like right now in Islamabad, Seoul, Madrid and Espoo?")
    print("\n\n\nFinal output:")
    # print(model_response.model_dump_json(indent=2))
    print("\n\n" + model_response.output_text)  

if __name__ == "__main__":
    main()
