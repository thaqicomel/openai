import streamlit as st
from openai import OpenAI
import re

def course_match_bot(user_info, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    
    # Combine all user inputs into one prompt
    prompt = f"User Information: {user_info}"

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in providing career choices and please give 3 recommendation"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def my_ambition(ambition_info, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    
    # Combine all user inputs into one prompt
    prompt = f"User Information: {ambition_info}"

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in giving motivation.Please give the 1 suitable career"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def character_bot(character_info, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    
    # Combine all user inputs into one prompt
    prompt = f"User Information: {character_info}"

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant in analysing user character.Please give about 5 scenarios for user to choose if it allign with him or not"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def finalize_character(character_info, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    
    # Combine all user inputs into one prompt
    prompt = f"User Persronality: {character_info}"

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant in analysing user Personality based on their answer ang give answer what kind of personality user have"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


# Streamlit application
st.title("💬 Course Match Bot")

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    st.write("Get personalized career suggestions based on your interests and strengths.")

    # Initialize session state for form submission and ambition display
    if 'show_ambition' not in st.session_state:
        st.session_state.show_ambition = False

    if 'show_character' not in st.session_state:
        st.session_state.show_character = False  

    if 'show_suggestion' not in st.session_state:
        st.session_state.show_suggestion = False      
    
    with st.form(key="career_suggestion_form"):
        # Collecting user input for career suggestion
        subject_like = st.text_input("Tell me about yourself. What subject do you like in school and do well?")
        like_not = st.radio("Do you like it?", ["I Like but I don't do well", "I don't like but I do well", "I like and I do well", "I have no interest at all"])

        submit_button = st.form_submit_button(label="Enter")

        if submit_button:
            if subject_like and like_not:
                # Combine all inputs into a single string
                user_info = f"Subject the user likes: {subject_like}, Do I like the subject?: {like_not}"
                suggestions = course_match_bot(user_info, openai_api_key)
                st.write("Here are some career suggestions for you:")
                st.write(suggestions)

                st.session_state.subject_like = subject_like
                st.session_state.like_not = like_not
                st.session_state.show_ambition = True
            else:
                st.warning("Please fill in all fields to receive suggestions.")

    # Display second form if the user has submitted the first form
    if st.session_state.show_ambition:
        with st.form(key="ambition_form"):
            ambition = st.text_input("What are your career ambitions or goals?")            
            submit_button_ambition = st.form_submit_button(label="Submit Ambition")
        

            if submit_button_ambition:
                ambition_info = f"Type of ambition the user want:{ambition}, The subject the user choose: {subject_like}, User Opinion on the subject"
                ambi_suggestion = course_match_bot(ambition_info, openai_api_key)
                st.write("Based on your ambition this is the new career that we will propose")
                st.write(ambi_suggestion)

                st.session_state.subject_like = subject_like
                st.session_state.like_not = like_not
                st.session_state.ambition = ambition
                st.session_state.show_character = True
            else:
                st.warning("Please put your ambition")

    if st.session_state.show_character:
        with st.form(key="character_form"):
            character = st.text_input("Can you describe your character") 
            introvert_not = st.radio("Are you an introvert or extrovert", ["I am an Introvert", "I am an Extrovert"])           
            submit_button_character = st.form_submit_button(label="Submit your character")
        

            if submit_button_character:
                character_info = f"This is what I think my character is like: {character}, I am a {introvert_not}"
                character_suggestion = character_bot(character_info, openai_api_key)
                
                st.session_state.character_suggestion = ambition
                st.session_state.show_suggestion = True

                # # Use regex to split suggestions by numbers if they are formatted as "1. ", "2. ", etc.
                # suggestions = re.split(r"\d+\.\s", character_suggestion)[1:]  # Skip the first split item as it's empty

                # # Display each suggestion with an input box beside it
                # for i, suggestion in enumerate(suggestions, start=1):
                #     st.write(f"{i}. {suggestion}")
                #     st.text_input(f"Your thoughts on suggestion {i}:", key=f"suggestion_input_{i}")

                # # Store user input for each suggestion in session state
                # st.session_state.character_suggestions = {
                #     f"suggestion_input_{i}": st.session_state.get(f"suggestion_input_{i}", "") for i in range(1, len(suggestions) + 1)
                # }

    if st.session_state.show_suggestion:
        with st.form(key="suggestion_form"):
            responses_array = []
            st.write("Based on your character, here are some scenarios for you to consider:")

            suggestions = re.split(r"\d+\.\s", character_suggestion)[1:]

            for i, suggestion in enumerate(suggestions, start=1):
                st.write(f"{i}. {suggestion}")
                user_response = st.text_input(f"Your thoughts on suggestion {i}:", key=f"suggestion_input_{i}")
                responses_array.append(user_response)

            submit_button_suggestion = st.form_submit_button(label="Submit your answer")

        if submit_button_suggestion:
            fcharacter_suggestion = finalize_character(responses_array, openai_api_key)
            st.write("Our Opinion:")
            st.write(fcharacter_suggestion)
