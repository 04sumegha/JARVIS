from groq import Groq, BadRequestError
import logging
import re
from llm.client import client
from llm.tool_service import tools, names_to_functions

SPECIAL_FOLDERS = {
    "desktop": "shell:Desktop",
    "downloads": "shell:Downloads",
    "documents": "shell:Documents",
    "pictures": "shell:Pictures",
    "videos": "shell:Videos",
    "music": "shell:Music",
    "screenshots": "shell:Screenshots",
}

def _match_open_special_folder(prompt: str) -> str | None:
    text = prompt.strip().lower()
    match = re.match(r"^open\s+(the\s+)?(.+)$", text)
    if not match:
        return None
    target = match.group(2)
    target = re.sub(r"\b(folder|dir|directory)\b", "", target).strip()
    return SPECIAL_FOLDERS.get(target)

def intent_recognition(prompt):
    SYSTEM_PROMPT = """
        You are a desktop AI assistant.

        You can control the user's computer using tools.
        Your job is to understand the user's command and decide what action should be performed.

        When a user asks to perform an action that matches a tool,
        you must call the correct tool.

        When calling the open_app tool:
        - Always return a valid Windows command usable with `start`
        - Convert natural language to executable names
        - Examples:
        - "vs code" → "code"
        - "visual studio code" → "code"
        - "file explorer" → "explorer"
        - "downloads folder" → "shell:Downloads"
        - "screenshots folder" → "shell:Screenshots"
        - Do NOT return conversational names

        When calling the close_app tool:
        - Always return a valid Windows image name (usually ends in .exe)
        - Examples:
        - "close chrome" → "chrome.exe"
        - "close visual studio code" → "code.exe"
        - "close notepad" → "notepad.exe"
        - IMPORTANT: Never attempt to close system-critical processes like "explorer.exe", "taskmgr.exe", or system drivers.
        - If the user asks to close "file explorer", do NOT call close_app with "explorer.exe". Instead, respond that you cannot close the desktop shell.

        Use tool calls only; do not output tool calls or JSON in the message content.

        When calling a tool, the arguments must be valid JSON with double quotes.
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

    special_folder = _match_open_special_folder(prompt)
    if special_folder:
        logging.info("Matched special folder open request.")
        return {
            "tool_name": "open_app",
            "function": names_to_functions.get("open_app"),
            "args": {"app_name": special_folder},
        }

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
            + "\nUse valid JSON for tool arguments. Do not add extra text."
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