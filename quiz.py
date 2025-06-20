from js import document
import random

questions = [
    {"question": "What is the capital of France?", "choices": ["Paris", "London", "Berlin", "Madrid"], "answer": "Paris"},
    {"question": "What is 2 + 2?", "choices": ["3", "4", "5", "6"], "answer": "4"},
    {"question": "Which planet is known as the Red Planet?", "choices": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"}
]

current_question = 0
score = 0

def display_question():
    q = questions[current_question]
    document.getElementById("question").innerHTML = q["question"]
    choices_html = ""
    for i, choice in enumerate(q["choices"]):
        choices_html += f'<input type="radio" name="choice" id="choice{i}" value="{choice}"> <label for="choice{i}">{choice}</label><br>'
    document.getElementById("choices").innerHTML = choices_html
    document.getElementById("feedback").innerHTML = ""

def check_answer(*args):
    global current_question, score
    selected = document.querySelector('input[name="choice"]:checked')
    if selected:
        answer = selected.value
        correct_answer = questions[current_question]["answer"]
        if answer == correct_answer:
            score += 1
            document.getElementById("feedback").innerHTML = "Correct!"
        else:
            document.getElementById("feedback").innerHTML = f"Wrong! The correct answer is {correct_answer}."
        current_question += 1
        document.getElementById("score").innerHTML = f"Score: {score}"
        if current_question < len(questions):
            display_question()
        else:
            document.getElementById("question").innerHTML = "Quiz Completed!"
            document.getElementById("choices").innerHTML = ""
            document.getElementById("feedback").innerHTML = f"Final Score: {score}/{len(questions)}"

display_question()