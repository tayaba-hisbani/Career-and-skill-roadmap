import os
import json
import html
import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Career & Skill Roadmap",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Main title */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        font-size: 1.15rem;
        color: #666;
        margin-bottom: 1.5rem;
    }

    /* Section headers */
    .section-title {
        font-size: 1.7rem;
        font-weight: 750;
        margin-top: 1.5rem;
        margin-bottom: 0.7rem;
    }

    /* Info cards */
    .info-card {
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
        background-color: #fafafa;
    }

    .info-card h3 {
        margin-top: 0;
    }

    /* Priority cards */
    .priority-high {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #d32f2f;
        background-color: #fff5f5;
        margin-bottom: 0.8rem;
    }

    .priority-medium {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f9a825;
        background-color: #fffaf0;
        margin-bottom: 0.8rem;
    }

    .priority-low {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #388e3c;
        background-color: #f4fff4;
        margin-bottom: 0.8rem;
    }

    /* Result cards */
    .result-card {
        padding: 1.3rem;
        border-radius: 12px;
        border: 1px solid #ddd;
        background-color: #ffffff;
        margin-bottom: 1rem;
    }

    /* Fit score */
    .fit-score {
        text-align: center;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #ddd;
        background-color: #fafafa;
    }

    .fit-number {
        font-size: 3rem;
        font-weight: 800;
    }

    .fit-label {
        font-size: 1rem;
        color: #666;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777;
        font-size: 0.85rem;
        margin-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎯 AI Career & Skill Roadmap</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Discover a realistic career direction, identify your skill gaps,
    and build a personalized learning roadmap.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HOW IT WORKS
# ============================================================

with st.expander("💡 How does this work?", expanded=True):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### 1️⃣")
        st.write("Create your student profile")

    with col2:
        st.markdown("### 2️⃣")
        st.write("Choose your target career")

    with col3:
        st.markdown("### 3️⃣")
        st.write("AI analyzes your skill gaps")

    with col4:
        st.markdown("### 4️⃣")
        st.write("Get your personalized roadmap")


st.divider()


# ============================================================
# API CONFIGURATION
# ============================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(
        "⚠️ GROQ_API_KEY is not configured. "
        "Add your Groq API key to your Streamlit secrets/environment variables."
    )
    st.stop()

client = Groq(api_key=api_key)


# ============================================================
# PROFILE SECTION
# ============================================================

st.markdown(
    '<div class="section-title">👤 1. Create Your Profile</div>',
    unsafe_allow_html=True
)

st.caption(
    "Tell us about your education, current skills, interests and career goals."
)

col1, col2 = st.columns(2)


with col1:

    degree = st.text_input(
        "🎓 Degree *",
        placeholder="Example: BBA"
    )

    university = st.text_input(
        "🏫 University / Institution *",
        placeholder="Example: SZABIST"
    )

    semester = st.text_input(
        "📚 Current Study Level *",
        placeholder="Example: 3rd year / 5th semester"
    )

    interests = st.text_area(
        "💡 Interests *",
        placeholder=(
            "Example: finance, AI, data analytics, "
            "business, marketing"
        ),
        height=120
    )


with col2:

    current_skills = st.text_area(
        "🛠️ Current Skills *",
        placeholder=(
            "Example: Excel, communication, basic Python, "
            "accounting"
        ),
        height=120
    )

    career_goals = st.text_area(
        "🎯 Career Goal *",
        placeholder=(
            "Example: I want to become a Business Analyst "
            "within 2 years."
        ),
        height=120
    )

    study_time = st.number_input(
        "⏰ Available Learning Time (hours/week)",
        min_value=1,
        max_value=60,
        value=5,
        step=1
    )


# ============================================================
# TARGET CAREER SECTION
# ============================================================

st.markdown(
    '<div class="section-title">🎯 2. Choose Your Target Career</div>',
    unsafe_allow_html=True
)

