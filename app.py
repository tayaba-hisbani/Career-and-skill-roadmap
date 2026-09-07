import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Career Roadmap",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Skill Gap & Career Roadmap")
st.write("Build a personalized career direction, skill-gap analysis, and learning roadmap.")

# ---------- API ----------
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY is not set. Add your Groq API key as an environment variable/secrets before generating a roadmap.")
    st.stop()

client = Groq(api_key=api_key)

# ---------- Profile ----------
st.header("1. Create Your Profile")

col1, col2 = st.columns(2)

with col1:
    degree = st.text_input("Degree", placeholder="e.g., BBA")
    university = st.text_input("University", placeholder="e.g., SZABIST")
    semester = st.text_input("Semester / Year", placeholder="e.g., 5th semester")
    interests = st.text_area(
        "Interests",
        placeholder="e.g., finance, AI, business analytics, marketing"
    )

with col2:
    current_skills = st.text_area(
        "Current Skills",
        placeholder="e.g., Excel, communication, basic Python"
    )
    career_goals = st.text_area(
        "Career Goals",
        placeholder="e.g., become a business analyst in 1–2 years"
    )
    study_time = st.number_input(
        "Available study time (hours per week)",
        min_value=1,
        max_value=60,
        value=7
    )

st.header("2. Choose Your Target Domain")

domain = st.text_input(
    "Field / Domain / Interest",
    placeholder="e.g., Business Analytics, AI, Digital Marketing, Finance"
)

level = st.selectbox(
    "Current Skill Level",
    ["Beginner", "Intermediate", "Advanced"]
)

learning_time = st.selectbox(
    "Time You Want to Spend Learning",
    ["1 month", "3 months", "6 months", "12 months", "2+ years"]
)

generate = st.button("🚀 Generate My Career Roadmap", type="primary", use_container_width=True)

# ---------- AI ----------
def generate_roadmap(profile, domain, level, learning_time):
    system_prompt = """
You are an expert AI career counselor and learning-roadmap designer.

Your job is to help university students make realistic career decisions.
Use the student's degree, university context, semester/year, interests,
current skills, career goals, available study time, target domain,
current level, and learning duration.

Do NOT pretend to know the student's exact job market or guarantee employment.
Clearly distinguish recommendations from guarantees.

Return a practical answer with these sections:

1. Career Direction
2. Why This Direction Fits
3. Recommended Career Roles
4. Skill Gap Analysis
   - Current/likely strengths
   - Skills to improve
   - New skills required
5. Personalized Learning Roadmap
   - Phase
   - Skills/topics
   - Practical project
   - Suggested time
6. Weekly Study Plan
7. Portfolio Projects
8. Internship/Job Preparation
9. Recommended Free/Low-Cost Learning Resources
10. Next 3 Actions

Keep the language simple and student-friendly.
Prioritize practical skills and projects.
Do not invent exact course URLs.
"""

    user_prompt = f"""
STUDENT PROFILE
Degree: {profile['degree']}
University: {profile['university']}
Semester/Year: {profile['semester']}
Interests: {profile['interests']}
Current Skills: {profile['current_skills']}
Career Goals: {profile['career_goals']}
Available Study Time: {profile['study_time']} hours/week

TARGET
Domain: {domain}
Current Level: {level}
Learning Duration: {learning_time}

Create a personalized career and skill-gap roadmap.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4,
        max_completion_tokens=5000
    )

    return response.choices[0].message.content

# ---------- Output ----------
if generate:
    if not degree or not interests or not current_skills or not career_goals or not domain:
        st.warning("Please complete the main profile fields and target domain first.")
    else:
        profile = {
            "degree": degree,
            "university": university,
            "semester": semester,
            "interests": interests,
            "current_skills": current_skills,
            "career_goals": career_goals,
            "study_time": study_time
        }

        with st.spinner("Analyzing your profile and building your roadmap..."):
            try:
                result = generate_roadmap(
                    profile, domain, level, learning_time
                )

                st.success("Your personalized roadmap is ready!")
                st.markdown(result)

                st.download_button(
                    "⬇️ Download Roadmap",
                    data=result,
                    file_name="career_roadmap.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.divider()
st.caption("AI-generated guidance is for educational and career-planning purposes. Always verify current job requirements and learning resources.")
