import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import wmi
import ctypes

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    """Use text-to-speech to say the given audio string."""
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    """Greet the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!!!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!!!")
    else:
        speak("Good Evening!!!")
    speak("I am Shinchan. How can I make your day better?")

def take_command():
    """Capture and recognize speech from the microphone."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, I did not catch that. Could you please repeat?")
        return "None"
    return query.lower()

def adjust_brightness(level):
    """Adjust the screen brightness (Windows only)."""
    if 0 <= level <= 100:
        try:
            wmi_interface = wmi.WMI(namespace='wmi')
            brightness = wmi_interface.WmiMonitorBrightnessMethods()[0]
            brightness.WmiSetBrightness(level, 0)
            speak(f"Brightness set to {level} percent.")
        except Exception as e:
            speak(f"Failed to set brightness. Error: {e}")
    else:
        speak("Brightness level should be between 0 and 100.")

def read_local_file(filepath):
    """Read the contents of a local file."""
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    else:
        return "File not found."

def write_local_file(filepath, content):
    """Write content to a local file."""
    with open(filepath, 'w') as file:
        file.write(content)
    return "File written successfully."

def list_files_in_directory(directory):
    """List all files in a specified directory."""
    if os.path.isdir(directory):
        files = os.listdir(directory)
        return files
    else:
        return "Directory not found."

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results for that query. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I could not find any results for that query.")
        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://google.com")
        elif 'hi shinchan' in query:
            speak("Hi! I am Shinchan. How is your day?")
        elif 'open stack overflow' in query:
            webbrowser.open("https://stackoverflow.com")
        elif 'play music' in query:
            music_url = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
            webbrowser.open(music_url)
        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Dear, the time is {str_time}.")
        elif 'open code' in query:
            codepath = "C:\\Users\\korra\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Code.exe"
            if os.path.isfile(codepath):
                os.startfile(codepath)
            else:
                speak("Visual Studio Code executable not found.")
        elif 'read file' in query:
            filepath = query.replace("read file", "").strip()
            content = read_local_file(filepath)
            speak(f"File content is: {content[:100]}")  
        elif 'write file' in query:
            parts = query.replace("write file", "").strip().split(' ', 1)
            if len(parts) == 2:
                filepath, content = parts
                result = write_local_file(filepath, content)
                speak(result)
            else:
                speak("Please provide the file path and content to write.")
        elif 'list files' in query:
            directory = query.replace("list files", "").strip()
            files = list_files_in_directory(directory)
            speak(f"Files in the directory are: {', '.join(files)}" if isinstance(files, list) else files)
        elif 'brightness' in query:
            try:
                level = int(query.replace("brightness", "").strip())
                adjust_brightness(level)
            except ValueError:
                speak("Please provide a valid number for brightness level.")
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a great day.")
            break
