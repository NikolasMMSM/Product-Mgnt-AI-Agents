import streamlit as st
import pandas as pd
import openai
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(dotenv_path="envconfig.env")

# Configure your OpenAI API key in the envconfig.env file
openai.api_key = os.getenv("OPENAI_API_KEY") 

st.set_page_config(page_title="AI Agent - Project Retrospective Insights", layout="wide")
st.title("🤖 AI Agent that Analyses Concluded Projects")

uploaded_file = st.file_uploader("📁 Upload your project CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # date and time conversion
    df['Activated Date'] = pd.to_datetime(df['Activated Date'], errors='coerce')
    df['Closed Date'] = pd.to_datetime(df['Closed Date'], errors='coerce')
    df = df.dropna(subset=['Activated Date', 'Closed Date'])
    df['Execution Time (days)'] = (df['Closed Date'] - df['Activated Date']).dt.days

    # Key metrics
    total_items = len(df)
    total_story_points = df['Story Points'].sum()
    avg_story_points = round(df['Story Points'].mean(), 2)
    avg_exec_time = round(df['Execution Time (days)'].mean(), 2)
    max_exec_time = round(df['Execution Time (days)'].max(), 2)

    # Top contributors
    by_assignee = df.groupby('Assigned To').agg(
        Items_Completed=('Title', 'count'),
        Total_Story_Points=('Story Points', 'sum'),
        Avg_Execution_Time=('Execution Time (days)', 'mean')
    ).sort_values(by='Total_Story_Points', ascending=False).head(3).reset_index()

    top_contributors = []
    for _, row in by_assignee.iterrows():
        top_contributors.append(f"- {row['Assigned To']}: {int(row['Items_Completed'])} items, {int(row['Total_Story_Points'])} points, avg. {round(row['Avg_Execution_Time'], 1)} days")

    # Prompt construction
    prompt = f"""
You are a product analyst. Below are the execution data of a completed project. Your task is to generate an executive summary of the delivery, highlighting strengths, bottlenecks, and opportunities for improvement. Also take into account the Story Points scale used to estimate task effort.

Project Data:
- Total items delivered: {total_items}
- Total Story Points: {total_story_points}
- Average Story Points per item: {avg_story_points}
- Average execution time per item: {avg_exec_time} days
- Top contributors:\n  """ + "\n  ".join(top_contributors) + """

Story Points Guide (Fibonacci Scale):
- 1: Extra small – One-line change or similar work, can be done in 1 hour.
- 2: Small – Developer understands the task, requires small problem-solving.
- 3: Average – Developer knows what to do, no research required.
- 5: Large – Task is not very common, may require help or some research.
- 8: Extra Large – Time-consuming, needs research and possibly multiple developers.
- 13: Warning – Complex, many unknowns, likely won't fit in one sprint.
- 21: Hazard – Very complex, unclear how to start, many assumptions and unknowns.

Instructions:
- Interpret whether delivery time is compatible with the estimated complexity.
- Identify potential estimation mistakes.
- Suggest improvement points for future sprints.
- Highlight strong individual contributions and possible performance issues.
- Respond in a professional, executive tone.
"""

    if st.button("🔍 Generate AI Analysis"):
        with st.spinner("The Agent is thinking..."):
            try:
                client = openai.OpenAI()

                response = client.chat.completions.create(
                    model="4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4
                    )
                analysis = response.choices[0].message.content.strip()

                st.markdown("### 📊 Analysis Done!")
                st.write(analysis)
            except Exception as e:
                st.error(f"Error - Review the model: {e}")
