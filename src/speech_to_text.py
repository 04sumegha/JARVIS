import pvleopard
from config import PICOVOICE_ACCESS_KEY


def transcribe_wav_file(wav_path: str = "command.wav") -> str:
    """Transcribe a WAV file using pvleopard and return full transcript."""

    leopard = pvleopard.create(access_key=PICOVOICE_ACCESS_KEY)
    transcript, words = leopard.process_file(wav_path)

    # Build sentence from word scores
    final_text = " ".join(word.word for word in words).strip()

    leopard.delete()
    return final_text
