import pandas as pd

def process_key_metrics(raw_df, scope_key, sprint_number):

    df = raw_df.copy()
    df['Activated Date'] = pd.to_datetime(df.get('Activated Date'), errors='coerce')
    df['Created Date'] = pd.to_datetime(df.get('Created Date'), errors='coerce')
    df['Closed Date'] = pd.to_datetime(df.get('Closed Date'), errors='coerce')

    if scope_key == "planning":
        df = df.dropna(subset=["Created Date"])
        df['Execution Time (days)'] = pd.NA  # não calcula tempo
    elif scope_key == "sprint_review" and sprint_number:
        sprint_col = next((col for col in df.columns if "iteration path" in col.lower()), None)
        if sprint_col:
            df = df[df[sprint_col] == sprint_number]
        df['Execution Time (days)'] = (df['Closed Date'] - df['Activated Date']).dt.days
    else:
        df['Execution Time (days)'] = (df['Closed Date'] - df['Activated Date']).dt.days

 
    total_items = len(df)
    total_story_points = df['Story Points'].sum()
    total_closed_items = df['Closed Date'].notna().sum()
    avg_story_points = round(df['Story Points'].mean(), 2)
    avg_exec_time = (round(df['Execution Time (days)'].mean(), 2) if df['Execution Time (days)'].notna().any() else "N/A")
    max_exec_time = (round(df['Execution Time (days)'].max(), 2) if df['Execution Time (days)'].notna().any() else "N/A")
    min_exec_time = (round(df['Execution Time (days)'].min(), 2) if df['Execution Time (days)'].notna().any() else "N/A")
    exec_time_std = (round(df['Execution Time (days)'].std(), 2) if df['Execution Time (days)'].notna().any() else "N/A")

    tasks_without_estimate = df['Story Points'].isna().sum()
    if df['Execution Time (days)'].dropna().empty:
        contributor_variability = pd.Series(dtype='float64')
    else:
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

    return df, total_items, total_story_points, total_closed_items, avg_story_points, avg_exec_time, max_exec_time, min_exec_time, exec_time_std, tasks_without_estimate, top_variability_contributor, top_variability_value, top_contributors, sprint_info_line

def generate_key_metrics(raw_df, df, sprint_number, total_items, total_closed_items, tasks_without_estimate, avg_exec_time, max_exec_time, min_exec_time, exec_time_std, top_variability_contributor, top_variability_value, scope_key):

    sprint_info_line = f"- Sprint Number: {sprint_number}" if scope_key == "sprint_review" and sprint_number else ""
    return f"""
        Key Metrics:
        {sprint_info_line}
        - Total items (raw): {len(raw_df)}
        - Items considered after filtering: {total_items}
        - Items closed: {total_closed_items}
        - Tasks without Story Point estimate: {tasks_without_estimate}
        - Average execution time: {avg_exec_time} days
        - Max execution time: {max_exec_time} days
        - Min execution time: {min_exec_time} days
        - Std deviation: {exec_time_std} days
        - Contributor with highest variability: {top_variability_contributor} ({top_variability_value} days)
        """
