import streamlit as st
import pandas as pd
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Agent - Project Consultant", layout="wide")
st.markdown("""
    <style>
        .block-container {
            max-width: 900px;
            margin: auto;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI Agent for Digital Project Analysis")

# Scope selector
scope_options = {
    "Initial Planning Quality": "planning",
    "Execution Monitoring": "execution",
    "Sprint Review": "sprint_review",
    "Delivery Summary": "delivery",
    "Risk Analysis": "risk",
    "Team Performance": "team"
}
selected_scope = st.selectbox("📌 What aspect of the project do you want to analyze?", list(scope_options.keys()))
scope_key = scope_options[selected_scope]

# Sprint number input (only for Sprint Review scope)
sprint_number = None
if scope_key == "sprint_review":
    sprint_number = st.text_input("📅 Enter the Sprint Number you are reviewing:")

# File upload
uploaded_file = st.file_uploader("📁 Upload your project CSV file", type="csv")

if uploaded_file:
    raw_df = pd.read_csv(uploaded_file)
    df = raw_df.copy()

    # Filer per sprint if applicable
    if scope_key == "sprint_review" and sprint_number:
        sprint_col = [col for col in df.columns if 'sprint' in col.lower()]
        if sprint_col:
            df = df[df[sprint_col[0]].astype(str).str.strip() == sprint_number.strip()]

    df['Activated Date'] = pd.to_datetime(df['Activated Date'], errors='coerce')
    df['Closed Date'] = pd.to_datetime(df['Closed Date'], errors='coerce')
    df = df.dropna(subset=['Activated Date'])
    df['Execution Time (days)'] = (df['Closed Date'] - df['Activated Date']).dt.days

    total_items = len(df)
    total_story_points = df['Story Points'].sum()
    avg_story_points = round(df['Story Points'].mean(), 2)
    avg_exec_time = round(df['Execution Time (days)'].mean(), 2) if 'Execution Time (days)' in df else 0
    max_exec_time = round(df['Execution Time (days)'].max(), 2) if 'Execution Time (days)' in df else 0
    min_exec_time = round(df['Execution Time (days)'].min(), 2) if 'Execution Time (days)' in df else 0
    exec_time_std = round(df['Execution Time (days)'].std(), 2) if 'Execution Time (days)' in df else 0

    tasks_without_estimate = df['Story Points'].isna().sum()
    contributor_variability = df.groupby('Assigned To')['Execution Time (days)'].std().sort_values(ascending=False)
    top_variability_contributor = contributor_variability.idxmax() if not contributor_variability.empty else "N/A"
    top_variability_value = round(contributor_variability.max(), 2) if not contributor_variability.empty else 0

    by_assignee = df.groupby('Assigned To').agg(
        Items_Completed=('Title', 'count'),
        Total_Story_Points=('Story Points', 'sum'),
        Avg_Execution_Time=('Execution Time (days)', 'mean')
    ).sort_values(by='Total_Story_Points', ascending=False).head(3).reset_index()

    top_contributors = []
    for _, row in by_assignee.iterrows():
        top_contributors.append(f"- {row['Assigned To']}: {int(row['Items_Completed'])} items, {int(row['Total_Story_Points'])} points, avg. {round(row['Avg_Execution_Time'], 1)} days")

    sprint_info_line = f"- Sprint Number: {sprint_number}" if scope_key == "sprint_review" and sprint_number else ""

    key_metrics_text = f"""
Key Metrics:
{sprint_info_line}
- Total items (raw): {len(raw_df)}
- Items considered after filtering: {total_items}
- Tasks without Story Point estimate: {tasks_without_estimate}
- Average execution time: {avg_exec_time} days
- Max execution time: {max_exec_time} days
- Min execution time: {min_exec_time} days
- Std deviation: {exec_time_std} days
- Contributor with highest variability: {top_variability_contributor} ({top_variability_value} days)
"""

    scope_config = {
        "planning": {
            "prompt": (
                "persona: You are an experienced product analyst specialized in agile delivery who wants to build a report to your stakeholders.\n",
                "Analyze data to extract insights and deliver strategic recommendations.\n",
                "Analyze the initial planning quality.\n",
                "Focus on unrealistic deadlines, missing estimates, or high-complexity tasks."
            ),
        "instructions": (
            "- Identify unrealistic target dates and complexity mismatches."
            "- Assess missing estimates and story point distribution."
            "- Highlight potential planning risks and scope issues."
            "- Create a report separated by topics and bullet points"
            )
        },
        "execution": {
            "prompt": (
                "Evaluate current execution progress, effort distribution, and flag possible risks or bottlenecks."
            ),
            "instructions": (
                "- Assess if the project is on time and on track."
                "- Interpret whether delivery time is compatible with the estimated complexity."
                "- Identify estimation mistakes and execution risks."
                "- Highlight contributors with inconsistent performance."
            )
        },
        "sprint_review": {
            "prompt": (
                "You are a Scrum Analyst reviewing Sprint {sprint_number} for a software development team."
                "Please analyze the provided data and respond to the following:"
                "- Delivery performance: Did the team deliver everything that was planned for Sprint {sprint_number}?"
                "- Problems encountered: Did the team experience any blockers or inconsistencies that impacted delivery?"
                "- Scope changes: Were there signs of scope increase during the sprint (e.g. new work items added after sprint start)?"
                "- Top performer: Who was the most impactful contributor in this sprint and why?"
                "- Needs attention: Is there any contributor who needs support, mentoring, or reallocation?"
                "- Recommendations: Suggest specific improvements for the next sprint."
                "- Use the following data as input:"
                "- Work item status (done/in progress/etc.)"
                "- Story Points (effort vs. completion)"
                "- Assigned contributors and their task count"
                "- Variability in delivery time"
                "- Missing estimates"
                "- Historical effort consistency"
                "Return your answer in an executive report format, structured by topic with objective insights and actionable suggestions."
            ),
            "instructions": (
                "- Compare what was planned vs. completed in the sprint."
                "- Highlight demo-ready items and partial/incomplete tasks."
                "- Mention stakeholder feedback and sprint goal alignment."
                "- Emphasize positive highlights and team engagement."
            )
        },
        "delivery": {
            "prompt": (
                "Generate a retrospective summary with highlights, bottlenecks, and improvement suggestions."
            ),
            "instructions": (
                "- Generate an executive summary."
                "- Highlight strengths, bottlenecks, and performance patterns."
                "- Suggest areas for improvement in future deliveries."
            )
        },
        "risk": {
            "prompt": (
                "Identify potential risks based on historical execution patterns, outliers, or estimation gaps."
            ),
            "instructions": (
                "- Detect outliers and execution anomalies."
                "- Highlight areas where estimates and real effort diverged."
                "- Suggest early mitigation strategies."
            )
        },
        "team": {
            "prompt": (
                "Assess individual contributor performance, consistency, and suggest improvements or mentoring."
            ),
            "instructions": (
                "- Identify contributors with inconsistent delivery speed."
                "- Suggest mentoring or workload balance actions."
                "- Highlight strong contributions."
            )
        }
}

    focus = scope_config[scope_key]["prompt"]

if scope_key == "sprint_review" and sprint_number:
    focus += f"\nThis is Sprint {sprint_number}. Focus your analysis specifically on tasks completed during this sprint."

instructions = scope_config[scope_key]["instructions"]

if st.button("🔍 Generate AI Analysis"):
    if scope_key == "sprint_review" and not sprint_number:
        st.warning(
            "Please enter a Sprint Number before generating the Sprint Review analysis."
            )
        st.stop()
        prompt = f"""
              ## {key_metrics_text.strip()}

              {focus}
              Also, take into account the Story Points scale used to estimate task effort.

              Project Data:
              - Total items: {total_items}
              - Total Story Points: {total_story_points}
              - Average Story Points per item: {avg_story_points}
              - Average execution time per item: {avg_exec_time} days
              - Maximum execution time for a single item: {max_exec_time} days
              - Minimum execution time for a single item: {min_exec_time} days
              - Standard deviation of execution time: {exec_time_std} days
              - Tasks without Story Point estimate: {tasks_without_estimate}
              - Contributor with highest time variability: {top_variability_contributor} ({top_variability_value} days)
              - Top contributors:\n  """ + "\n  ".join(top_contributors) + (f"""
              - Work items in Sprint {sprint_number}:\n
                """ + "\n  ".join([f"  - {row['Title']} (ID: {row['ID']})" for _, row in df.iterrows()]) if scope_key == "sprint_review" and sprint_number and 'Title' in df.columns and 'ID' in df.columns else "") + f"""

              Story Points Guide (Fibonacci Scale):
              - 1: Extra small – One-line change or similar work, can be done in 1 hour.
              - 2: Small – Developer understands the task, requires small problem-solving.
              - 3: Average – Developer knows what to do, no research required.
              - 5: Large – Task is not very common, may require help or some research.
              - 8: Extra Large – Time-consuming, needs research and possibly multiple developers.
              - 13: Warning – Complex, many unknowns, likely won't fit in one sprint.
              - 21: Hazard – Very complex, unclear how to start, many assumptions and unknowns.
              (Note: 21 is the upper limit of the story point scale used in this analysis.)

              Instructions:
              {instructions}
              """

        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            analysis = response.choices[0].message.content.strip()
                
            st.markdown("### 📌 Key Metrics")
            st.code(key_metrics_text.strip(), language='markdown')
            st.markdown("### 📊 Analysis Result")
            st.text_area("",value=analysis, height=400, key="ai_report")
                
            st.markdown("""
                <script>
                    function copyReport() {
                    const text = document.getElementById('ai_report').value;
                    navigator.clipboard.writeText(text).then(function() {
                        alert('Report copied to clipboard!');}, 
                    function(err) {
                        alert('Failed to copy text: ', err);
                        });
                    }
                    </script>
                    <button onclick="copyReport()">📋 Copy Report to Clipboard</button>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Model consultation error: {e}")
