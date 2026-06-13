import asyncio
import os
from google import genai
from google.genai import types
import speech_recognition as sr

MODEL = "gemini-3.1-flash-live-preview"


def record_audio(timeout: float = 5.0, phrase_time_limit: float = 15.0) -> bytes:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1.0)
        print("Listening...")
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    pcm_bytes = audio.get_raw_data(convert_rate=16000, convert_width=2)
    return pcm_bytes


async def transcribe_with_gemini(audio_data: bytes) -> str:
    client = genai.Client()
    transcript = ""

    connect_config = {
        "response_modalities": ["TEXT"],
    }

    async with client.aio.live.connect(model=MODEL, config=connect_config) as session:
        await session.send_realtime_input(
            audio=types.Blob(data=audio_data, mime_type="audio/pcm;rate=16000")
        )
        await session.send_realtime_input(audio_stream_end=True)

        async for msg in session.receive():
            if getattr(msg, "text", None) is not None:
                print(msg.text, end="", flush=True)
                transcript += msg.text
            if getattr(msg, "turn_complete", False):
                break

    print()
    return transcript


def stt():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY in your environment before running.")
        return

    try:
        audio_bytes = record_audio()
        print("Sending audio to Gemini for transcription...")
        transcript = asyncio.run(transcribe_with_gemini(audio_bytes))
        print("Transcription result:", transcript)
    except Exception as exc:
        print("Error during transcription:", exc)


if __name__ == "__main__":
    stt()