st.caption(
    "Choose the career you want to explore. If it isn't listed, select Other."
)

career_options = [
    "Business Analyst",
    "Data Analyst",
    "Financial Analyst",
    "Marketing Analyst",
    "HR Analyst",
    "Product Manager",
    "Project Manager",
    "AI / Data",
    "Digital Marketing",
    "Finance",
    "Other"
]

domain_choice = st.selectbox(
    "Target Career / Domain *",
    career_options
)

if domain_choice == "Other":

    custom_domain = st.text_input(
        "Enter your target career/domain *",
        placeholder="Example: Supply Chain Analyst"
    )

    domain = custom_domain.strip()

else:

    domain = domain_choice


level = st.selectbox(
    "📊 Current Skill Level *",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


learning_time = st.selectbox(
    "📅 Time You Want to Spend Learning *",
    [
        "1 month",
        "3 months",
        "6 months",
        "12 months",
        "2+ years"
    ]
)


st.divider()


# ============================================================
# GENERATE BUTTON
# ============================================================

generate = st.button(
    "🚀 Generate My Personalized Roadmap",
    type="primary",
    use_container_width=True
)


# ============================================================
# AI FUNCTION
# ============================================================

def generate_roadmap(profile, domain, level, learning_time):

    system_prompt = """
You are an expert AI career counselor, business analyst career advisor,
and learning-roadmap designer.

Your task is to create a realistic, practical and highly personalized
career and skill roadmap for a university student.

IMPORTANT RULES:

1. Use ONLY information explicitly provided by the student when describing
   their current skills, experience, education or strengths.

2. If you infer something, clearly label it as an AI inference or recommendation.

3. Do not claim that the student has a skill that they did not mention.

4. Do not guarantee employment, salary, promotions or career success.

5. Do not invent exact job-market statistics.

6. Do not invent exact course URLs.

7. Recommend free or low-cost learning resources by NAME only unless a URL
   is explicitly known with confidence.

8. Make the roadmap practical and suitable for a university student.

9. Consider the student's available study time.

10. Do not give the student an unrealistic number of skills to learn at once.

11. Prioritize the most important skills first.

12. Make the recommendations specific to the student's target career,
    current skills, interests and learning duration.

13. The roadmap should help the student build a portfolio and become
    internship/job ready.

CAREER FIT SCORE:

Provide an AI-estimated career fit score from 0 to 100.

This is NOT a scientific assessment.

The score should be based on:
- Alignment between current skills and target career
- Relevant education
- Relevant interests
- Career goal
- Skill gaps

Use the score only as a rough planning indicator.

SKILL PRIORITY:

Every important missing skill should have:
- Current level
- Target level
- Priority: High / Medium / Low
- Reason

ROADMAP:

Create phases appropriate to the student's selected learning duration.

Each phase should contain:
- Time period
- Skills/topics
- Practical learning activities
- Portfolio project
- Suggested weekly time

WEEKLY PLAN:

Adapt the weekly schedule to the student's available hours.

PORTFOLIO:

Recommend realistic projects that a student can actually complete.

RESOURCES:

Recommend resource names such as:
- Kaggle Learn
- Microsoft Learn
- Tableau Public
- YouTube
- OpenLearn
- Coursera
or other appropriate resources.

Do not fabricate exact links.

RETURN FORMAT:

Return ONLY valid JSON.

Use exactly this structure:

{
  "career_direction": "",
  "career_fit_score": 0,
  "fit_explanation": "",
  "recommended_roles": [
    {
      "role": "",
      "why": "",
      "key_skills": []
    }
  ],
  "current_strengths": [
    {
      "skill": "",
      "reason": ""
    }
  ],
  "skill_gaps": [
    {
      "skill": "",
      "current_level": "",
      "target_level": "",
      "priority": "High",
      "why": ""
    }
  ],
  "top_3_priorities": [
    {
      "skill": "",
      "why": "",
      "first_step": ""
    }
  ],
  "learning_roadmap": [
    {
      "phase": "",
      "timeframe": "",
      "skills": [],
      "practical_work": "",
      "portfolio_project": "",
      "suggested_hours": ""
    }
  ],
  "weekly_plan": [
    {
      "day": "",
      "activity": "",
      "hours": ""
    }
  ],
  "portfolio_projects": [
    {
      "project": "",
      "difficulty": "",
      "tools": [],
      "description": "",
      "portfolio_output": ""
    }
  ],
  "learning_resources": [
    {
      "skill": "",
      "resources": [],
      "how_to_use": ""
    }
  ],
  "internship_job_preparation": [
    ""
  ],
  "next_3_actions": [
    ""
  ],
  "disclaimer": ""
}

Keep the language simple, clear and student-friendly.
"""


    user_prompt = f"""
STUDENT PROFILE

Degree:
{profile['degree']}

University:
{profile['university']}

Current Study Level:
{profile['semester']}

Interests:
{profile['interests']}

Current Skills:
{profile['current_skills']}

Career Goals:
{profile['career_goals']}

Available Learning Time:
{profile['study_time']} hours/week


TARGET CAREER

Target Career / Domain:
{domain}

Current Skill Level:
{level}

Learning Duration:
{learning_time}


TASK

Analyze this student's profile.

Identify:
1. The most suitable career direction related to their target.
2. Why it fits their current background.
3. Suitable entry-level career roles.
4. Their stated strengths.
5. Their skill gaps.
6. Which skills should be learned first.
7. A realistic learning roadmap.
8. A weekly learning plan based on their available hours.
9. Portfolio projects.
10. Free or low-cost resource names.
11. Internship/job preparation actions.
12. The next three actions they should take.

Make the result genuinely personalized.
"""


    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.3,
        max_completion_tokens=6000
    )

    return response.choices[0].message.content


