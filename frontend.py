import streamlit as st
import requests
import html
import mysql.connector
import random
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="onlinequizdb.c7w2cu4oaweu.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="9999101694",
        database="onlinequizdb"
    )

try:
    conn = get_connection()
except mysql.connector.Error as e:
    st.error(f"Error connecting to MySQL: {e}")
    st.stop()

st.set_page_config(page_title="Quiz App", layout="centered")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = None
if 'topic' not in st.session_state:
    st.session_state.topic = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}

def login(username, password):
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cur.fetchone()
    if user:
        st.session_state.user_id = user[0]
        st.session_state.username = user[1]
        st.session_state.logged_in = True
        return True
    return False

def signup(username, password):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        st.success("User registered successfully! Please login.")
    except mysql.connector.IntegrityError:
        st.error("Username already exists.")

def fetch_questions_from_api(level, topic, num_qs):
    topic_mapping = {
        "General Knowledge": 9,
        "Science": 17,
        "Mathematics": 19,
        "History": 23
    }
    category_id = topic_mapping.get(topic, 9)

    url = f"https://opentdb.com/api.php?amount={num_qs}&category={category_id}&difficulty={level}&type=multiple"
    response = requests.get(url).json()

    if "results" not in response or len(response["results"]) == 0:
        st.error("⚠️ No questions available for this selection. Please try another level or topic.")
        return []

    questions = []
    for q in response['results']:
        options = q['incorrect_answers'] + [q['correct_answer']]
        random.shuffle(options)
        questions.append({
            'question': html.unescape(q['question']),
            'options': [html.unescape(opt) for opt in options],
            'correct': html.unescape(q['correct_answer'])
        })
    return questions

if not st.session_state.logged_in:
    st.title("Welcome to Online Quiz")
    st.markdown("<p style='text-align: center;'>Please sign in to continue or create a new account.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

    with tab1:
        st.subheader("Sign In to your account")
        username = st.text_input("Username", key="signin_username")
        password = st.text_input("Password", type="password", key="signin_password")
        if st.button("Login", use_container_width=True):
            if login(username, password):
                st.success(f"Logged in as {username}")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Create a new account")
        new_username = st.text_input("Choose Username", key="signup_username")
        new_password = st.text_input("Choose Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
        if st.button("Register", use_container_width=True):
            if not new_username or not new_password:
                st.warning("Username and password cannot be empty")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                signup(new_username, new_password)
    st.stop()

if st.session_state.logged_in and not st.session_state.questions:
    st.title("Select Quiz Preferences")
    st.session_state.level = st.selectbox("Select Level", ["easy", "medium", "hard"])
    st.session_state.topic = st.selectbox("Select Topic", ["General Knowledge", "Science", "Mathematics", "History"])
    num_qs = st.selectbox("Select Number of Questions", [5, 10, 15, 20])

    if st.button("Start Quiz"):
        st.session_state.questions = fetch_questions_from_api(st.session_state.level, st.session_state.topic, num_qs)
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answers = {}
        st.rerun()

if st.session_state.questions:
    
    if len(st.session_state.questions) == 0 or st.session_state.current_q >= len(st.session_state.questions):
        st.stop()

    q_index = st.session_state.current_q
    question = st.session_state.questions[q_index]

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Question {q_index + 1}:** {question['question']}")
    with col2:
        st.metric("Score", st.session_state.score)

    selected_option = None
    selected_count = 0

    for i, option in enumerate(question['options']):
        key = f"q{q_index}_opt{i}"
        checked = st.checkbox(option, key=key, value=st.session_state.answers.get(key, False))
        if checked:
            selected_option = option
            selected_count += 1
        st.session_state.answers[key] = checked

    if selected_count > 1:
        st.warning("⚠️ Please select only one option.")

    if st.button("Next"):
        if selected_count == 1:
            if selected_option == question['correct']:
                st.session_state.score += 1
            st.session_state.current_q += 1

            if st.session_state.current_q >= len(st.session_state.questions):
                total_questions = len(st.session_state.questions)
                score = st.session_state.score
                percentage = (score / total_questions) * 100

                st.success(f"🎉 Quiz Completed!")
                st.markdown(f"## **Your Score:** {score} / {total_questions}")
                st.markdown(f"### Percentage: {percentage:.2f}%")
                st.progress(percentage / 100)

                st.markdown("---")
                st.markdown("### **Review Your Answers**")

                results_data = []
                for i, q in enumerate(st.session_state.questions):
                    st.write(f"**Q{i + 1}:** {q['question']}")
                    correct_answer = q['correct']

                    selected_answer = None
                    for opt_key, checked in st.session_state.answers.items():
                        if str(opt_key).startswith(f"q{i}_") and checked:
                            selected_answer = q['options'][int(str(opt_key).split("_opt")[1])]
                            break

                    if selected_answer == correct_answer:
                        st.success(f"✅ Your Answer: {selected_answer}")
                    else:
                        st.error(f"❌ Your Answer: {selected_answer if selected_answer else 'No answer selected'}")
                        st.info(f"Correct Answer: {correct_answer}")

                    results_data.append({
                        "Question": q['question'],
                        "Your Answer": selected_answer if selected_answer else "Not answered",
                        "Correct Answer": correct_answer,
                        "Result": "Correct" if selected_answer == correct_answer else "Wrong"
                    })
                    st.markdown("---")

                df_results = pd.DataFrame(results_data)
                csv = df_results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Quiz Report as CSV",
                    data=csv,
                    file_name="quiz_results.csv",
                    mime="text/csv",
                )

                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO results (user_id, level, topic, score, total_questions) VALUES (%s,%s,%s,%s,%s)",
                    (st.session_state.user_id, st.session_state.level, st.session_state.topic, score, total_questions)
                )
                conn.commit()

                st.session_state.questions = []
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.level = None
                st.session_state.topic = None
                st.session_state.answers = {}

                if st.button("Restart Quiz"):
                    st.rerun()
            else:
                st.rerun()
        else:
            st.error("Please select exactly one option before proceeding.")
