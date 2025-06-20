import js
import json

document = js.document

# --- Câu hỏi mặc định ---
default_questions = [
    {"question": "What is the capital of France?", "choices": ["Paris", "London", "Berlin", "Madrid"], "answer": "Paris"},
    {"question": "What is 2 + 2?", "choices": ["3", "4", "5", "6"], "answer": "4"},
    {"question": "Which planet is known as the Red Planet?", "choices": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
    {"question": "What color do you get by mixing red and white?", "choices": ["Pink", "Purple", "Orange", "Brown"], "answer": "Pink"},
    {"question": "How many continents are there?", "choices": ["5", "6", "7", "8"], "answer": "7"},
    {"question": "What is the boiling point of water?", "choices": ["90°C", "100°C", "110°C", "120°C"], "answer": "100°C"},
    {"question": "Who wrote 'Romeo and Juliet'?", "choices": ["Shakespeare", "Dickens", "Tolstoy", "Hemingway"], "answer": "Shakespeare"},
    {"question": "What is the largest ocean?", "choices": ["Atlantic", "Indian", "Pacific", "Arctic"], "answer": "Pacific"},
    {"question": "Which gas do plants breathe in?", "choices": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon dioxide"},
    {"question": "What is the square root of 81?", "choices": ["7", "8", "9", "10"], "answer": "9"},
    # ... có thể thêm nhiều câu hơn
]

# --- Các biến toàn cục ---
questions = default_questions.copy()
current_question_index = 0
score = 0
answers_record = []  # lưu trữ từng câu hỏi, đáp án user, kết quả đúng/sai

QUESTIONS_PER_PART = 10
current_part = 1
total_parts = (len(questions) + QUESTIONS_PER_PART - 1) // QUESTIONS_PER_PART

def update_part_info():
    global current_part, total_parts
    document.getElementById("part-info").innerHTML = f"Part {current_part} / {total_parts}"

def display_question():
    global current_question_index, questions
    if current_question_index >= len(questions):
        show_results()
        return
    
    update_part_info()

    q = questions[current_question_index]
    document.getElementById("question").innerHTML = f"{current_question_index+1}. {q['question']}"
    
    choices_html = ""
    for i, choice in enumerate(q["choices"]):
        choices_html += f'<input type="radio" name="choice" id="choice{i}" value="{choice}"> <label for="choice{i}">{choice}</label><br>'
    document.getElementById("choices").innerHTML = choices_html
    document.getElementById("feedback").innerHTML = ""
    document.getElementById("score").innerHTML = f"Score: {score}"

def check_answer(*args):
    global current_question_index, score, answers_record, current_part, total_parts

    selected = document.querySelector('input[name="choice"]:checked')
    if not selected:
        document.getElementById("feedback").innerHTML = "<span style='color:red;'>Please select an answer!</span>"
        return
    
    answer = selected.value
    correct_answer = questions[current_question_index]["answer"]

    is_correct = (answer == correct_answer)
    if is_correct:
        score += 1
        document.getElementById("feedback").innerHTML = "Correct!"
    else:
        document.getElementById("feedback").innerHTML = f"Wrong! Correct answer: {correct_answer}"

    # Ghi nhận câu trả lời
    answers_record.append({
        "question": questions[current_question_index]["question"],
        "your_answer": answer,
        "correct_answer": correct_answer,
        "correct": is_correct
    })

    current_question_index += 1

    # Cập nhật part hiện tại dựa trên câu hỏi
    current_part = (current_question_index // QUESTIONS_PER_PART) + 1

    if current_question_index < len(questions):
        display_question()
    else:
        show_results()

def show_results():
    document.getElementById("question").innerHTML = "<b>Quiz Completed!</b>"
    document.getElementById("choices").innerHTML = ""
    document.getElementById("submit").style.display = "none"
    document.getElementById("feedback").innerHTML = ""
    document.getElementById("score").innerHTML = f"Final Score: {score} / {len(questions)}"
    document.getElementById("part-info").innerHTML = ""

    results_div = document.getElementById("results")
    results_html = "<h3>Review Answers:</h3><ol>"
    for ans in answers_record:
        color = "green" if ans["correct"] else "red"
        results_html += f"<li>{ans['question']}<br>Your answer: <span style='color:{color}'>{ans['your_answer']}</span><br>Correct answer: {ans['correct_answer']}</li><br>"
    results_html += "</ol>"
    results_div.innerHTML = results_html

# --- Xử lý upload file ---
def handle_file_upload(event):
    global questions, current_question_index, score, answers_record, current_part, total_parts
    
    file = event.target.files.item(0)
    if not file:
        return
    
    def onload(evt):
        try:
            content = evt.target.result
            data = json.loads(content)
            # Kiểm tra định dạng
            if not isinstance(data, list) or not all(
                "question" in q and "choices" in q and "answer" in q and
                isinstance(q["question"], str) and
                isinstance(q["choices"], list) and
                len(q["choices"]) >= 2 and
                q["answer"] in q["choices"]
                for q in data):
                raise ValueError("Invalid question file format")
            
            # Thay thế câu hỏi, reset trạng thái
            questions = data
            current_question_index = 0
            score = 0
            answers_record = []
            current_part = 1
            total_parts = (len(questions) + QUESTIONS_PER_PART - 1) // QUESTIONS_PER_PART
            document.getElementById("submit").style.display = "inline-block"
            document.getElementById("results").innerHTML = ""
            display_question()
            document.getElementById("feedback").innerHTML = "<span style='color:green;'>Uploaded questions loaded successfully!</span>"
        except Exception as e:
            document.getElementById("feedback").innerHTML = f"<span style='color:red;'>Error loading file: {e}</span>"
    
    reader = js.FileReader.new()
    reader.onload = onload
    reader.readAsText(file)

# Đăng ký sự kiện input file
file_input = document.getElementById("file-upload")
file_input.addEventListener("change", handle_file_upload)

# Khởi động quiz với bộ câu hỏi mặc định
display_question()