# ============================================================
# JSON CLEANING FUNCTION
# ============================================================

def parse_json_response(raw_response):

    cleaned = raw_response.strip()

    # Remove markdown code fences if the model adds them
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]

    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()

    return json.loads(cleaned)


# ============================================================
# MARKDOWN REPORT GENERATOR
# ============================================================

def create_markdown_report(data, profile, domain, level, learning_time):

    report = []

    report.append("# 🎯 Personalized Career & Skill Roadmap")
    report.append("")

    report.append("## Student Profile")
    report.append("")
    report.append(f"- **Degree:** {profile['degree']}")
    report.append(f"- **University:** {profile['university']}")
    report.append(f"- **Study Level:** {profile['semester']}")
    report.append(f"- **Interests:** {profile['interests']}")
    report.append(f"- **Current Skills:** {profile['current_skills']}")
    report.append(f"- **Career Goal:** {profile['career_goals']}")
    report.append(f"- **Available Study Time:** {profile['study_time']} hours/week")
    report.append(f"- **Target Career:** {domain}")
    report.append(f"- **Current Level:** {level}")
    report.append(f"- **Learning Duration:** {learning_time}")
    report.append("")

    report.append("## 🎯 Career Direction")
    report.append("")
    report.append(data.get("career_direction", ""))
    report.append("")

    report.append("## 📊 AI-Estimated Career Fit")
    report.append("")
    report.append(
        f"**{data.get('career_fit_score', 0)} / 100**"
    )
    report.append("")
    report.append(data.get("fit_explanation", ""))
    report.append("")
    report.append(
        "*This score is an AI-generated planning estimate, not a scientific "
        "or professional career assessment.*"
    )
    report.append("")

    report.append("## 💼 Recommended Career Roles")
    report.append("")

    for role in data.get("recommended_roles", []):
        report.append(f"### {role.get('role', '')}")
        report.append("")
        report.append(f"**Why:** {role.get('why', '')}")
        report.append("")
        report.append(
            "**Key Skills:** "
            + ", ".join(role.get("key_skills", []))
        )
        report.append("")

    report.append("## 🛠️ Current Strengths")
    report.append("")

    for item in data.get("current_strengths", []):
        report.append(
            f"- **{item.get('skill', '')}:** "
            f"{item.get('reason', '')}"
        )

    report.append("")

    report.append("## 📊 Skill Gap Analysis")
    report.append("")

    for item in data.get("skill_gaps", []):

        priority = item.get("priority", "Medium")

        report.append(
            f"### {item.get('skill', '')} — {priority} Priority"
        )

        report.append(
            f"- Current level: {item.get('current_level', '')}"
        )

        report.append(
            f"- Target level: {item.get('target_level', '')}"
        )

        report.append(
            f"- Why it matters: {item.get('why', '')}"
        )

        report.append("")

    report.append("## 🚀 Start Here — Top 3 Priorities")
    report.append("")

    for index, item in enumerate(
        data.get("top_3_priorities", []),
        start=1
    ):

        report.append(
            f"### {index}. {item.get('skill', '')}"
        )

        report.append(
            f"**Why:** {item.get('why', '')}"
        )

        report.append(
            f"**First step:** {item.get('first_step', '')}"
        )

        report.append("")

    report.append("## 📚 Personalized Learning Roadmap")
    report.append("")

    for phase in data.get("learning_roadmap", []):

        report.append(
            f"### {phase.get('phase', '')}"
        )

        report.append(
            f"**Timeframe:** {phase.get('timeframe', '')}"
        )

        report.append(
            f"**Skills:** {', '.join(phase.get('skills', []))}"
        )

        report.append(
            f"**Practical Work:** {phase.get('practical_work', '')}"
        )

        report.append(
            f"**Portfolio Project:** "
            f"{phase.get('portfolio_project', '')}"
        )

        report.append(
            f"**Suggested Time:** "
            f"{phase.get('suggested_hours', '')}"
        )

        report.append("")

    report.append("## 🗓️ Weekly Study Plan")
    report.append("")

    for day in data.get("weekly_plan", []):

        report.append(
            f"- **{day.get('day', '')}:** "
            f"{day.get('activity', '')} "
            f"({day.get('hours', '')})"
        )

    report.append("")

    report.append("## 💼 Portfolio Projects")
    report.append("")

    for project in data.get("portfolio_projects", []):

        report.append(
            f"### {project.get('project', '')}"
        )

        report.append(
            f"- **Difficulty:** {project.get('difficulty', '')}"
        )

        report.append(
            f"- **Tools:** "
            f"{', '.join(project.get('tools', []))}"
        )

        report.append(
            f"- **Description:** "
            f"{project.get('description', '')}"
        )

        report.append(
            f"- **Portfolio Output:** "
            f"{project.get('portfolio_output', '')}"
        )

        report.append("")

    report.append("## 📖 Learning Resources")
    report.append("")

    for resource in data.get("learning_resources", []):

        report.append(
            f"### {resource.get('skill', '')}"
        )

        report.append(
            f"**Resources:** "
            f"{', '.join(resource.get('resources', []))}"
        )

        report.append(
            f"**How to use:** "
            f"{resource.get('how_to_use', '')}"
        )

        report.append("")

    report.append("## 💼 Internship / Job Preparation")
    report.append("")

    for item in data.get("internship_job_preparation", []):
        report.append(f"- {item}")

    report.append("")

    report.append("## 🚀 Your Next 3 Actions")
    report.append("")

    for index, action in enumerate(
        data.get("next_3_actions", []),
        start=1
    ):
        report.append(f"{index}. {action}")

    report.append("")

    report.append("## ⚠️ Disclaimer")
    report.append("")
    report.append(data.get("disclaimer", ""))

    return "\n".join(report)


