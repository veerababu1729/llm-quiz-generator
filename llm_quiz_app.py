import streamlit as st
import os
import google.generativeai as genai
from typing import List, Dict, Any
import re

# --- MOCK DATA FOR TESTING ---
MOCK_QUIZ = {
    "questions": [
        {
            "question": "What is the principle of wave-particle duality?",
            "type": "short answer",
            "answer": "It states that every particle or quantum entity exhibits both wave and particle properties.",
            "explanation": "Wave-particle duality is a fundamental concept of quantum mechanics."
        },
        {
            "question": "Which of the following is an example of quantum entanglement?",
            "type": "multiple choice",
            "options": [
                "Two electrons sharing the same orbit",
                "Two particles whose states are dependent regardless of distance",
                "A photon passing through a slit",
                "A neutron decaying into a proton"
            ],
            "answer": "Two particles whose states are dependent regardless of distance",
            "explanation": "Entanglement means the state of one particle instantly influences the other, no matter the distance."
        },
        {
            "question": "True or False: The Schrödinger equation is a fundamental equation in quantum mechanics.",
            "type": "true/false",
            "answer": "True",
            "explanation": "The Schrödinger equation describes how the quantum state of a system changes over time."
        }
    ]
}

# --- LLM API CALL ---
def generate_quiz(params: Dict[str, Any]) -> Dict[str, Any]:
    """Call Gemini API to generate quiz based on parameters. Returns parsed quiz dict."""
    prompt = build_prompt(params)
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyA_oHh-VfRexj6B8pF6YLAJd_CnLBj162g"))
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        quiz_text = response.text
        return parse_quiz_output(quiz_text)
    except Exception as e:
        st.warning(f"Gemini API error: {e}. Showing mock quiz.")
        return MOCK_QUIZ

# --- PROMPT ENGINEERING ---
def build_prompt(params: Dict[str, Any]) -> str:
    prompt = f"""
You are a quiz generator. Generate a quiz following this EXACT format for each question type:

For multiple choice questions:
1. [Question text here]
a) [First option here]
b) [Second option here]
c) [Third option here]
d) [Fourth option here]
Answer: [Correct option letter (a, b, c, or d)]
Explanation: [Explanation text if requested]

For true/false questions:
1. [Question text here]
True/False: [statement]
Answer: [True or False]
Explanation: [Explanation text if requested]

For short answer questions:
1. [Question text here]
Answer: [Correct answer text]
Explanation: [Explanation text if requested]

Generate a quiz with these parameters:
- Topic: {params['topic']}
- Difficulty: {params['difficulty']}
- Number of Questions: {params['num_questions']}
- Question Types: {', '.join(params['question_types'])}
"""
    if params.get('subtopics'):
        prompt += f"- Sub-topics: {', '.join(params['subtopics'])}\n"
    if params.get('context_keywords'):
        prompt += f"- Context Keywords: {', '.join(params['context_keywords'])}\n"
    if params.get('target_audience'):
        prompt += f"- Target Audience: {params['target_audience']}\n"
    prompt += f"- Language: {params.get('language', 'en')}\n"
    prompt += f"- Include Explanations: {'Yes' if params.get('include_explanations') else 'No'}\n"
    if params.get('max_length'):
        prompt += f"- Maximum Length per Question: {params['max_length']} words\n"
    
    prompt += "\nIMPORTANT: Follow the exact format shown above. For multiple choice, always provide exactly 4 options labeled a), b), c), d)."
    return prompt

