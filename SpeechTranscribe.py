import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

SMALL_AUDIO: str = "./audio_file.wav"
LARGE_AUDIO: str = "./audio-file-2.wav"


def transcribe_small(audio_file: str, show_output: bool = False):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        if show_output:
            print(text)
    return text


def transcribe_large(audio_file: str, show_output: bool = False, folder_name: str = "audio_chunks"):
    sound_segment = AudioSegment.from_file(audio_file)
    chunks = split_on_silence(
        sound_segment,
        min_silence_len=500,
        silence_thresh=sound_segment.dBFS - 14,
        keep_silence=500
    )

    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    whole_text = ""

    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk_{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        try:
            text = transcribe_small(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error Occured, ->", str(e))
        else:
            text = f"{text.capitalize()}. "
            if show_output:
                print(chunk_filename, ":", text)
            whole_text += text
    return whole_text


if __name__ == "__main__":
    print("Small Transcription", transcribe_small(SMALL_AUDIO))
    print("Large Transcription", transcribe_large(LARGE_AUDIO))
