
# Assistant-I-V - Flask Voice Assistant

## Overview
This Assistant is a Flask-based AI-powered voice assistant that can process user commands to perform various actions such as retrieving information from Wikipedia, opening websites, playing music, managing files, adjusting screen brightness, and more. The assistant also features a web-based interface for user interaction.

## Features
- **Voice-based interaction** using `pyttsx3`
- **Wikipedia search** for quick knowledge retrieval
- **Web navigation** (YouTube, Google, Stack Overflow, etc.)
- **File management** (read, write, list files in a directory)
- **Music playback**
- **System brightness control**
- **Real-time clock**
- **Flask-based web interface**

## Technologies Used
- **Python** (Flask, pyttsx3, wikipedia, wmi, webbrowser, datetime, os)
- **HTML, CSS, JavaScript** (for the web-based UI)

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/shinchan-assistant.git
   ```
2. Install dependencies:
   ```bash
   pip install flask pyttsx3 wikipedia wmi
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage
1. Open the web interface.
2. Enter a command (e.g., "open YouTube", "play music", "what is AI on Wikipedia").
3. The assistant will process the query and respond accordingly.

## Example Commands
| Command              | Action Performed |
|----------------------|-----------------|
| `open youtube`      | Opens YouTube   |
| `the time`          | Returns current time |
| `wikipedia AI`      | Fetches Wikipedia summary of AI |
| `play music`        | Plays an online music track |
| `read file test.txt` | Reads the contents of `test.txt` |
| `write file test.txt Hello` | Writes "Hello" to `test.txt` |
| `list files C:\\Users` | Lists files in `C:\Users` directory |
| `brightness 50`     | Adjusts screen brightness to 50% |

## API Endpoints
### `GET /`
Renders the web-based UI.

### `POST /process`
Processes user commands and returns a response.
- **Request Body:**
  ```json
  { "user_input": "your command here" }
  ```
- **Response:**
  ```json
  { "response": "processed response" }
  ```

## Troubleshooting
- If `wmi` module errors occur on Linux, use Windows as it is primarily a Windows-based module.
- Ensure Python's TTS engine (`sapi5`) is installed on Windows.
- Check if the `wikipedia` package is installed if Wikipedia queries fail.

## License
This project is licensed under the MIT License.

## Author
**Your Name**  
GitHub: [Sudheerbmb](https://github.com/yourusername)
