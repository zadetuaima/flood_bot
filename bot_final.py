from openai import AzureOpenAI
import os
import json
import urllib

client = AzureOpenAI(
    api_key=os.getenv("AZURE_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version="2023-10-01-preview"
)

#initial chat input message
messages = [
    {"role": "user", "content": "How many flood warnings are there in wiltshire?"}
]

def get_flood_data(area_name):
    url = "https://environment.data.gov.uk/flood-monitoring/id/floods"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    flood_data = json.loads(response.read())
    if 'items' in flood_data:
        county_areas = [
            item for item in flood_data['items'] if 'floodArea' in item and isinstance(item['floodArea'].get('county'), str) and area_name.lower() in item['floodArea']['county'].lower()]
        flood_warning_count = sum(1 for item in county_areas if item.get('severity', '').lower() == 'flood warning')
        flood_alert_count = sum(1 for item in county_areas if item.get('severity', '').lower() == 'flood alert')
        return f"There are {flood_warning_count} flood warnings and {flood_alert_count} flood alerts in {area_name}."


functions = [
    {
        "type": "function",
        "function": {
            "name": "get_flood_data",
            "description": "Gets flood warning and alert count for a specific area",
            "parameters": {
                "type": "object",
                "properties": {
                    "area_name": {
                        "type": "string",
                        "description": "The name of the area where there might be flood warnings or alerts"
                    }
                },
                "required": ["area_name"]
            }
        }
    }
]

#This is the initial chat completion request, where it send the user message and function description to the gpt
#bascially routes all the info above to the openAI API so it can get an answer
response = client.chat.completions.create(
    model = "GPT-4",
    messages = messages,
    tools = functions,
    #auto means chatgpt decides when it wants to call this function
    tool_choice = "auto"
)

#response_message is the initial response of the GPT
response_message = response.choices[0].message
#gpt_tools determines if the GPT needs external data
gpt_tools = response.choices[0].message.tool_calls


if gpt_tools:
    messages.append(response_message)

    for gpt_tool in gpt_tools:
        function_name = gpt_tool.function.name
        if function_name == "get_flood_data":
            function_parameters = json.loads(gpt_tool.function.arguments)
            area_name = function_parameters.get("area_name")
            function_response = get_flood_data(area_name)

            #this appends the tool response to the convo
            messages.append(
                {
                    "tool_call_id": gpt_tool.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                }
            )

            #then this requests a follow-up response from the GPT
            second_response = client.chat.completions.create(
                model="GPT-4",
                messages=messages
            )
            print(second_response.choices[0].message.content)
#and if the GPT doesn't need any tools, i.e. if the initial question doesnt relate to crypto in this case it will just print a repsonse as normal
else:
    print(response.choices[0].message.content)
