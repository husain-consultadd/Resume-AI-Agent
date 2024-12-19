# app.py

import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit page configuration
st.set_page_config(
    page_title="Tech Resume Crafter",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for styling
# Custom CSS for styling
def local_css():
    st.markdown(
        """
        <style>
        /* General Body Styling */
        .chat-header {
            background-color: #202123;
            padding: 10px 20px;
            text-align: center;
            color: #ffffff;
            font-size: 24px;
            font-weight: bold;
            border-radius: 8px 8px 0 0;
        }

        /* Chat Window */
        .chat-window {
            background-color: #2d2f36;
            padding: 15px;
            border-radius: 0 0 8px 8px;
            height: 60vh;
            overflow-y: auto;
            width: 100%;  /* Ensure it takes full width */
            box-sizing: border-box;  /* Include padding in width */
        }

        /* Container for Chat and Input */
        .chat-container {
            display: flex;
            flex-direction: column;
            max-width: 800px;  /* Set a max width for better readability */
            margin: auto;  /* Center the container */
        }

        /* User Message */
        .user-message {
            background-color: #1a73e8;
            color: #ffffff;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            max-width: 70%;
            align-self: flex-end;
            word-wrap: break-word;
        }

        /* GPT Message */
        .gpt-message {
            background-color: #3e3f4b;
            color: #ffffff;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            max-width: 70%;
            align-self: flex-start;
            word-wrap: break-word;
        }

        /* Input Section */
        .input-section {
            display: flex;
            align-items: center;
            background-color: #40414f;
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            width: 100%;  /* Ensure it takes full width */
            box-sizing: border-box;  /* Include padding in width */
        }

        /* Textarea Styling */
        textarea {
            flex: 1;
            border: none;
            background-color: #565869;
            color: #ffffff;
            padding: 12px 15px;
            border-radius: 24px;
            font-size: 16px;
            resize: none;
            outline: none;
            max-height: 100px;
            max-width: 600px;  /* Limit the maximum width */
        }

        textarea:focus {
            background-color: #6b6d7b;
        }

        textarea::placeholder {
            color: #9ca3af;
        }

        /* Send Button Styling */
        .send-button {
            background-color: #1a73e8;
            border: none;
            color: #ffffff;
            cursor: pointer;
            margin-left: 10px;
            padding: 10px;
            border-radius: 50%;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.3s, transform 0.2s;
        }

        .send-button:hover {
            background-color: #1669d4;
            transform: scale(1.1);
        }

        .send-button:active {
            transform: scale(1);
        }

        /* Scrollbar Styling */
        .chat-window::-webkit-scrollbar {
            width: 8px;
        }

        .chat-window::-webkit-scrollbar-thumb {
            background: #565869;
            border-radius: 4px;
        }

        .chat-window::-webkit-scrollbar-thumb:hover {
            background: #737682;
        }

        .chat-window::-webkit-scrollbar-track {
            background: #343541;
        }

        /* Hide Streamlit's default styling for text areas and buttons */
        .stTextArea > div > div > textarea {
            height: 100px !important;
            max-width: 600px !important;  /* Ensure the textarea doesn't exceed the max width */
        }

        .stButton > button {
            display: none;
        }

        /* Center the chat container */
        .streamlit-container {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


local_css()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown('<div class="chat-header">Tech Resume Crafter</div>', unsafe_allow_html=True)

# Chat window
chat_placeholder = st.empty()

# Input section
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_area(
        "",
        key="input",
        height=68,
        max_chars=None,
        placeholder="Type your message here...",
    )
    submit_button = st.form_submit_button(label="Send", type="primary")

# Function to add messages to the chat
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# Function to display messages
def display_messages():
    chat_content = '<div class="chat-window">'
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_content += f'<div class="user-message">{msg["content"]}</div>'
        else:
            chat_content += f'<div class="gpt-message">{msg["content"]}</div>'
    chat_content += '</div>'
    chat_placeholder.markdown(chat_content, unsafe_allow_html=True)

# Display existing messages
display_messages()

# Handle form submission
if submit_button and user_input.strip():
    add_message("user", user_input.strip())
    display_messages()

    # System Prompt
    system_prompt = (
        "TASK: "
        "1. Gather Initial Information: "
        "* Ask for the Job Description (JD): Prompt the user to provide the complete JD for the role they are targeting. "
        "* Job Level Analysis: Determine if the JD is for a junior-level or senior-level position. "
        "  * For junior roles, focus on creating projects from scratch to showcase technical expertise. "
        "2. Tech Stack Extraction: "
        "* Analyze the JD to identify the key technical stacks (programming languages, frameworks, tools, etc.) associated with the role. "
        "* Suggest additional or complementary technologies that might be required to complete the project fully. "
        "* Ensure these tools are aligned with the company's ecosystem (e.g., if the company uses Azure, avoid suggesting AWS). "
        "3. Project Details Collection: "
        "* Ask the user for the project title and a brief description of the project they want to include in the resume. "
        "* Based on the provided tech stack and project description, generate the following content: "
        "  * Problem Statement: Clearly define the issue the project addresses. "
        "  * Approach: Explain the steps and strategies used to develop the project. "
        "* Experience Bullet Points: Describe the project in detail using bullet points. "
        "4. Content Guidelines: "
        "* Avoid Redundant Tools: Do not include technologies that serve the same purpose in a single project (e.g., avoid pairing MySQL and PostgreSQL in the same context unless justified). "
        "* Unique Content: Ensure each bullet point is distinct, avoiding repetitive phrasing and ideas. "
        "* Technical Language: Use precise and advanced technical terminology to describe tools, methodologies, and outcomes. "
        "* Bullet Point Format: "
        "  * Provide 10 to 15 bullet points per project (approximately 900-1000 words total). "
        "  * Each bullet point should be 25-40 words in length. "
        "  * No subheadings within the bullet points. "
        "5. Role-Specific Focus: "
        "* For junior-level roles, emphasize: "
        "  * Developing projects from the ground up. "
        "  * Demonstrating technical skills, problem-solving abilities, and a thorough understanding of the development process. "
        "* For senior-level roles, highlight: "
        "  * Enhancements made to existing systems. "
        "  * Efficiency improvements, scalability, and technical leadership. "
        "  * Contributions to the company's workflow optimization or system architecture. "
        "6. Provide ATS Evaluation: "
        "  Review the Generated Content against the JD to provide an ATS score and feedback. Follow this structure: "
        " 1. Percentage Match: Calculate and display the percentage match between the content and the JD. "
        " 2. Missing Keywords: Identify important keywords or skills missing from the content that are present in the JD. "
        " 3. Final Thoughts: Provide an evaluation summary highlighting the strengths and weaknesses of the generated content in relation to the JD. "
        "Example Output Template: "
        "* [Bullet Point 1]: Designed and implemented a scalable microservices architecture using Python and Docker to optimize service deployment and management. "
        "* [Bullet Point 2]: Developed REST APIs with Flask and PostgreSQL to facilitate seamless data exchange, reducing latency by 25%. "
        "* [Bullet Point 3]: Integrated CI/CD pipelines using Jenkins and GitHub Actions to automate testing and deployment, increasing code delivery speed by 40%. "
        "1. ATS Evaluation: "
        "* Match Percentage: e.g., 'Your resume matches the JD by 85%.' "
        "* Missing Keywords: e.g., 'Missing Keywords: Docker, Kubernetes, CI/CD.' "
        "* Final Thoughts: e.g., 'Your profile aligns well with the role, but incorporating more DevOps tools would strengthen your fit.'"
    )

    # Prepare the messages for OpenAI
    messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=10000,
        )

        assistant_message = response.choices[0].message.content.strip()
        add_message("assistant", assistant_message)
        display_messages()

    except Exception as e:
        add_message("assistant", f"An unexpected error occurred: {e}")
        display_messages()