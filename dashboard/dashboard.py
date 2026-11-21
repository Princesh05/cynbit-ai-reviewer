
import streamlit as st
import requests
import pandas as pd

from app.database.db import get_dashboard_stats, get_pr_analyses


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Cynbit AI Reviewer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# 2. SESSION STATE
# --------------------------------------------------

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "latest_files_changed" not in st.session_state:
    st.session_state.latest_files_changed = 0


# --------------------------------------------------
# 3. SIDEBAR
# --------------------------------------------------

st.sidebar.title("🤖 Cynbit AI")
st.sidebar.caption("Pull Request Intelligence System")

st.sidebar.divider()

st.sidebar.subheader("System Status")

try:
    health_response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )

    if health_response.ok:
        st.sidebar.success("FastAPI Connected")
    else:
        st.sidebar.warning("API is responding with an error")

except requests.exceptions.RequestException:
    st.sidebar.error("FastAPI Disconnected")

st.sidebar.divider()

st.sidebar.info(
    "Analyze code, predict Pull Request risk, "
    "review code quality and mentor developers."
)

st.sidebar.caption("Cynbit AI Reviewer | MVP")


# --------------------------------------------------
# 4. MAIN HEADER
# --------------------------------------------------

st.title("🤖 Cynbit AI Pull Request Intelligence")

st.subheader(
    "AI-powered Code Review & Developer Mentorship System"
)

st.write(
    "An intelligent platform that analyzes Python code, "
    "identifies potential issues, predicts Pull Request risk "
    "and provides AI-powered developer guidance."
)

st.divider()


# --------------------------------------------------
# 5. DASHBOARD METRICS
# --------------------------------------------------

stats = get_dashboard_stats()

col1, col2, col3 = st.columns(3)

col1.metric(
    "PR Analyses",
    stats["total_analyses"]
)

col2.metric(
    "High Risk PRs",
    stats["high_risk_prs"]
)

col3.metric(
    "Detected Issues",
    stats["total_issues"]
)

st.caption(
    "Metrics are retrieved from persistent SQLite database storage."
)

st.divider()


# --------------------------------------------------
# 6. PR ANALYSIS FORM
# --------------------------------------------------

st.header("🔍 Analyze a Pull Request")

st.write(
    "Enter Python source code and Pull Request statistics "
    "to generate a complete AI-powered analysis."
)