# --- PARSING LLM OUTPUT ---
def parse_quiz_output(text: str) -> Dict[str, Any]:
    # This is a simple parser for demo purposes. Adjust as needed for your LLM's output format.
    questions = []
    q_blocks = re.split(r'\n\d+\. ', '\n' + text)
    for block in q_blocks[1:]:
        q = {}
        lines = block.strip().split('\n')
        q['question'] = lines[0]
        if any(opt in lines[1].lower() for opt in ['a)', 'b)', 'c)', 'd)']):
            q['type'] = 'multiple choice'
            q['options'] = [l[3:].strip() for l in lines[1:5] if l[:2].lower() in ['a)', 'b)', 'c)', 'd)']]
            answer_line = next((l for l in lines if l.lower().startswith('answer:')), None)
            q['answer'] = answer_line.split(':',1)[1].strip() if answer_line else ''
        elif 'true' in lines[1].lower() or 'false' in lines[1].lower():
            q['type'] = 'true/false'
            q['answer'] = lines[1].strip()
        else:
            q['type'] = 'short answer'
            answer_line = next((l for l in lines if l.lower().startswith('answer:')), None)
            q['answer'] = answer_line.split(':',1)[1].strip() if answer_line else ''
        explanation_line = next((l for l in lines if l.lower().startswith('explanation:')), None)
        q['explanation'] = explanation_line.split(':',1)[1].strip() if explanation_line else ''
        questions.append(q)
    return {"questions": questions}

# --- QUIZ INTERACTION ---
def take_quiz(quiz: Dict[str, Any]) -> None:
    """Allow user to take the quiz and get scored."""
    if 'user_answers' not in st.session_state or len(st.session_state.user_answers) != len(quiz["questions"]):
        st.session_state.user_answers = [None] * len(quiz["questions"])
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

    st.header("Take the Quiz")

    # Collect user answers for each question
    for idx, q in enumerate(quiz["questions"], 1):
        st.markdown(f"**Q{idx}: {q['question']}**")
        if q['type'] == 'multiple choice' and 'options' in q:
            options = q['options']
            option_letters = [chr(97 + i) for i in range(len(options))]
            options_dict = {f"{letter}) {opt}": letter for letter, opt in zip(option_letters, options)}
            user_choice = st.radio(
                f"Select your answer:",
                options_dict.keys(),
                key=f"q{idx}",
                index=None if not st.session_state.quiz_submitted else list(options_dict.values()).index(st.session_state.user_answers[idx-1]) if st.session_state.user_answers[idx-1] in options_dict.values() else None
            )
            if not st.session_state.quiz_submitted and user_choice:
                st.session_state.user_answers[idx-1] = options_dict[user_choice]
        elif q['type'] == 'true/false':
            user_choice = st.radio(
                f"Select your answer:",
                ["True", "False"],
                key=f"q{idx}",
                index=None if not st.session_state.quiz_submitted else ["True", "False"].index(st.session_state.user_answers[idx-1]) if st.session_state.user_answers[idx-1] in ["True", "False"] else None
            )
            if not st.session_state.quiz_submitted and user_choice:
                st.session_state.user_answers[idx-1] = user_choice
        else:  # short answer
            user_text = st.text_input(
                f"Enter your answer:",
                key=f"q{idx}",
                value=st.session_state.user_answers[idx-1] or ""
            )
            if not st.session_state.quiz_submitted and user_text:
                st.session_state.user_answers[idx-1] = user_text
                
        # Show validation and explanation only after submission
        if st.session_state.quiz_submitted:
            user_ans = st.session_state.user_answers[idx-1]
            if user_ans is None:
                st.warning(f"No answer provided")
            else:
                correct = False
                if q['type'] == 'multiple choice':
                    correct = user_ans.lower() == q['answer'].lower()
                elif q['type'] == 'true/false':
                    correct = user_ans.lower() == q['answer'].lower()
                else:  # short answer
                    correct = user_ans.lower().strip() == q['answer'].lower().strip()
                
                if correct:
                    st.success(f"✅ Correct!")
                else:
                    st.error(f"❌ Incorrect")
                    st.markdown(f"Your answer: **{user_ans}**")
                    st.markdown(f"Correct answer: **{q['answer']}**")
                
                # Show explanation after submission
                if q.get('explanation'):
                    st.info(f"💡 *{q['explanation']}*")
        
        st.markdown("---")

    # Submit button at the bottom
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.quiz_submitted:
            if st.button("Submit Quiz", key="submit_quiz"):
                st.session_state.quiz_submitted = True
                st.rerun()

    # Show results after submission (total marks and % at bottom only)
    if st.session_state.quiz_submitted:
        correct_answers = 0
        total_questions = len(quiz["questions"])
        for idx, (q, user_ans) in enumerate(zip(quiz["questions"], st.session_state.user_answers), 1):
            if user_ans is None:
                continue
            correct = False
            if q['type'] == 'multiple choice':
                correct = user_ans.lower() == q['answer'].lower()
            elif q['type'] == 'true/false':
                correct = user_ans.lower() == q['answer'].lower()
            else:  # short answer
                correct = user_ans.lower().strip() == q['answer'].lower().strip()
            if correct:
                correct_answers += 1
                
        score_percentage = (correct_answers / total_questions) * 100
        st.header(f"Final Score: {correct_answers}/{total_questions} ({score_percentage:.1f}%)")
        if score_percentage >= 90:
            st.balloons()
            st.success("🎯 Excellent work! Keep it up!")
        elif score_percentage >= 70:
            st.success("👍 Good job!")
        elif score_percentage >= 50:
            st.warning("📚 Keep practicing!")
        else:
            st.error("📖 You might want to review the material.")
        
        # Reset button at the bottom
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Try Again", key="reset_quiz"):
                st.session_state.quiz_submitted = False
                st.session_state.user_answers = [None] * len(quiz["questions"])
                st.rerun()

