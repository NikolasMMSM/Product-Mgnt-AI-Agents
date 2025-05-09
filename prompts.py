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
