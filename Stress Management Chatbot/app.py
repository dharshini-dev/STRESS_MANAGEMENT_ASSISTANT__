import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Configure the Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the model
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)
CORS(app)

def virtual_psychologist(user_input):
    # Define the context for the AI
    context = """"You’re a friendly and empathetic virtual assistant here to support users with their stress and mental health concerns. Your job is to provide warm, caring responses that make users feel heard and understood. Always remind them that seeking professional help is important for serious issues, but avoid diagnosing or suggesting any medication. If someone asks about something unrelated to mental health, kindly let them know that you’re here specifically for mental health support, and gently guide the conversation back to how you can help them feel better"""
    
    # Combine the context and user input
    prompt = f"{context}\n\nUser: {user_input}\n\nAssistant:"
    
    try:
        # Generate a response
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        return f"An error occurred: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    if not user_input.strip():
        return jsonify({"response": "I'm sorry, but I didn't receive any input. Could you please provide a question or topic related to mental health?"})
    
    response = virtual_psychologist(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)