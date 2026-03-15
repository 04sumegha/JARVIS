import pvporcupine
from pvrecorder import PvRecorder
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def invoke_assistant():
    print("Assistant activated!")
    # TODO: start speech recognition here

access_key = os.getenv('PICOVOICE_ACCESS_KEY')
if not access_key:
    raise ValueError("PICOVOICE_ACCESS_KEY environment variable is not set")

ppn = pvporcupine.create(
    access_key=access_key,
    keyword_paths=[os.path.join(os.path.dirname(__file__), 'Jarvis.ppn')]
)

recorder = PvRecorder(device_index=-1, frame_length=ppn.frame_length)

try:
    recorder.start()
    print("Listening for wake words...")

    while True:
        pcm = recorder.read()
        keyword_index = ppn.process(pcm)

        if keyword_index >= 0:
            print("Wake word Hey Jarvis! detected!")
            invoke_assistant()

except KeyboardInterrupt:
    print("Stopping...")

finally:
    recorder.stop()
    recorder.delete()
    ppn.delete()