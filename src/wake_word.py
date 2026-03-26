import pvporcupine
from pvrecorder import PvRecorder
import os
import wave
import time
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

SILENCE_THRESHOLD = 500
SILENCE_DURATION = 4  # seconds
SAMPLE_RATE = 16000


def is_silent(pcm):
    return max(abs(x) for x in pcm) < SILENCE_THRESHOLD


def record_command(recorder):
    print("Listening for command...")

    audio_frames = []
    silence_start = None

    while True:
        pcm = recorder.read()
        audio_frames.extend(pcm)

        if is_silent(pcm):
            if silence_start is None:
                silence_start = time.time()

            elif time.time() - silence_start > SILENCE_DURATION:
                print("Silence detected, stopping recording")
                break
        else:
            silence_start = None

    return audio_frames


def frames_to_pcm_bytes(audio_frames):
    return b"".join(int(x).to_bytes(2, 'little', signed=True) for x in audio_frames)


def save_audio(audio_frames, filename="command.wav"):
    import wave

    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(frames_to_pcm_bytes(audio_frames))

    print("Audio saved:", filename)


def invoke_assistant(recorder):
    print("Assistant activated!")

    audio_frames = record_command(recorder)
    save_audio(audio_frames, filename="command.wav")

    return frames_to_pcm_bytes(audio_frames)


def run_wake_word_once(output_wav="command.wav"):
    from config import PICOVOICE_ACCESS_KEY

    keyword_path = os.path.join(os.path.dirname(__file__), "../models", "Jarvis.ppn")

    ppn = pvporcupine.create(access_key=PICOVOICE_ACCESS_KEY, keyword_paths=[keyword_path])
    recorder = PvRecorder(device_index=-1, frame_length=ppn.frame_length)

    try:
        recorder.start()
        print("Listening for wake words...")

        while True:
            pcm = recorder.read()
            keyword_index = ppn.process(pcm)

            if keyword_index >= 0:
                print("Wake word Hey Jarvis detected!")
                audio_frames = record_command(recorder)
                save_audio(audio_frames, filename=output_wav)
                return output_wav

    finally:
        recorder.stop()
        recorder.delete()
        ppn.delete()