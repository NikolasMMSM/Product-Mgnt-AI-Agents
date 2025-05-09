# 🤖 AI Agent – Agile Project Analysis

This project is a Streamlit-based AI assistant that analyzes agile project data exported from Azure DevOps. The agent acts as a **digital consultant**, capable of evaluating project planning, in-progress performance, or retrospective insights — depending on the current status of the project.

## 🔍 What it does

Given a `.csv` file exported from Azure DevOps, the agent will:

- 📅 Evaluate **initial planning** based on effort vs. deadlines
- 📈 Monitor **in-progress performance**, risk and workload distribution
- ✅ Provide **retrospective insights** when the project is completed:
  - Execution summary
  - Contributor performance
  - Estimation consistency
  - Strategic improvement suggestions

## 📂 CSV Requirements

The file should contain at least the following columns:

- `ID`
- `Work Item Type`
- `Title`
- `State`
- `Assigned To`
- `Story Points`
- `Activated Date`
- `Target Date`
- `Closed Date` *(optional but recommended)*
- `Iteration Path`
- `Priority`
- `Tags`
- `Reason`
- `Parent`
- `Created Date`

## 🚀 How to Run Locally

1. Install dependencies:
   ```bash
   pip install streamlit openai pandas python-dotenv
   ```

2. Create a file named `envconfig.env` with your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. Launch the app:
   ```bash
   streamlit run Project-Retro-AI-Agent.py
   ```

## 📌 Status Options

You will be prompted to select one of the following project statuses:
- **Initial** – for planning evaluation
- **In Progress** – for monitoring current performance
- **Completed** – for retrospective analysis

## ⚠️ Disclaimer

This app uses the GPT-4 API from OpenAI. Please keep your API key secure and monitor your usage according to your OpenAI plan.

---

Agent by Nikolas Moreira
"Alone, we go fast. Together, we go further"
