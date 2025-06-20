import js, json, random
from pyodide.ffi import create_proxy

document = js.document
QUESTIONS_PER_SECTION = 10

all_questions = []
sections = []
current_section = None
current_idx = 0
score = 0
user_answers = []

def load_file(event=None):
    file_input = document.getElementById("file-input")
    f = file_input.files.item(0)
    if not f:
        document.getElementById("feedback").innerHTML = "Please select a JSON file."
        return
    reader = js.FileReader.new()
    def onload(e):
        global all_questions
        try:
            data = json.loads(reader.result)
            if not isinstance(data, list):
                raise
            random.shuffle(data)
            # Shuffle choices within each question
            for q in data:
                if "choices" in q and isinstance(q["choices"], list):
                    random.shuffle(q["choices"])
            all_questions = data
            if len(data) < QUESTIONS_PER_SECTION:
                document.getElementById("feedback").innerHTML = f"Need at least {QUESTIONS_PER_SECTION} questions."
                return
            document.getElementById("upload-section").style.display = "none"
            setup_sections()
        except:
            document.getElementById("feedback").innerHTML = "Invalid JSON format."
    reader.onload = create_proxy(onload)
    reader.readAsText(f)

def setup_sections():
    global sections
    sections = [all_questions[i:i+QUESTIONS_PER_SECTION] for i in range(0, len(all_questions), QUESTIONS_PER_SECTION)]
    btns = ""
    for i in range(len(sections)):
        btns += f'<button id="sec-{i}">Section {i+1}</button> '
    document.getElementById("section-buttons").innerHTML = btns
    for i in range(len(sections)):
        btn = document.getElementById(f"sec-{i}")
        btn.addEventListener("click", create_proxy(lambda e, idx=i: start_section(idx)))
    document.getElementById("select-section").style.display = "block"

def start_section(idx):
    global current_section, current_idx, score, user_answers
    current_section = sections[idx]
    current_idx = 0
    score = 0
    user_answers = []
    document.getElementById("select-section").style.display = "none"
    document.getElementById("quiz-section").style.display = "block"
    document.getElementById("section-title").innerText = f"Section {idx+1}"
    display_question()

def display_question():
    q = current_section[current_idx]
    document.getElementById("question").innerHTML = q["question"]
    # render choices
    html = ""
    for i, ch in enumerate(q["choices"]):
        html += f'<input type="radio" name="choice" id="c{i}" value="{ch}"> <label for="c{i}">{ch}</label><br>'
    document.getElementById("choices").innerHTML = html
    document.getElementById("feedback").innerHTML = ""
    document.getElementById("score").innerHTML = f"Score: {score}/{len(current_section)}"

def submit_answer(event):
    global current_idx, score
    sel = document.querySelector('input[name="choice"]:checked')
    if not sel:
        document.getElementById("feedback").innerHTML = "Please select an answer."
        return
    answer = sel.value
    q = current_section[current_idx]
    correct = (answer == q["answer"])
    user_answers.append({"question": q["question"], "your": answer, "correct": q["answer"], "is_correct": correct})
    if correct:
        score += 1
        document.getElementById("feedback").innerHTML = "✅ Correct!"
    else:
        document.getElementById("feedback").innerHTML = f"❌ Wrong! Correct: {q['answer']}"
    current_idx += 1
    if current_idx < len(current_section):
        display_question()
    else:
        show_summary()

def show_summary():
    document.getElementById("quiz-section").style.display = "none"
    html = "<table><tr><th>#</th><th>Question</th><th>Your Answer</th><th>Correct Answer</th></tr>"
    for i, ua in enumerate(user_answers,1):
        cls = "correct" if ua["is_correct"] else "wrong"
        html += f'<tr><td>{i}</td><td>{ua["question"]}</td><td class="{cls}">{ua["your"]}</td><td>{ua["correct"]}</td></tr>'
    html += "</table>"
    document.getElementById("summary-list").innerHTML = html
    document.getElementById("summary").style.display = "block"

def play_again(event):
    document.getElementById("summary").style.display = "none"
    document.getElementById("select-section").style.display = "block"

# Event bindings
document.getElementById("load-btn").addEventListener("click", create_proxy(load_file))
document.getElementById("submit-btn").addEventListener("click", create_proxy(submit_answer))
document.getElementById("play-again-btn").addEventListener("click", create_proxy(play_again))