# ============================================================
# HTML REPORT GENERATOR
# ============================================================

def create_html_report(markdown_text):

    safe_text = html.escape(markdown_text)

    html_report = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<title>Personalized Career & Skill Roadmap</title>

<style>

body {{
    font-family: Arial, sans-serif;
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
    line-height: 1.6;
    color: #222;
}}

h1 {{
    font-size: 32px;
}}

h2 {{
    margin-top: 35px;
}}

h3 {{
    margin-top: 25px;
}}

pre {{
    white-space: pre-wrap;
    font-family: Arial, sans-serif;
}}

.footer {{
    margin-top: 40px;
    color: #777;
    font-size: 13px;
}}

</style>

</head>

<body>

<pre>{safe_text}</pre>

<div class="footer">
Generated by AI Career & Skill Roadmap.
</div>

</body>
</html>
"""

    return html_report


# ============================================================
# MAIN GENERATION LOGIC
# ============================================================

if generate:

    required_fields = {
        "Degree": degree.strip(),
        "University": university.strip(),
        "Study Level": semester.strip(),
        "Interests": interests.strip(),
        "Current Skills": current_skills.strip(),
        "Career Goal": career_goals.strip(),
        "Target Career": domain.strip()
    }

    missing_fields = [
        name
        for name, value in required_fields.items()
        if not value
    ]

    if missing_fields:

        st.warning(
            "⚠️ Please complete the following required fields:"
        )

        for field in missing_fields:
            st.write(f"• {field}")

    else:

        profile = {
            "degree": degree.strip(),
            "university": university.strip(),
            "semester": semester.strip(),
            "interests": interests.strip(),
            "current_skills": current_skills.strip(),
            "career_goals": career_goals.strip(),
            "study_time": study_time
        }

        with st.spinner(
            "🔎 Analyzing your profile, identifying skill gaps, "
            "and building your roadmap..."
        ):

            try:

                raw_result = generate_roadmap(
                    profile,
                    domain,
                    level,
                    learning_time
                )

                data = parse_json_response(raw_result)

                st.session_state["roadmap_data"] = data
                st.session_state["roadmap_profile"] = profile
                st.session_state["roadmap_domain"] = domain
                st.session_state["roadmap_level"] = level
                st.session_state["roadmap_learning_time"] = learning_time

                st.success(
                    "✅ Your personalized roadmap is ready!"
                )

            except json.JSONDecodeError:

                st.error(
                    "⚠️ The AI returned an unexpected format. "
                    "Please try generating the roadmap again."
                )

            except Exception as e:

                st.error(
                    "⚠️ Something went wrong while generating "
                    "your roadmap."
                )

                st.caption(
                    "Technical details: "
                    + str(e)
                )


# ============================================================
# DISPLAY STORED RESULTS
# ============================================================

if "roadmap_data" in st.session_state:

    data = st.session_state["roadmap_data"]

    profile = st.session_state["roadmap_profile"]

    domain = st.session_state["roadmap_domain"]

    level = st.session_state["roadmap_level"]

    learning_time = st.session_state["roadmap_learning_time"]


    st.divider()

    st.markdown(
        '<div class="section-title">📋 Your Personalized Results</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # CAREER DIRECTION + FIT SCORE
    # ========================================================

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown("### 🎯 Career Direction")

        st.info(
            data.get(
                "career_direction",
                "No career direction was generated."
            )
        )

        st.markdown("### 💡 Why This Direction Fits")

        st.write(
            data.get(
                "fit_explanation",
                ""
            )
        )


    with col2:

        score = data.get(
            "career_fit_score",
            0
        )

        try:
            score = int(score)
        except:
            score = 0

        score = max(0, min(100, score))

        st.markdown(
            f"""
            <div class="fit-score">

            <div class="fit-number">
            {score}%
            </div>

            <div class="fit-label">
            AI-Estimated Career Fit
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "Planning estimate only — not a scientific assessment."
        )


    # ========================================================
    # RECOMMENDED ROLES
    # ========================================================

    st.markdown("### 💼 Recommended Career Roles")

    roles = data.get(
        "recommended_roles",
        []
    )

    if roles:

        role_columns = st.columns(
            min(len(roles), 3)
        )

        for index, role in enumerate(roles):

            with role_columns[index % len(role_columns)]:

                st.markdown(
                    f"""
                    <div class="result-card">

                    <h3>
                    {html.escape(role.get('role', ''))}
                    </h3>

                    <p>
                    {html.escape(role.get('why', ''))}
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                skills = role.get(
                    "key_skills",
                    []
                )

                if skills:
                    st.write(
                        "**Key skills:** "
                        + ", ".join(skills)
                    )


    # ========================================================
    # SKILL GAP
    # ========================================================

    st.markdown("### 📊 Your Skill Gap")

    skill_gaps = data.get(
        "skill_gaps",
        []
    )

    if skill_gaps:

        for item in skill_gaps:

            skill = item.get(
                "skill",
                "Skill"
            )

            current = item.get(
                "current_level",
                "Not specified"
            )

            target = item.get(
                "target_level",
                "Not specified"
            )

            priority = item.get(
                "priority",
                "Medium"
            )

            why = item.get(
                "why",
                ""
            )

            if priority.lower() == "high":

                st.markdown(
                    f"""
                    <div class="priority-high">

                    <strong>🔴 {html.escape(skill)}</strong>

                    <br>

                    Current:
                    {html.escape(current)}

                    →

                    Target:
                    {html.escape(target)}

                    <br><br>

                    {html.escape(why)}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif priority.lower() == "low":

                st.markdown(
                    f"""
                    <div class="priority-low">

                    <strong>🟢 {html.escape(skill)}</strong>

                    <br>

                    Current:
                    {html.escape(current)}

                    →

                    Target:
                    {html.escape(target)}

                    <br><br>

                    {html.escape(why)}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="priority-medium">

                    <strong>🟡 {html.escape(skill)}</strong>

                    <br>

                    Current:
                    {html.escape(current)}

                    →

                    Target:
                    {html.escape(target)}

                    <br><br>

                    {html.escape(why)}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # ========================================================
    # TOP 3 PRIORITIES
    # ========================================================

    st.markdown("### 🚀 Start Here — Your Top 3 Priorities")

    priorities = data.get(
        "top_3_priorities",
        []
    )

    for index, item in enumerate(
        priorities,
        start=1
    ):

        st.markdown(
            f"#### {index}. {item.get('skill', '')}"
        )

        st.write(
            f"**Why:** {item.get('why', '')}"
        )

        st.write(
            f"**First step:** {item.get('first_step', '')}"
        )


    # ========================================================
    # TABBED RESULTS
    # ========================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📚 Learning Roadmap",
            "🗓 Weekly Plan",
            "💼 Portfolio",
            "📖 Resources",
            "🎯 Job Preparation"
        ]
    )


    # ========================================================
    # TAB 1 — ROADMAP
    # ========================================================

    with tab1:

        roadmap = data.get(
            "learning_roadmap",
            []
        )

        for phase in roadmap:

            with st.expander(
                f"📍 {phase.get('phase', '')} — "
                f"{phase.get('timeframe', '')}",
                expanded=True
            ):

                st.markdown("**Skills & Topics**")

                for skill in phase.get(
                    "skills",
                    []
                ):
                    st.write(f"✓ {skill}")

                st.markdown("**Practical Work**")

                st.write(
                    phase.get(
                        "practical_work",
                        ""
                    )
                )

                st.markdown("**Portfolio Project**")

                st.info(
                    phase.get(
                        "portfolio_project",
                        ""
                    )
                )

                st.markdown("**Suggested Time**")

                st.write(
                    phase.get(
                        "suggested_hours",
                        ""
                    )
                )


    # ========================================================
    # TAB 2 — WEEKLY PLAN
    # ========================================================

    with tab2:

        weekly_plan = data.get(
            "weekly_plan",
            []
        )

        st.caption(
            f"Designed around your available "
            f"{profile['study_time']} hours/week."
        )

        for day in weekly_plan:

            col1, col2, col3 = st.columns(
                [1, 3, 1]
            )

            with col1:
                st.markdown(
                    f"**{day.get('day', '')}**"
                )

            with col2:
                st.write(
                    day.get(
                        "activity",
                        ""
                    )
                )

            with col3:
                st.write(
                    day.get(
                        "hours",
                        ""
                    )
                )


    # ========================================================
    # TAB 3 — PORTFOLIO
    # ========================================================

    with tab3:

        projects = data.get(
            "portfolio_projects",
            []
        )

        for project in projects:

            st.markdown(
                f"### 💼 {project.get('project', '')}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Difficulty:** "
                    + project.get(
                        "difficulty",
                        ""
                    )
                )

                tools = project.get(
                    "tools",
                    []
                )

                st.write(
                    "**Tools:** "
                    + ", ".join(tools)
                )

            with col2:

                st.write(
                    "**Portfolio Output:** "
                    + project.get(
                        "portfolio_output",
                        ""
                    )
                )

            st.write(
                project.get(
                    "description",
                    ""
                )
            )

            st.divider()


    # ========================================================
    # TAB 4 — RESOURCES
    # ========================================================

    with tab4:

        resources = data.get(
            "learning_resources",
            []
        )

        st.info(
            "Resource names are recommendations. "
            "Always verify the current course/resource availability "
            "before starting."
        )

        for resource in resources:

            st.markdown(
                f"### 📖 {resource.get('skill', '')}"
            )

            resource_list = resource.get(
                "resources",
                []
            )

            for resource_name in resource_list:

                st.write(
                    f"• {resource_name}"
                )

            st.write(
                "**How to use:** "
                + resource.get(
                    "how_to_use",
                    ""
                )
            )

            st.divider()


    # ========================================================
    # TAB 5 — JOB PREPARATION
    # ========================================================

    with tab5:

        preparation = data.get(
            "internship_job_preparation",
            []
        )

        for item in preparation:

            st.write(
                f"✓ {item}"
            )


    # ========================================================
    # NEXT ACTIONS
    # ========================================================

    st.divider()

    st.markdown(
        "### 🚀 Your Next 3 Actions"
    )

    actions = data.get(
        "next_3_actions",
        []
    )

    for index, action in enumerate(
        actions,
        start=1
    ):

        st.success(
            f"**{index}.** {action}"
        )


    # ========================================================
    # DOWNLOAD SECTION
    # ========================================================

    st.divider()

    st.markdown(
        "### 📥 Download Your Personalized Roadmap"
    )

    markdown_report = create_markdown_report(
        data,
        profile,
        domain,
        level,
        learning_time
    )

    html_report = create_html_report(
        markdown_report
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="📄 Download Markdown Roadmap",
            data=markdown_report,
            file_name="personalized_career_roadmap.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col2:

        st.download_button(
            label="🌐 Download HTML Roadmap",
            data=html_report,
            file_name="personalized_career_roadmap.html",
            mime="text/html",
            use_container_width=True
        )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.divider()

    st.warning(
        data.get(
            "disclaimer",
            "This roadmap is AI-generated and should be used "
            "as a planning guide, not as a guarantee of career success."
        )
    )


# ============================================================
# RESET BUTTON
# ============================================================

if "roadmap_data" in st.session_state:

    st.divider()

    if st.button(
        "🔄 Start Over",
        use_container_width=True
    ):

        for key in [
            "roadmap_data",
            "roadmap_profile",
            "roadmap_domain",
            "roadmap_level",
            "roadmap_learning_time"
        ]:

            if key in st.session_state:
                del st.session_state[key]

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
    🎯 AI Career & Skill Roadmap |
    AI-generated guidance for educational and career-planning purposes.
    </div>
    """,
    unsafe_allow_html=True
)
