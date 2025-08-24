from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('OPENROUTER_API_KEY')
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/')
def home():
    # Возвращаем HTML файл
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/style.css')
def style():
    # Возвращаем CSS файл
    with open('style.css', 'r', encoding='utf-8') as f:
        return f.read(), 200, {'Content-Type': 'text/css'}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        
        if not user_message:
            return jsonify({'error': 'Сообщение не может быть пустым'}), 400

        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "model": "z-ai/glm-4.5-air:free",  # Используем указанную модель
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response_data = response.json()

        if 'choices' in response_data and len(response_data['choices']) > 0:
            ai_response = response_data['choices'][0]['message']['content']
            return jsonify({'response': ai_response})
        else:
            return jsonify({'error': 'Ошибка получения ответа от ИИ'}), 500

    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5500, host='127.0.0.1')