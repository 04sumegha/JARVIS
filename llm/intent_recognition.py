from groq import Groq
import logging
from llm.client import client
from llm.tool_service import tools, names_to_functions

def intent_recognition(prompt):
    SYSTEM_PROMPT = """
        You are a desktop AI assistant.

        You can control the user's computer using tools.
        Your job is to understand the user's command and decide what action should be performed.

        When a user asks to perform an action that matches a tool,
        you must call the correct tool.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        tools=tools,
        tool_choice="auto"
    )

    logging.info(f"LLM response: {response}")
    logging.info(f"LLM response content: {response.choices[0].message.content}")

    msg = response.choices[0].message

    tool_name = msg.tool_calls[0].function.name
    args = msg.tool_calls[0].function.arguments

    function_name = names_to_functions.get(tool_name)

    logging.info(f"Tool to call: {tool_name} with args: {args}")
    return {
        "function": function_name,
        "args": args,
        "tool_name": tool_name
    }