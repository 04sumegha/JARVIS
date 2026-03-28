import pvorca
import sounddevice as sd
import numpy as np
from config import PICOVOICE_ACCESS_KEY


def speak(text: str) -> None:
    orca = pvorca.create(access_key=PICOVOICE_ACCESS_KEY)

    result = orca.synthesize(text=text)

    if isinstance(result, tuple):
        pcm = result[0]   # extract audio
    else:
        pcm = result

    sample_rate = orca.sample_rate

    audio = np.array(pcm, dtype=np.int16)

    sd.play(audio, samplerate=sample_rate)
    sd.wait()

    orca.delete()

def synthesize_to_file(text: str, output_path: str = "output.wav") -> None:
    """Synthesize text to a WAV file using pvorca.
    
    Args:
        text: The text to synthesize.
        output_path: Path where the WAV file will be saved.
    """

    orca = pvorca.create(access_key=PICOVOICE_ACCESS_KEY)
    
    # Synthesize text directly to file
    orca.synthesize_to_file(text=text, output_path=output_path)
    
    orca.delete()
    
    print(f"Audio saved to: {output_path}")

