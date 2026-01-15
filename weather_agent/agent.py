from openai import OpenAI
from dotenv import load_dotenv
import json
import requests

load_dotenv()

client = OpenAI()
def get_weather(city: str):
    url= f"https://wttr.in/{city.lower()}?format=%C+%t"
    response= requests.get(url)
    
    if response.status_code== 200:
        return f"The weather in : { city } is {response.text}"
    
    return "Something went wrong while fetching the data" 

available_tools = {
   "get_weather": get_weather
}

SYSTEM_PROMPT="""
        You are an expert AI assistant in resolving user queries chain of thought.
        You work on START, PLAN and OUTPUT steps.
        You need to first PLAN what needs to ben done. The PLAN can be multiple steps.
        Once you think enough PLAN has been done, finally you can give an OUTPUT.
        You can also call a tool if required if required from the list of available tools.
        for evey tool call wait for the observe step which is the output from the called tool.

        Rules: 
        - Strictly Follow the given JSON output format
        - Only run one step at a time.
        - The sequence of steps is START (where user gives an input), PLAN(That can be multiple times) and finally OUTPUT (which is going to the displayed to the user)
        
        
        Output JSON Format:
        {"step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content":"string", "tool": "string", "input": "string"}
    
        Available Tools:
        - get_weather: Takes the city name as an input string and returns the weather of the city.
            
    
        Example 1:
        START: Hey, Can you solve 2+ 3 * 5 / 10
        PLAN: { "step":"PLAN" : "content": "seems like the user is interested in math problem"}
        PLAN: { "step":"PLAN" : "content": "looking at the problem, we should solve this using BODMAS method"}
        PLAN: { "step":"PLAN" : "content": "Yes, The BODMAS is correct thing to be done here"}
        PLAN: { "step":"PLAN" : "content": "first we must multiply 3 * 5 which is 15"}
        PLAN: { "step":"PLAN" : "content": "Now the new equation is 2 + 14 / 10"}
        PLAN: { "step":"PLAN" : "content": "We must perform divide that is 15 / 10"}
        PLAN: { "step":"PLAN" : "content": "Now the new equation is 2 + 1.5"}
        PLAN: { "step":"PLAN" : "content": "Now finally lets perform the add 3.5"}
        PLAN: { "step":"PLAN" : "content": "Great, we have solved and finally left with 3.5 as ans"}
        OUTPUT:{ "step":"OUTPUT" : "content" : "3.5"}

        
        Example 2:
        START: Hey, What is the weather of Delhi?
        PLAN: { "step":"PLAN" : "content": "seems like the user is interested in getting the weather information of Delhi in india."}
        PLAN: { "step":"PLAN" : "content": "Lets see if we have available tools from the list of available tools"}
        PLAN: { "step":"PLAN" : "content": "Great, we have get_weather tool available for this query."}
        PLAN: { "step":"PLAN" : "content": "I need to call get_weather tool for delhi as input for city "}
        PLAN: { "step":"TOOL" : "tool":" get_weather", "input" : "delhi"} 
        PLAN: { "step":"OBSERVE" : "tool":" get_weather", "output" : "The temperature of delhi is cloudy with 20 celsius "} 
        PLAN: { "step":"PLAN" : "content": "Great, I got the weather info about delhi"}
        OUTPUT:{ "step":"OUTPUT" : "content" : "The current weather in delhi is 20 C with some clouds. }

    """
    
print("\n\n\n\n")
message_history =[
    { "role":"system", "content": SYSTEM_PROMPT },
]

user_query = input("👍🏼")
message_history.append({"role":"user","content":user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format= {"type": "json_object"},
        messages=message_history
    )
    
    raw_result =(response.choices[0].message.content)
    message_history.append({"role":"assistant", "content": raw_result})
    
    parsed_result = json.loads(raw_result)
    
    if  parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "TOOL":
        tool_to_call = parsed_result.get("tool")
        tool_input = parsed_result.get("input")
        print(f" 🔨: {tool_to_call}({tool_input})")
        
        tool_response = available_tools[tool_to_call](tool_input)
        print(f"🔨: {tool_to_call}({tool_input}) = {tool_response}")
        message_history.append ({ "role": "developer", "content": json.dumps( { "step" : "OBSERVE", "tool": tool_to_call ,     "input": tool_input , "output": tool_response } ) })
        continue
        
    if parsed_result.get("step") == "PLAN":
        print("💭", parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "OUTPUT":
        print("🤖", parsed_result.get("content"))
        break
print("\n\n\n\n")
