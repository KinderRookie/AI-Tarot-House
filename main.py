import os
import random
from flask import Flask, render_template, request
import openai
from tarot_data import tarot_data  # Import the tarot data

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')
try:
    with open('/etc/secrets/api_key.txt', 'r') as file:
        openai.api_key = file.read()
except FileNotFoundError:
    print("The file does not exist")
except Exception as e:
    print(f"An error occurred: {e}")

@app.route('/')
def index():
    return render_template('proto.html')

@app.route('/tarot', methods=['POST'])
def get_tarot():
    card_indices = random.sample(range(22), 3)
    cards = [tarot_data[index] for index in card_indices]
    card_names = ', '.join(card['card_name'] for card in cards)
    
    question = request.form['question']
    selected_language = request.form['language']


    if selected_language == 'English':
        prompt = f"Your question: {question}, and my tarot card is {card_names}. "
    elif selected_language == 'Korean':
        prompt = f"질문은 다음과 같습니다. : {question}, 그리고 나의 타로 카드는 {card_names}입니다. "
    
    

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system", "content":"You are a AI tarot reader. You give advice to client based on his/her tarot card."},
                {"role":"user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=600,
            top_p=1,
        )
        answer = response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        answer = "Sorry, there was an error processing your request."
        answer = e
    
    return render_template('answer.html', cards=card_indices, answer=answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
