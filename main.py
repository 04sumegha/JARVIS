import argparse
import json
import logging

from llm.intent_recognition import intent_recognition
from llm.tool_service import names_to_functions
from src.wake_word import run_wake_word_once
from src.speech_to_text import transcribe_wav_file
from src.text_to_speech import speak
from utils.helpers import format_response

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


def run_wake_and_llm(wav_path: str = "command.wav"):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("Wake-word mode: say the keyword to start recording.")
    print("Ctrl+C to exit.")

    try:
        while True:
            captured_audio = run_wake_word_once(output_wav=wav_path)
            print(f"Captured audio bytes: {len(captured_audio)} bytes")

            transcription = transcribe_wav_file(captured_audio)
            print(f"Transcription: {transcription}")

            if transcription:
                response = intent_recognition(transcription)
                function_name = response.get("function")
                args = response.get("args")
                tool_name = response.get("tool_name")

                try:
                    parsed_args = json.loads(args) if isinstance(args, str) else args
                except json.JSONDecodeError:
                    parsed_args = args

                if function_name:
                    if parsed_args is None:
                        parsed_args = {}

                    if isinstance(parsed_args, dict):
                        result_value = function_name(**parsed_args)
                    else:
                        result_value = function_name(parsed_args)

                    print(f"LLM Result: {result_value}")
                    
                    # Speak the formatted response
                    response_text = format_response(tool_name, result_value)
                    print(f"Speaking: {response_text}")
                    speak(response_text)
                else:
                    response_text = "I could not understand that request."
                    print(response_text)
                    speak(response_text)
            else:
                error_msg = "Could not transcribe audio. Please try again."
                print(error_msg)
                speak(error_msg)

    except KeyboardInterrupt:
        print("Exiting wake-word mode.")


def main():
    parser = argparse.ArgumentParser(description="Run JARVIS assistant")
    parser.add_argument("--mode", choices=["wake", "cli"], default="wake", help="Choose 'wake' or 'cli'.")
    parser.add_argument("--wav-path", default="command.wav", help="Path to store recorded command audio.")

    args = parser.parse_args()

    if args.mode == "cli":
        run_cli()
    else:
        run_wake_and_llm(wav_path=args.wav_path)


if __name__ == "__main__":
    main()
