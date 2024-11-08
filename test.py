import streamlit as st
from openai import OpenAI


# client = OpenAI(api_key="")

def course_match_bot(user_info,openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    # Ask Question
    # user_info = input("What subjects do you like in school that you think you do reasonably well (or at least above average) at the same time? Explain why in less than 20 words: ")

    # #generate prompt dari user
    prompt = f"Suggest at least 5 career choices based on this: {user_info}. For each career, provide a brief description more than 55 words explaining why it fits well."

    #Print output
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in giving answer for career choices and all description must be more than 60 words"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

    # Output
    # print("Here are some courses that I may suggest for you")
    # print(completion.choices[0].message.content)

    # prompt = f"Suggest 1 of the most suitable carrer based on this: {user_info}"
    # # ni add-on
    # completion = client.chat.completions.create(

    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant specialized in suggesting what carier is suitable for the user"},
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # print("\nIf you are looking career transaction, here is my recommendation:\n")
    # print(completion.choices[0].message.content)

# course_match_bot()

#streamlit application
st.title("💬Course Match Bot")
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    st.write("Get personalized career suggestions based on your interests and strengths.")

# Get user input
    with st.form(key="career_suggestion_form"):
        # User input for subjects and interests
        user_info = st.text_input("What subjects do you like in school that you think you do reasonably well (or at least above average) at the same time? Explain why in less than 20 words:")

        # Automatically submit the form when pressing Enter
        submit_button = st.form_submit_button(label="Get Career Suggestions")

        if submit_button:
            # Generate career suggestions if input is provided
            if user_info:
                suggestions = course_match_bot(user_info, openai_api_key)
                st.write("Here are some courses that I may suggest for you:")
                st.write(suggestions)
            else:
                st.warning("Please enter dulu")
