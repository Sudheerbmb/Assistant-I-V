from flask import Flask, request, jsonify, render_template_string
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import wmi

app = Flask(__name__)

# Initialize pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        return "Good Morning!!!"
    elif hour >= 12 and hour < 18:
        return "Good Afternoon!!!"
    else:
        return "Good Evening!!!"

def take_command(text):
    return text.lower()

def process_query(query):
    response = ""
    if 'wikipedia' in query:
        response = 'Searching Wikipedia...'
        query = query.replace("wikipedia", "")
        try:
            result = wikipedia.summary(query, sentences=2)
            response = f"According to Wikipedia: {result}"
        except wikipedia.exceptions.DisambiguationError:
            response = "There are multiple results for that query. Please be more specific."
        except wikipedia.exceptions.PageError:
            response = "Sorry, I could not find any results for that query."
    elif 'open youtube' in query:
        webbrowser.open("https://youtube.com")
        response = "Opening YouTube."
    elif 'open google' in query:
        webbrowser.open("https://google.com")
        response = "Opening Google."
    elif 'hi shinchan' in query:
        response = "Hi! I am Shinchan. How is your day?"
    elif 'open stack overflow' in query:
        webbrowser.open("https://stackoverflow.com")
        response = "Opening Stack Overflow."
    elif 'play music' in query:
        music_url = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
        webbrowser.open(music_url)
        response = "Playing music."
    elif 'the time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"Dear, the time is {str_time}."
    elif 'open code' in query:
        if os.path.isfile(codepath):
            os.startfile(codepath)
            response = "Opening Visual Studio Code."
        else:
            response = "Visual Studio Code executable not found."
    elif 'read file' in query:
        filepath = query.replace("read file", "").strip()
        content = read_local_file(filepath)
        response = f"File content is: {content[:100]}"
    elif 'write file' in query:
        parts = query.replace("write file", "").strip().split(' ', 1)
        if len(parts) == 2:
            filepath, content = parts
            result = write_local_file(filepath, content)
            response = result
        else:
            response = "Please provide the file path and content to write."
    elif 'list files' in query:
        directory = query.replace("list files", "").strip()
        files = list_files_in_directory(directory)
        response = f"Files in the directory are: {', '.join(files)}" if isinstance(files, list) else files
    elif 'brightness' in query:
        try:
            level = int(query.replace("brightness", "").strip())
            response = adjust_brightness(level)
        except ValueError:
            response = "Please provide a valid number for brightness level."
    elif 'exit' in query or 'quit' in query:
        response = "Goodbye! Have a great day."
    else:
        response = "Sorry, I didn't understand that command."
    return response

@app.route('/')
def home():
    # HTML content as a string
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shinchan Assistant</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            input[type="text"] {
                width: 80%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            button {
                padding: 10px 20px;
                border: none;
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            #response {
                margin-top: 20px;
                font-size: 1.2em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Shinchan Assistant</h1>
            <form id="commandForm">
                <input type="text" id="user_input" name="user_input" placeholder="Enter command..." required>
                <button type="submit">Submit</button>
            </form>
            <div id="response"></div>
        </div>
        <script>
            document.getElementById('commandForm').addEventListener('submit', function(event) {
                event.preventDefault();
                const userInput = document.getElementById('user_input').value;
                fetch('/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        'user_input': userInput
                    })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('response').innerText = data.response;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['user_input']
    response = process_query(user_input)
    return jsonify({'response': response})

def read_local_file(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    else:
        return "File not found."

def write_local_file(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)
    return "File written successfully."

def list_files_in_directory(directory):
    if os.path.isdir(directory):
        files = os.listdir(directory)
        return files
    else:
        return "Directory not found."

def adjust_brightness(level):
    if 0 <= level <= 100:
        try:
            wmi_interface = wmi.WMI(namespace='wmi')
            brightness = wmi_interface.WmiMonitorBrightnessMethods()[0]
            brightness.WmiSetBrightness(level, 0)
            return f"Brightness set to {level} percent."
        except Exception as e:
            return f"Failed to set brightness. Error: {e}"
    else:
        return "Brightness level should be between 0 and 100."

if __name__ == "__main__":
    app.run(debug=True)
