# Voice-controlled scientific calculator (Jupyter Notebook compatible)
import speech_recognition as sr
import math

def safe_eval(expr):
    # Allowed names for eval
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names.update({'abs': abs, 'round': round})
    try:
        return eval(expr, {"__builtins__": None}, allowed_names)
    except Exception as e:
        return f"Error: {e}"

recognizer = sr.Recognizer()

print("Say your calculation (e.g., '2 plus 2', 'sin 30', 'log 10'):")

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    print("Listening...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
    # Replace words with symbols for basic operations
    text = text.lower()
    text = text.replace('plus', '+').replace('minus', '-')
    text = text.replace('times', '*').replace('multiplied by', '*')
    text = text.replace('x', '*').replace('divided by', '/').replace('over', '/')
    text = text.replace('power', '**').replace('to the power of', '**')
    # Replace spoken math functions
    text = text.replace('sin', 'math.sin')
    text = text.replace('cos', 'math.cos')
    text = text.replace('tan', 'math.tan')
    text = text.replace('log', 'math.log10')
    text = text.replace('ln', 'math.log')
    text = text.replace('sqrt', 'math.sqrt')
    # Remove 'of' and 'by' for easier parsing
    text = text.replace(' of ', ' ').replace(' by ', ' ')
    # Evaluate the expression
    result = safe_eval(text)
    print("Result:", result)
except sr.UnknownValueError:
    print("Sorry, could not understand the audio.")
except sr.RequestError as e:
    print(f"Could not request results; {e}")