from google import genai
from openai import OpenAI
import whisper
import os
import speech_recognition as sr
from gtts import gTTS
import pygame

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
genai_client = genai.Client()
local_model = whisper.load_model("base")
model="gemini-3-flash-preview"
r = sr.Recognizer()
r.pause_threshold = 1.5


#microphone input here to continue
def stt():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1.0)
        print("lising...")

        #audio = r.listen(source)
        #command = r.recognize_google(audio, language='zh-TW')
        #print("you say:", command)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            with open("temp_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())

            print("whisper recognizing...")
            #with open("temp_audio.mp3", "rb") as audio_f:
            #    transcription = openai_client.audio.transcriptions.create(
            #        model="whisper-1",
            #        file=audio_f,
            #        language="zh"
            #    )
            #user_input = transcription.text
            result = local_model.transcribe("temp_audio.wav", fp16=False, language="zh", beam_size=1)
            command = result["text"]
            print("you say:",command)

            #return command

            print("response:",end="",flush=True)
            #initialization
            response_text = ""
            response = genai_client.models.generate_content_stream(
                model=model,
                #config=types.GenerateContentConfig(
                #    system_instruction="這是一段語音辨識文字，可能包含中英夾雜或輕微誤聽", #這邊引導gemini的行為
                #)
                contents=command
            )

            for chunk in response:
                print(chunk.text, end="", flush=True)
                response_text += chunk.text
        except Exception as e:
            print("發生問題",e)


if __name__ == "__main__":
    stt()
