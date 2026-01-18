import streamlit as st
import requests
import pandas as pd

# Page configuration
st.set_page_config(page_title="AI Knowledge Gap Analyzer", layout="centered")

# Header
st.markdown(
    "<h1 style='text-align: center; color: #4B0082;'>🧠 AI Knowledge Gap Analyzer</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# Friendly intro
st.write(
    "Hi there! 👋 I can help you understand your current skills, "
    "highlight the ones you need to learn, and give you a personalized learning roadmap. "
    "Let's get started!"
)

# Inputs
user_name = st.text_input("What's your name?", placeholder="Your name here")
user_skills_input = st.text_input(
    "Enter your skills (comma separated)",
    placeholder="Python, SQL, Git"
)

# Job roles
target_role = st.selectbox(
    "Select the job role you want to target",
    [
        "Python Developer",
        "Data Analyst",
        "Web Developer",
        "Machine Learning Engineer",
        "Cloud Engineer",
        "Cybersecurity Analyst",
        "DevOps Engineer",
        "AI Researcher",
        "Mobile App Developer"
    ]
)

# Button
if st.button("Analyze My Skills"):
    if not user_skills_input or not user_name:
        st.warning("Please enter your name and at least one skill to continue.")
    else:
        user_skills = [skill.strip() for skill in user_skills_input.split(",")]
        data = {"user_skills": user_skills, "target_role": target_role}

        try:
            response = requests.post("http://127.0.0.1:5000/analyze", json=data)
            result = response.json()

            # Personalized greeting
            st.success(f"Hi {user_name}! Here's your skill analysis for the role: **{target_role}** 🎯")

            # Readiness score
            st.subheader("\U0001F393 Readiness Score")
            st.write(f"You are currently **{result['readiness_score']}%** ready for this role.")
            st.progress(result["readiness_score"] / 100)
            st.bar_chart([result["readiness_score"], 100 - result["readiness_score"]],
                         use_container_width=True)

            # Matched Skills
            st.subheader("✅ Skills You Already Have")
            if result["matched_skills"]:
                st.info(f"Awesome! You already know: {', '.join(result['matched_skills'])} 🎉")
            else:
                st.warning("It looks like you haven't covered any core skills yet, but no worries! 💪")

            # Missing Skills
            st.subheader("⚠️ Skills You Might Need")
            if result["missing_skills"]:
                st.error(f"You should focus on: {', '.join(result['missing_skills'])} 🔑")
            else:
                st.success("You have all the essential skills for this role! 🎉")

            # Learning Roadmap with Resources using expanders
            st.subheader("Personalized Learning Roadmap")
            if result["roadmap"]:
                st.write("Here’s a roadmap to help you close your skill gaps:")

                for item in result["roadmap"]:
                    with st.expander(f"{item['skill'].title()}"):
                        st.write(item["suggestion"])
                        if item.get("links"):
                            for link in item["links"]:
                                st.markdown(f"- [🔗 Learn Here]({link})")
            else:
                st.info("No roadmap available.")

        except Exception as e:
            st.error(
                "Oops! Could not connect to backend. Make sure Flask is running.\n"
                f"Error: {e}"
            )
