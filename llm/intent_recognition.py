from groq import Groq, BadRequestError
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

    def _request(system_prompt):
        return client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            tools=tools,
            tool_choice="auto",
            temperature=0
        )

    try:
        response = _request(SYSTEM_PROMPT)
    except BadRequestError:
        logging.warning("Tool call validation failed, retrying once with stricter prompt.")
        tool_names = ", ".join(t["function"]["name"] for t in tools)
        strict_prompt = (
            SYSTEM_PROMPT
            + "\nValid tool names (use exactly as shown): "
            + tool_names
            + "\nReturn a tool call only; do not invent tools or change names."
        )
        response = _request(strict_prompt)

    logging.info(f"LLM response: {response}")
    logging.info(f"LLM response content: {response.choices[0].message.content}")

    msg = response.choices[0].message

    if not msg.tool_calls:
        logging.info("No tool calls found in the response.")
        return {
            "message_content": msg.content
        }

    tool_name = msg.tool_calls[0].function.name
    args = msg.tool_calls[0].function.arguments

    function_name = names_to_functions.get(tool_name)

    logging.info(f"Tool to call: {tool_name} with args: {args}")
    return {
        "tool_name": tool_name,
        "function": function_name,
        "args": args
    }