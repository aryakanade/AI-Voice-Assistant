import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey  # Ensure you have your API key set in a config file
import datetime
import pyttsx3

engine = pyttsx3.init()
chatStr = ""


def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"User: {query}\nAura: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response_text = response["choices"][0]["text"].strip()
    engine.say(response_text)
    engine.runAndWait()
    chatStr += f"{response_text}\n"
    return response_text


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt}\n*************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response_text = response["choices"][0]["text"]
    text += response_text

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

    engine.say(response_text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(e)
            return "Some Error Occurred. Sorry from Aura"


if __name__ == '__main__':
    print('Welcome to Aura A I')
    engine.say("Welcome to Aura A I")
    engine.runAndWait()
    while True:
        query = takeCommand().lower()

        # List of sites
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"]
        ]

        for site in sites:
            if f"open {site[0]}" in query:
                engine.say(f"Opening {site[0]} sir...")
                engine.runAndWait()
                webbrowser.open(site[1])

        if "open music" in query:
            musicPath = "C:\\Path\\To\\Your\\MusicFile.mp3"  # Replace with the actual path to your music file
            os.system(f'start {musicPath}')

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            engine.say(f"Sir, the time is {hour} hours and {minute} minutes")
            engine.runAndWait()

        elif "open facetime" in query:
            os.system("start Facetime")  # Adjust if needed for Windows or macOS specifics

        elif "open pass" in query:
            os.system("start Passky")  # Adjust if needed for Windows or macOS specifics

        elif "using artificial intelligence" in query:
            ai(prompt=query)

        elif "aura quit" in query:
            engine.say("Goodbye, sir!")
            engine.runAndWait()
            exit()

        elif "reset chat" in query:
            chatStr = ""
            engine.say("Chat history reset")
            engine.runAndWait()

        else:
            response = chat(query)
            print(response)
