import json
import logging

from llm.intent_recognition import intent_recognition
from llm.tool_service import names_to_functions

def run_cli():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print("Type a request (or 'exit' to quit).")

    while True:
        try:
            prompt = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return

        if not prompt:
            continue
        if prompt.lower() in {"exit", "quit"}:
            print("Goodbye.")
            return

        result = intent_recognition(prompt)
        function_name = result.get("function")
        args = result.get("args")

        try:
            parsed_args = json.loads(args) if isinstance(args, str) else args
        except json.JSONDecodeError:
            parsed_args = args

        print(f"Function: {function_name}")
        print(f"Args: {parsed_args}")

        if not function_name:
            print("No function selected.")
            continue

        if parsed_args is None:
            parsed_args = {}

        try:
            if isinstance(parsed_args, dict):
                result_value = function_name(**parsed_args)
            else:
                result_value = function_name(parsed_args)
        except Exception as exc:
            logging.exception("Function execution failed")
            print(f"Function error: {exc}")
            continue

        print(f"Result: {result_value}")


if __name__ == "__main__":
    run_cli()
