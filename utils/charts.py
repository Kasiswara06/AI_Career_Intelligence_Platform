import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

COLOR_PRIMARY = "#6366F1"   # Indigo / Purple Accent
COLOR_SECONDARY = "#10B981" # Emerald Green
COLOR_WARNING = "#F59E0B"   # Amber / Orange
COLOR_DANGER = "#EF4444"    # Rose / Red
COLOR_BG = "rgba(0,0,0,0)"

# 1. Resume Score Gauge
def create_resume_score_gauge(score: int) -> go.Figure:
    """Creates gauge chart for Overall Resume Score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Resume Score", 'font': {'size': 18, 'color': '#F3F4F6'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#9CA3AF"},
            'bar': {'color': COLOR_PRIMARY},
            'bgcolor': "rgba(31, 41, 55, 0.5)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(99, 102, 241, 0.2)'}
            ]
        }
    ))
    fig.update_layout(
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6", 'family': "Inter, sans-serif"},
        height=240,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# 2. ATS Score Gauge
def create_ats_gauge(score: int) -> go.Figure:
    """Creates gauge chart for ATS Compatibility Score."""
    color = COLOR_SECONDARY if score >= 75 else (COLOR_WARNING if score >= 50 else COLOR_DANGER)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "ATS Score Gauge", 'font': {'size': 18, 'color': '#F3F4F6'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#9CA3AF"},
            'bar': {'color': color},
            'bgcolor': "rgba(31, 41, 55, 0.5)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
            ]
        }
    ))
    fig.update_layout(
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6", 'family': "Inter, sans-serif"},
        height=240,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# 3. Skill Match Pie Chart
def create_skill_match_pie(detected_count: int = 12, missing_count: int = 4) -> go.Figure:
    """Creates pie chart showing Detected vs Missing skills ratio."""
    fig = go.Figure(data=[go.Pie(
        labels=['Detected Skills', 'Missing Skills'],
        values=[detected_count, missing_count],
        hole=0.55,
        marker=dict(colors=[COLOR_SECONDARY, COLOR_DANGER]),
        textinfo='label+percent',
        hoverinfo='label+value'
    )])
    fig.update_layout(
        title={'text': "Skill Match Ratio", 'font': {'size': 16, 'color': '#F3F4F6'}},
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        showlegend=True,
        height=260,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

# 4. Missing Skills Bar Chart
def create_missing_skills_chart(missing_skills: list = None) -> go.Figure:
    """Creates horizontal bar chart for Missing Skills analysis."""
    missing_skills = list(missing_skills or ["Docker", "AWS", "Kubernetes", "CI/CD", "MLOps"])
    if not missing_skills:
        missing_skills = ["Docker", "AWS", "Kubernetes", "CI/CD", "MLOps"]

    skills_subset = missing_skills[:6]
    weights = [max(40, 95 - i * 8) for i in range(len(skills_subset))]

    df = pd.DataFrame({
        "Skill": skills_subset,
        "Demand Weight": weights
    })
    fig = px.bar(
        df,
        x="Demand Weight",
        y="Skill",
        orientation="h",
        color_discrete_sequence=[COLOR_DANGER]
    )
    fig.update_layout(
        title={'text': "Missing Skills & Market Demand", 'font': {'size': 16, 'color': '#F3F4F6'}},
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        xaxis=dict(title="Importance %", gridcolor="rgba(75,85,99,0.3)"),
        yaxis=dict(title="", gridcolor="rgba(75,85,99,0.3)"),
        height=260,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

# 5. Top Skills Bar Chart
def create_top_skills_chart(skills: list = None) -> go.Figure:
    """Creates bar chart showing top candidate technical skills."""
    skills = list(skills or ["Python", "SQL", "Machine Learning", "PyTorch", "Streamlit", "Git"])
    if not skills:
        skills = ["Python", "SQL", "Machine Learning", "PyTorch", "Streamlit", "Git"]

    skills_subset = skills[:6]
    proficiencies = [max(50, 95 - i * 4) for i in range(len(skills_subset))]

    df = pd.DataFrame({
        "Skill": skills_subset,
        "Proficiency": proficiencies
    })
    fig = px.bar(
        df,
        x="Skill",
        y="Proficiency",
        color_discrete_sequence=[COLOR_PRIMARY]
    )
    fig.update_layout(
        title={'text': "Top Extracted Technical Skills", 'font': {'size': 16, 'color': '#F3F4F6'}},
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        xaxis=dict(title="Skill Name", gridcolor="rgba(75,85,99,0.3)"),
        yaxis=dict(title="Proficiency Score", gridcolor="rgba(75,85,99,0.3)"),
        height=260,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig


# 6. Job Match Bar Chart
def create_job_match_chart(jobs_list: list = None) -> go.Figure:
    """Creates bar chart showing candidate job match percentages across roles."""
    if not jobs_list:
        jobs_list = [
            {"job_title": "AI Engineer", "match_pct": 92},
            {"job_title": "Data Scientist", "match_pct": 88},
            {"job_title": "Python Developer", "match_pct": 85},
            {"job_title": "MLOps Engineer", "match_pct": 78}
        ]
    df = pd.DataFrame(jobs_list)
    fig = px.bar(
        df,
        x="match_pct",
        y="job_title",
        orientation="h",
        color="match_pct",
        color_continuous_scale="Purples"
    )
    fig.update_layout(
        title={'text': "Job Match Percentage", 'font': {'size': 16, 'color': '#F3F4F6'}},
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        xaxis=dict(title="Match %", range=[0, 100], gridcolor="rgba(75,85,99,0.3)"),
        yaxis=dict(title="", gridcolor="rgba(75,85,99,0.3)"),
        height=260,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

# 7. Salary Prediction Trajectory Chart
def create_salary_prediction_chart(exp_years: float, predicted_lpa: float) -> go.Figure:
    """Generates 5-year salary progression comparison chart."""
    years = [max(0, exp_years + i) for i in range(5)]
    salaries = [round(predicted_lpa * (1 + 0.15 * i), 2) for i in range(5)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=salaries,
        mode='lines+markers',
        name='Projected Salary (LPA)',
        line=dict(color=COLOR_SECONDARY, width=3),
        marker=dict(size=8, color=COLOR_SECONDARY)
    ))
    fig.update_layout(
        title={'text': "5-Year Projected Salary Trajectory (₹ LPA)", 'font': {'size': 16, 'color': '#F3F4F6'}},
        xaxis=dict(title="Experience (Years)", gridcolor="rgba(75,85,99,0.3)"),
        yaxis=dict(title="Salary (LPA ₹)", gridcolor="rgba(75,85,99,0.3)"),
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        height=260,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# 8. Career Recommendation Matrix Chart (Radar)
def create_career_recommendation_chart(skill_count: int = 12, ats_score: int = 85) -> go.Figure:
    """Generates career readiness radar matrix graph."""
    categories = ['Technical Skills', 'ATS Optimization', 'Experience', 'Education', 'Projects']
    scores = [
        min(100, skill_count * 8),
        ats_score,
        75,
        88,
        85
    ]
    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        fillcolor='rgba(99, 102, 241, 0.35)',
        line=dict(color=COLOR_PRIMARY, width=2)
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(75,85,99,0.3)"),
            bgcolor="rgba(31, 41, 55, 0.3)"
        ),
        title={'text': "Career Readiness Matrix", 'font': {'size': 16, 'color': '#F3F4F6'}},
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        height=260,
        margin=dict(l=30, r=30, t=40, b=20)
    )
    return fig

# 9. Learning Progress Chart
def create_learning_progress_chart() -> go.Figure:
    """Generates course completion & skill acquisition progress chart."""
    df = pd.DataFrame({
        "Module": ["Python Basics", "SQL & Databases", "Machine Learning", "Deep Learning", "Docker & AWS"],
        "Progress %": [100, 90, 85, 60, 30]
    })
    fig = px.bar(
        df,
        x="Module",
        y="Progress %",
        color="Progress %",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(
        title={'text': "Learning & Skill Acquisition Progress", 'font': {'size': 16, 'color': '#F3F4F6'}},
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        xaxis=dict(title="", gridcolor="rgba(75,85,99,0.3)"),
        yaxis=dict(title="Completion %", range=[0, 100], gridcolor="rgba(75,85,99,0.3)"),
        height=260,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

# 10. Salary Gauge Chart
def create_salary_gauge(salary_lpa: float = 8.5, max_target_lpa: float = 25.0) -> go.Figure:
    """Creates Speedometer Gauge Chart for Predicted Salary."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=salary_lpa,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Predicted Salary Gauge (₹ LPA)", 'font': {'size': 18, 'color': '#F3F4F6'}},
        number={'suffix': " LPA", 'font': {'size': 26, 'color': '#10B981'}},
        gauge={
            'axis': {'range': [0, max_target_lpa], 'tickwidth': 1, 'tickcolor': "#9CA3AF"},
            'bar': {'color': COLOR_SECONDARY},
            'bgcolor': "rgba(31, 41, 55, 0.5)",
            'steps': [
                {'range': [0, max_target_lpa * 0.35], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [max_target_lpa * 0.35, max_target_lpa * 0.70], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [max_target_lpa * 0.70, max_target_lpa], 'color': 'rgba(16, 185, 129, 0.2)'}
            ]
        }
    ))
    fig.update_layout(
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6", 'family': "Inter, sans-serif"},
        height=240,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# 11. Resume Comparison Chart (Old vs New Resume)
def create_salary_comparison_chart(old_lpa: float = 6.5, new_lpa: float = 8.2) -> go.Figure:
    """Side-by-side comparison bar chart for Old Resume vs New Resume Salary."""
    df = pd.DataFrame({
        "Resume Version": ["Old Resume", "New Resume"],
        "Expected Salary (LPA)": [old_lpa, new_lpa]
    })
    fig = px.bar(
        df,
        x="Resume Version",
        y="Expected Salary (LPA)",
        color="Resume Version",
        color_discrete_map={"Old Resume": "#6B7280", "New Resume": "#10B981"},
        text="Expected Salary (LPA)"
    )
    fig.update_traces(texttemplate='₹ %{text} LPA', textposition='outside')
    fig.update_layout(
        title={'text': "Salary Comparison: Old vs New Resume", 'font': {'size': 16, 'color': '#F3F4F6'}},
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        yaxis=dict(title="Salary (LPA ₹)", range=[0, max(12.0, new_lpa * 1.3)], gridcolor="rgba(75,85,99,0.3)"),
        xaxis=dict(title=""),
        height=260,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

# 12. Skill Impact Chart
def create_skill_impact_chart(skill_impacts: list = None) -> go.Figure:
    """Creates horizontal bar chart showing top skills contributing to salary valuation."""
    if not skill_impacts:
        skill_impacts = [
            {"skill": "Python", "impact": 9.2},
            {"skill": "Machine Learning", "impact": 8.8},
            {"skill": "SQL", "impact": 8.5},
            {"skill": "PyTorch", "impact": 8.2},
            {"skill": "Docker", "impact": 7.9},
            {"skill": "AWS", "impact": 7.5}
        ]
    df = pd.DataFrame(skill_impacts)
    fig = px.bar(
        df,
        x="impact",
        y="skill",
        orientation="h",
        color="impact",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(
        title={'text': "Top Skills Valuation Impact Score", 'font': {'size': 16, 'color': '#F3F4F6'}},
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        xaxis=dict(title="Impact Weight", range=[0, 10], gridcolor="rgba(75,85,99,0.3)"),
        yaxis=dict(title=""),
        height=260,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

# 13. Experience vs Salary Curve Chart
def create_exp_vs_salary_chart(exp_years: float = 1.5, current_lpa: float = 8.5) -> go.Figure:
    """Experience vs Salary curve across industry experience milestones."""
    milestones = [0.5, 1.5, 3.0, 5.0, 7.5, 10.0]
    base_curve = [round(4.5 + m * 2.2 + (m ** 0.8), 1) for m in milestones]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=milestones,
        y=base_curve,
        mode='lines+markers',
        name='Industry Average Curve',
        line=dict(color=COLOR_PRIMARY, width=2, dash='dash'),
        marker=dict(size=6)
    ))
    fig.add_trace(go.Scatter(
        x=[exp_years],
        y=[current_lpa],
        mode='markers',
        name='Your Current Evaluation',
        marker=dict(size=14, color=COLOR_SECONDARY, symbol='star')
    ))
    fig.update_layout(
        title={'text': "Experience vs Salary Market Curve", 'font': {'size': 16, 'color': '#F3F4F6'}},
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        xaxis=dict(title="Experience (Years)", gridcolor="rgba(75,85,99,0.3)"),
        yaxis=dict(title="Salary (LPA ₹)", gridcolor="rgba(75,85,99,0.3)"),
        height=260,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# 14. Market Salary Comparison Chart
def create_market_salary_comparison_chart(candidate_lpa: float = 8.5, market_avg_lpa: float = 7.8) -> go.Figure:
    """Compares candidate salary against market percentiles (25th, 50th, Candidate, 90th)."""
    df = pd.DataFrame({
        "Percentile": ["25th Percentile", "50th (Market Avg)", "Your Prediction", "90th Percentile"],
        "Salary (LPA)": [round(market_avg_lpa * 0.75, 1), market_avg_lpa, candidate_lpa, round(market_avg_lpa * 1.45, 1)]
    })
    fig = px.bar(
        df,
        x="Percentile",
        y="Salary (LPA)",
        color="Percentile",
        color_discrete_sequence=["#9CA3AF", "#60A5FA", "#10B981", "#A855F7"]
    )
    fig.update_layout(
        title={'text': "Candidate vs Industry Market Benchmark", 'font': {'size': 16, 'color': '#F3F4F6'}},
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        font={'color': "#F3F4F6"},
        yaxis=dict(title="Salary (LPA ₹)", gridcolor="rgba(75,85,99,0.3)"),
        xaxis=dict(title=""),
        height=260,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig


