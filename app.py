# import os
# import openai
# import streamlit as st
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Set OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Streamlit page configuration
# st.set_page_config(
#     page_title="Tech Resume Crafter",
#     page_icon="\U0001F4BC",
#     layout="wide",
# )

# # Add custom CSS for centering the heading and styling user messages
# st.markdown("""
#     <style>
#     .center-heading {
#         text-align: center;
#         font-size: 36px;
#         font-weight: bold;
#         color: white;
#         margin-top: 20px;
#         margin-bottom: 20px;
#     }
#     .chat-container {
#         display: flex;
#         align-items: flex-start;
#         margin: 10px 0;
#     }
#     .chat-icon {
#         width: 40px;
#         height: 40px;
#         border-radius: 50%;
#         margin-right: 10px;
#         overflow: hidden;
#     }
#     .chat-icon img {
#         width: 100%;
#         height: 100%;
#         object-fit: cover;
#     }
#     .user-message {
#         background-color: #007BFF; /* Blue background */
#         border-radius: 10px;
#         padding: 10px;
#         margin: 5px 0;
#         color: white; /* White text color */
#         font-size: 16px;
#         line-height: 1.5;
#         max-width: 80%;
#         word-wrap: break-word;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Display the heading at the center
# st.markdown("<div class='center-heading'>Tech Resume Crafter</div>", unsafe_allow_html=True)

# # Initialize session state for chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []  # List to store chat messages

# # Function to add messages to the chat
# def add_message(role, content):
#     st.session_state.messages.append({"role": role, "content": content})

# # Custom user icon URL
# USER_ICON_URL = "https://media.licdn.com/dms/image/v2/D560BAQHl70ESPZeYlw/company-logo_200_200/company-logo_200_200/0/1704214380639?e=1743033600&v=beta&t=zN3f1pPCbkuk5T0zq3mRGjF2p7rYWSDiEn03xJ0n1P0"

# # Render all chat messages
# for msg in st.session_state.messages:
#     if msg["role"] == "user":
#         st.markdown(f"""
#             <div class="chat-container">
#                 <div class="chat-icon">
#                     <img src="{USER_ICON_URL}" alt="User Icon">
#                 </div>
#                 <div class="user-message">{msg['content']}</div>
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

# # Input for user to type a message
# if user_input := st.chat_input("Type your message here..."):
#     add_message("user", user_input)  # Add user's message to history

#     # Display the user's message with custom styling and image
#     st.markdown(f"""
#         <div class="chat-container">
#             <div class="chat-icon">
#                 <img src="{USER_ICON_URL}" alt="User Icon">
#             </div>
#             <div class="user-message">{user_input}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     # Prepare messages for the assistant
#     system_prompt = "You are a specialized AI designed to generate tailored, high-impact technical resume content for job seekers applying to various tech roles. Your primary goal is to create unique, detailed, and role-specific project descriptions or experience summaries whose total ATS score according to JD should be greater than 95 out of 100. Follow these instructions carefully: 1. Gather Initial Information: * Ask for the Job Description (JD): Prompt the user to provide the complete JD for the role they are targeting. * Job Level Analysis: Determine if the JD is for a junior-level or senior-level position. * For junior roles, focus on creating projects from scratch to showcase technical expertise. * For senior roles, emphasize improvements and optimizations made to existing systems to highlight leadership and innovation. 2. Tech Stack Extraction: * Analyze the JD to identify the key technical stacks (programming languages, frameworks, tools, etc.) associated with the role. * Suggest additional or complementary technologies that might be required to complete the project fully. * Ensure these tools are aligned with the company's ecosystem (e.g., if the company uses Azure, avoid suggesting AWS). 3. Project Details Collection: * Ask the user for the project title and a brief description of the project they want to include in the resume. * Based on the provided tech stack and project description, generate the following content: * Problem Statement: Clearly define the issue the project addresses. * Approach: Explain the steps and strategies used to develop the project. * Experience Bullet Points: Describe the project in detail using bullet points. 4. Content Guidelines: * Avoid Redundant Tools: Do not include technologies that serve the same purpose in a single project (e.g., avoid pairing MySQL and PostgreSQL in the same context unless justified). * Unique Content: Ensure each bullet point is distinct, avoiding repetitive phrasing and ideas. * Technical Language: Use precise and advanced technical terminology to describe tools, methodologies, and outcomes. * Bullet Point Format: * Provide 15 to 25 bullet points per project each bullet point. * Each bullet point should be 2 to 3 lines without subheading. * No subheadings within the bullet points. 5. Role-Specific Focus: * For junior-level roles, emphasize: * Developing projects from the ground up. * Demonstrating technical skills, problem-solving abilities, and a thorough understanding of the development process. * For senior-level roles, highlight: * Enhancements made to existing systems. * Efficiency improvements, scalability, and technical leadership. * Contributions to the company's workflow optimization or system architecture. 6. Provide ATS Evaluation: Review the Generated Content against the JD to provide an ATS score and feedback. Follow this structure: 1. Percentage Match: Calculate and display the percentage match between the content and the JD. 2. Missing Keywords: Identify important keywords or skills missing from the content that are present in the JD. 3. Final Thoughts: Provide an evaluation summary highlighting the strengths and weaknesses of the generated content in relation to the JD."
#     conversation = [{"role": "system", "content": system_prompt}] + st.session_state.messages

#     # Display a placeholder while generating the assistant's response
#     with st.chat_message("assistant"):
#         response_placeholder = st.empty()
#         with st.spinner("Crafting a response..."):
#             try:
#                 # Call OpenAI API
#                 response = openai.ChatCompletion.create(
#                     model="gpt-4",
#                     messages=conversation,
#                     max_tokens=1000,
#                 )
#                 assistant_message = response.choices[0].message.content.strip()
#             except Exception as e:
#                 assistant_message = f"An error occurred: {e}"

#             # Replace the placeholder with the actual response
#             response_placeholder.markdown(assistant_message)

#     # Add assistant's response to the message history
#     add_message("assistant", assistant_message)


import os
import openai
import streamlit as st
from dotenv import load_dotenv
from groq import Groq  # Import Groq client for LLAMA model

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Streamlit page configuration
st.set_page_config(
    page_title="Tech Resume Crafter",
    page_icon="\U0001F4BC",
    layout="wide",
)

# Add custom CSS for centering the heading and styling user messages
st.markdown("""
    <style>
    .center-heading {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: white;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .chat-container {
        display: flex;
        align-items: flex-start;
        margin: 10px 0;
    }
    .chat-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
        overflow: hidden;
    }
    .chat-icon img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .user-message {
        background-color: #007BFF;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        color: white;
        font-size: 16px;
        line-height: 1.5;
        max-width: 80%;
        word-wrap: break-word;
    }
    </style>
    """, unsafe_allow_html=True)

# Display the heading at the center
st.markdown("<div class='center-heading'>Tech Resume Crafter</div>", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # List to store chat messages

# Function to add messages to the chat
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# Custom user icon URL
USER_ICON_URL = "https://media.licdn.com/dms/image/v2/D560BAQHl70ESPZeYlw/company-logo_200_200/company-logo_200_200/0/1704214380639?e=1743033600&v=beta&t=zN3f1pPCbkuk5T0zq3mRGjF2p7rYWSDiEn03xJ0n1P0"

# Model selection dropdown
model_option = st.sidebar.selectbox("Choose LLM Model", ["OpenAI", "LLAMA"])

# Function to handle message submission and generate a response
def generate_response(model, chat_history):
    if model == "OpenAI":
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=chat_history,
                max_tokens=10000,
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"An error occurred: {e}"
    elif model == "LLAMA":
        try:
            groq_client = Groq(api_key=groq_api_key)
            chat_completion = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=chat_history,
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"An error occurred: {e}"

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
            <div class="chat-container">
                <div class="chat-icon">
                    <img src="{USER_ICON_URL}" alt="User Icon">
                </div>
                <div class="user-message">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input for user to type a message
if user_input := st.chat_input("Type your message here..."):
    add_message("user", user_input)  # Add user's message to history

    # Display the user's message with custom styling and image
    st.markdown(f"""
        <div class="chat-container">
            <div class="chat-icon">
                <img src="{USER_ICON_URL}" alt="User Icon">
            </div>
            <div class="user-message">{user_input}</div>
        </div>
        """, unsafe_allow_html=True)

    # Prepare messages for the assistant, including the system prompt
    system_prompt = {"role": "system", "content": "TASK: You are a Resume Specialist for Tech Professionals. Your primary responsibility is to generate and modify resume content based on user-provided project information and tech stack details. USER INPUT: Ask for the Job Description (JD): Prompt the user to provide the complete JD for the role they are targeting. If User does not provide JD and provide some random input then answer that based on below instructions. INSTRUCTIONS: Generate all summaries and project information as bullet points (Do not include Sub-headings). Project Summary should include 10-15 bullet points (approximately 30-40 words in each bullet point). User Summary should include 5-6 bullet points (approximately 30-40 words in each bullet point). Use multiple related technologies within a single bullet point where applicable. Avoid repeating the same skill or technology within a single project. Ensure compatibility of technologies (e.g., use Python with Django or Flask, but not both Django and Flask in the same project). Incorporate numbers or quantifiable achievements in the last 2-3 bullet points to highlight successes (To increase ATS score efficiency). Avoidance: Do not use numbers in the initial bullet points. Use natural, human-readable English and avoid overly perfect or artificial language. Incorporate relevant technical terms appropriately to demonstrate expertise. Analyze the provided JD for keywords and required skills (if provided). If the company’s tech stack is provided, prioritize using those tools and technologies. If not provided, default to industry-standard tools relevant to the technologies used in the projects. Include additional technologies or tools that enhance the project's technical completeness, scalability, or deployment. NOTE: Make sure you follow above instructions every time while giving response. .If user ask for resume then give the complete resume including each section under 1800 words."}

    chat_history = [system_prompt] + st.session_state.messages

    # Display a placeholder while generating the assistant's response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("Crafting a response..."):
            response = generate_response(model_option, chat_history)

            # Replace the placeholder with the actual response
            response_placeholder.markdown(response)

    # Add assistant's response to the message history
    add_message("assistant", response)