with st.form("pr_analysis_form"):

    code = st.text_area(
        "Python Source Code",
        height=250,
        placeholder=(
            "def calculate_total(price, quantity):\n"
            "    discount = 10\n"
            "    return price * quantity\n\n"
            "print(calculate_total(100, 2))"
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        files_changed = st.number_input(
            "Files Changed",
            min_value=0,
            value=3,
            step=1
        )

    with col2:
        lines_added = st.number_input(
            "Lines Added",
            min_value=0,
            value=25,
            step=1
        )

    with col3:
        lines_deleted = st.number_input(
            "Lines Deleted",
            min_value=0,
            value=5,
            step=1
        )

    question = st.text_input(
        "Developer Question",
        value="Explain how I can improve this Python function."
    )

    submitted = st.form_submit_button(
        "🚀 Analyze Pull Request",
        type="primary",
        width="stretch"
    )


# --------------------------------------------------
# 7. SEND REQUEST TO FASTAPI
# --------------------------------------------------

if submitted:

    if not code.strip():
        st.warning("Please enter Python code before submitting.")

    else:

        payload = {
            "code": code,
            "files_changed": int(files_changed),
            "lines_added": int(lines_added),
            "lines_deleted": int(lines_deleted),
            "question": question
        }

        try:

            with st.spinner(
                "Analyzing code, predicting risk and generating AI feedback..."
            ):

                response = requests.post(
                    f"{API_URL}/ai/pr-workflow",
                    json=payload,
                    timeout=180
                )

                response.raise_for_status()

                result = response.json()

            st.session_state.latest_result = result
            st.session_state.latest_files_changed = int(files_changed)

            st.success(
                "Pull Request analysis completed successfully!"
            )

        except requests.exceptions.HTTPError as error:

            st.error(
                f"API returned an HTTP error: {error}"
            )

            try:
                st.json(response.json())
            except ValueError:
                st.write(response.text)

        except requests.exceptions.Timeout:

            st.error(
                "The analysis took too long. Please try again."
            )

        except requests.exceptions.RequestException as error:

            st.error(
                f"Unable to connect to FastAPI: {error}"
            )

        except (KeyError, ValueError) as error:

            st.error(
                f"Unexpected API response: {error}"
            )


# --------------------------------------------------
# 8. DISPLAY LATEST ANALYSIS
# --------------------------------------------------

result = st.session_state.latest_result

if result is not None:

    st.divider()

    st.header("📊 Pull Request Analysis Results")

    static_data = result.get("static_analysis", {})
    risk_data = result.get("risk_analysis", {})
    review_data = result.get("code_review", {})
    mentor_data = result.get("mentorship", {})

    # Risk and issue metrics

    col1, col2, col3 = st.columns(3)

    with col1:

        risk = risk_data.get(
            "predicted_risk",
            "Unavailable"
        )

        st.metric(
            "Predicted Risk",
            risk
        )

    with col2:

        st.metric(
            "Detected Issues",
            static_data.get("total_issues", 0)
        )

    with col3:

        st.metric(
            "Files Changed",
            st.session_state.get("latest_files_changed", 0)
        )

    # Risk status

    st.subheader("PR Risk Assessment")

    if not risk_data.get("success", False):

        st.warning(
            risk_data.get(
                "message",
                "Risk prediction is unavailable."
            )
        )

    elif risk == "High":

        st.error("High Risk Pull Request")

    elif risk == "Medium":

        st.warning("Medium Risk Pull Request")

    elif risk == "Low":

        st.success("Low Risk Pull Request")

    # Static analysis

    with st.expander(
        "🔎 Static Code Analysis",
        expanded=True
    ):

        if static_data.get("valid", False):

            st.success("Python syntax is valid.")

            issues = static_data.get("issues", [])

            if issues:

                st.write("Detected issues:")

                st.dataframe(
                    pd.DataFrame(issues),
                    width="stretch",
                    hide_index=True
                )

            else:

                st.success(
                    "No issues detected by the current analyzer."
                )

        else:

            st.error("Python syntax errors detected.")

            st.json(static_data)

    # Risk confidence

    with st.expander("📈 Risk Prediction Details"):

        if risk_data.get("success", False):

            st.write(
                "Predicted Risk:",
                risk_data.get("predicted_risk")
            )

            confidence = risk_data.get("confidence", {})

            if confidence:

                confidence_df = pd.DataFrame(
                    {
                        "Risk Level": list(confidence.keys()),
                        "Confidence": list(confidence.values())
                    }
                )

                st.bar_chart(
                    confidence_df.set_index("Risk Level")
                )

                st.caption(
                    "These confidence scores come from the current "
                    "experimental model trained on synthetic data. "
                    "They are not validated real-world probabilities."
                )

        else:

            st.warning(
                risk_data.get(
                    "message",
                    "Risk prediction unavailable."
                )
            )

    # AI code review

    with st.expander(
        "🤖 AI Code Review",
        expanded=True
    ):

        if review_data.get("success", False):

            st.markdown(
                review_data.get(
                    "ai_review",
                    "No AI review available."
                )
            )

            st.caption(
                f"AI Provider: {review_data.get('provider', 'Unknown')}"
            )

        else:

            st.warning(
                review_data.get(
                    "ai_review",
                    review_data.get(
                        "message",
                        "AI review unavailable."
                    )
                )
            )

    # Developer mentorship

    with st.expander(
        "👨‍🏫 Developer Mentorship",
        expanded=True
    ):

        if mentor_data.get("success", False):

            st.markdown(
                mentor_data.get(
                    "mentor_response",
                    "No mentorship response available."
                )
            )

            st.write("Retrieved Knowledge:")

            topics = mentor_data.get(
                "retrieved_knowledge",
                []
            )

            for topic in topics:
                st.write(f"- {topic}")

            st.caption(
                f"AI Provider: {mentor_data.get('provider', 'Unknown')}"
            )

        else:

            st.warning(
                mentor_data.get(
                    "message",
                    "Developer mentorship unavailable."
                )
            )


# --------------------------------------------------
# 9. ANALYTICS SECTION
# --------------------------------------------------

st.divider()

st.header("📈 PR Analytics")

history = get_pr_analyses(limit=100)

if history:

    history_df = pd.DataFrame([
        {
            "Analysis ID": item["id"],
            "Date": item["created_at"],
            "Risk": item["risk_level"],
            "Issues": item["issue_count"],
            "Files Changed": item["files_changed"],
            "Lines Added": item["lines_added"],
            "Lines Deleted": item["lines_deleted"]
        }
        for item in history
    ])

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Risk Distribution")

        risk_counts = (
            history_df["Risk"]
            .value_counts()
            .reindex(
                ["Low", "Medium", "High"],
                fill_value=0
            )
        )

        st.bar_chart(risk_counts)

    with col2:

        st.subheader("Issues per Analysis")

        st.bar_chart(
            history_df.set_index("Analysis ID")["Issues"]
        )

    st.subheader("Persistent Analysis History")

    st.dataframe(
        history_df,
        width="stretch",
        hide_index=True
    )

else:

    st.info("No saved PR analyses found in the database.")


# --------------------------------------------------
# 10. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Cynbit AI Pull Request Intelligence | "
    "AI Code Review • ML Risk Prediction • RAG Mentorship • LangGraph"
)
