import streamlit as st
import pandas as pd
import openai
import os
from datetime import datetime
from dotenv import load_dotenv
from prompts import scope_config

# Load environment variables
# If you're deploying this code to Streamlit Cloud, you may will need to comment line 12
# and define OPENAI_API_KEY directly in the app's Secrets Manager instead.
# load_dotenv(dotenv_path="envconfig.env")
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

# File upload
uploaded_file = st.file_uploader("📁1st - Upload your project CSV file", type="csv")

if uploaded_file:
    # Defining Variables
    sprint_col = None
    sprint_number = None

    # Reading CSV File
    raw_df = pd.read_csv(uploaded_file)
    
     # Scope selector
    scope_options = {
        "Initial Planning Quality": "planning",
        "Execution Monitoring Report": "execution",
        "Stakeholder Sprint Review Report": "sprint_review",
        "Close-out Summary": "delivery",
    }
    selected_scope = st.selectbox("📌 2nd - What aspect of the project do you want to analyze?", list(scope_options.keys()))
    scope_key = scope_options[selected_scope]

    # Sprint number input (only for Sprint Review scope)
    focus = scope_config[scope_key]["prompt"]
    instructions = scope_config[scope_key]["instructions"]   
    
    #Importing processing functions
    from keymetrics import process_key_metrics 
    from keymetrics import generate_key_metrics
   
    df, total_items, total_story_points, total_closed_items, avg_story_points, avg_exec_time, max_exec_time, min_exec_time, exec_time_std, tasks_without_estimate, top_variability_contributor, top_variability_value, top_contributors, sprint_info_line = process_key_metrics(raw_df, scope_key, sprint_number)

    key_metrics_text = generate_key_metrics(
        raw_df=raw_df,
        df=df,
        sprint_number=sprint_number,
        total_items=total_items,
        tasks_without_estimate=tasks_without_estimate,
        avg_exec_time=avg_exec_time,
        max_exec_time=max_exec_time,
        min_exec_time=min_exec_time,
        exec_time_std=exec_time_std,
        total_closed_items=total_closed_items,
        top_variability_contributor=top_variability_contributor,
        top_variability_value=top_variability_value,
        scope_key=scope_key
    )

    # Filter per sprint if applicable
    if scope_key == "sprint_review":
        sprint_col = next(
                (col for col in df.columns if "iteration path" in col.lower()), None
            )
        sprint_options = sorted(
                df[sprint_col].dropna().unique()
                ) if sprint_col else []
        if sprint_options:
            sprint_number = st.selectbox("📅 Select the Sprint you are reviewing (*required)", sprint_options)
        else:
            sprint_number = st.text_input("📅 Enter the Sprint Number you are reviewing (*required)")
        if sprint_col and sprint_number:
                df = df[df[sprint_col].astype(str).str.contains(sprint_number.strip(), case=False)]
    


    # CTA Button
    if st.button("🔍 Generate AI Analysis"):
        
        if scope_key == "sprint_review" and not sprint_number:
                st.warning("Please enter a Sprint Number before generating the Sprint Review analysis.")
                st.stop()
        
        if scope_key == "sprint_review" and sprint_number:
            focus += f"\nThis is Sprint {sprint_number}. Focus your analysis specifically on tasks completed during this sprint."
        
        with st.spinner("AI is thinking..."):        
            prompt = f"""
                    ## {key_metrics_text.strip()}

                    {focus}
                    Also, take into account the Story Points scale used to estimate task effort.

                    Project Data:
                    - Total items: {total_items}
                    - Total Story Points: {total_story_points}
                    - Total Closed Items: {total_closed_items}
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
                st.code(analysis, height=400, language='markdown')

            except Exception as e:
                st.error(f"Model consultation error: {e}")