# --- STREAMLIT UI ---
st.set_page_config(page_title="LLM Quiz Creator", layout="centered")
st.title("🤖 Interactive LLM-Powered Quiz Creator")

# Add tabs for create/take quiz
tab1, tab2 = st.tabs(["Create Quiz", "Take Quiz"])

with tab1:
    st.markdown("""
    Create a new quiz using a Large Language Model. Set your parameters below.
    """)
    
    with st.form("quiz_params_form"):
        topic = st.text_input("Quiz Topic", "Quantum Physics")
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, value=3)
        question_types = st.multiselect("Question Types", ["multiple choice", "short answer", "true/false"], default=["multiple choice"])
        subtopics = st.text_input("Specific Sub-topics (comma separated, optional)")
        context_keywords = st.text_input("Context Keywords (comma separated, optional)")
        target_audience = st.text_input("Target Audience (optional)")
        language = st.text_input("Language (default: en)", "en")
        include_explanations = st.checkbox("Include Explanations?", value=True)
        max_length = st.number_input("Maximum Length per Question (words, optional)", min_value=0, value=0)
        submitted = st.form_submit_button("Generate Quiz")

    if submitted:
        params = {
            "topic": topic,
            "difficulty": difficulty,
            "num_questions": num_questions,
            "question_types": question_types,
            "subtopics": [s.strip() for s in subtopics.split(",") if s.strip()] if subtopics else [],
            "context_keywords": [k.strip() for k in context_keywords.split(",") if k.strip()] if context_keywords else [],
            "target_audience": target_audience if target_audience else None,
            "language": language if language else "en",
            "include_explanations": include_explanations,
            "max_length": max_length if max_length > 0 else None
        }
        quiz = generate_quiz(params)
        # Store quiz in session state for the Take Quiz tab
        st.session_state['current_quiz'] = quiz
        
        # Preview the generated quiz
        st.header("Generated Quiz Preview")
        for idx, q in enumerate(quiz["questions"], 1):
            st.markdown(f"**Q{idx}: {q['question']}**")
            if q['type'] == 'multiple choice' and 'options' in q:
                for i, opt in enumerate(q['options']):
                    letter = chr(97 + i)
                    st.markdown(f"{letter}) {opt}")
            st.markdown(f"**Answer:** {q['answer']}")
            if q.get('explanation'):
                st.markdown(f"*Explanation: {q['explanation']}*")
            st.markdown("---")
        
        st.success("Quiz generated! Go to the 'Take Quiz' tab to try it out.")

with tab2:
    st.markdown("""
    Take the quiz that was just generated. Your answers will be scored at the end.
    """)
    
    if 'current_quiz' in st.session_state:
        take_quiz(st.session_state['current_quiz'])
    else:
        st.info("Please generate a quiz first in the 'Create Quiz' tab.")