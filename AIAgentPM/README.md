# 🤖 AI Agent – Agile Project Intelligence for Product & Project Managers

This Streamlit-based AI Agent acts as a **digital consultant** to help Product Managers, Scrum Masters, and Agile Leads extract insights from project data exported from Azure DevOps. It offers dynamic analyses tailored to different project stages: planning, execution monitoring, sprint review, and delivery retrospectives.

---

## 🔍 What It Does

Given a `.csv` file exported from Azure DevOps, the agent will:

- 📌 Analyze **initial planning** for:
  - Unrealistic deadlines
  - Missing story point estimates
  - Overcommitment or complexity mismatches

- 🚦 Monitor **in-progress execution**:
  - Risk exposure
  - Task effort vs. velocity
  - Contributor variability

- 🧾 Produce **sprint review reports**:
  - What was accomplished vs. planned
  - Who contributed the most
  - Cycle time inconsistencies

- ✅ Generate **retrospective delivery insights**:
  - Summary of execution
  - Estimation hygiene
  - Strategic recommendations for future planning

- 📊 Optionally, generate **Python code with pandas + matplotlib** to visualize the user story distribution in the project.

---

## 📂 CSV Requirements

Your file must contain at least the following columns:

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
   OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
   OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
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

This app uses the GPT-3.5-turbo API from OpenAI or NVIDIA's Llama-3.1-Nemotron-Ultra-253B-v1. \n 
Please keep your API key secure and monitor your usage according to your OpenAI.\n
For set up the NVIDA's Llama-3.1-Nemotron-Ultra-253B-v1 API key:
- Sign up or log in at [NVIDIA Build](https://build.nvidia.com/nvidia/llama-3_1-nemotron-ultra-253b-v1?integrate_nim=true&hosted_api=true&modal=integrate-nim)
- Generate an API key

---

Made by Nikolas Moreira
