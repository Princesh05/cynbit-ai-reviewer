
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

defaults = {
    "latest_result": None,
    "latest_files_changed": 0,
    "github_pull_requests": None,
    "github_repository": None,
    "latest_analysis_info": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


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
        st.sidebar.warning(
            f"API Error: {health_response.status_code}"
        )

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
# 6. GITHUB REPOSITORY INTEGRATION
# --------------------------------------------------

st.header("🐙 GitHub Repository Integration")

st.write(
    "Connect a public GitHub repository and fetch its "
    "Pull Requests for AI-powered analysis."
)

github_col1, github_col2 = st.columns(2)

with github_col1:
    github_owner = st.text_input(
        "GitHub Owner",
        value="Princesh05",
        key="github_owner"
    )

with github_col2:
    github_repo = st.text_input(
        "Repository Name",
        value="cynbit-ai-reviewer",
        key="github_repo"
    )


# --------------------------------------------------
# FETCH PULL REQUESTS
# --------------------------------------------------

if st.button(
    "🔍 Fetch Pull Requests",
    key="fetch_github_prs",
    type="primary"
):

    if not github_owner.strip() or not github_repo.strip():

        st.warning(
            "Please enter both GitHub owner and repository name."
        )

    else:

        try:

            with st.spinner(
                "Fetching Pull Requests from GitHub..."
            ):

                response = requests.get(
                    f"{API_URL}/github/"
                    f"{github_owner.strip()}/"
                    f"{github_repo.strip()}/pulls",
                    timeout=30
                )

                response.raise_for_status()

                github_data = response.json()

            st.session_state.github_pull_requests = (
                github_data.get("pull_requests", [])
            )

            st.session_state.github_repository = (
                f"{github_owner.strip()}/{github_repo.strip()}"
            )

            st.success(
                "GitHub repository connected successfully!"
            )

        except requests.exceptions.HTTPError:

            st.error(
                f"GitHub API request failed: {response.status_code}"
            )

            try:
                st.json(response.json())
            except ValueError:
                st.write(response.text)

        except requests.exceptions.Timeout:

            st.error(
                "GitHub request timed out. Please try again."
            )

        except requests.exceptions.RequestException as error:

            st.error(
                f"Unable to connect to FastAPI: {error}"
            )

        except ValueError:

            st.error(
                "The backend returned an invalid JSON response."
            )


# --------------------------------------------------
# DISPLAY PULL REQUESTS
# --------------------------------------------------

pull_requests = st.session_state.github_pull_requests

if pull_requests is not None:

    st.metric(
        "Total Pull Requests",
        len(pull_requests)
    )

    if pull_requests:

        st.subheader("Repository Pull Requests")

        for pr in pull_requests:

            pr_number = pr.get("number", "N/A")
            pr_title = pr.get("title", "Untitled")

            with st.expander(
                f"PR #{pr_number} - {pr_title}"
            ):

                author = pr.get("author", "Unknown")

                st.write("**Author:**", author)

                st.write(
                    "**State:**",
                    pr.get("state", "Unknown")
                )

                st.write(
                    "**PR Number:**",
                    pr_number
                )

                st.write(
                    "**Created At:**",
                    pr.get("created_at", "Unavailable")
                )

                st.write(
                    "**Last Updated:**",
                    pr.get("updated_at", "Unavailable")
                )

                pr_url = pr.get("url") or pr.get("html_url")

                if pr_url:

                    st.link_button(
                        "Open Pull Request on GitHub",
                        pr_url
                    )

                st.divider()

                # ----------------------------------
                # ANALYZE GITHUB PULL REQUEST
                # ----------------------------------

                if st.button(
                    "🚀 Analyze This Pull Request",
                    key=f"analyze_github_pr_{pr_number}",
                    type="primary"
                ):

                    try:

                        with st.spinner(
                            f"Analyzing GitHub PR #{pr_number}..."
                        ):

                            analyze_response = requests.post(
                                f"{API_URL}/github/"
                                f"{github_owner.strip()}/"
                                f"{github_repo.strip()}/"
                                f"pulls/{pr_number}/analyze",
                                timeout=300
                            )

                            analyze_response.raise_for_status()

                            github_result = analyze_response.json()

                        analysis = github_result.get("analysis")

                        if not isinstance(analysis, dict):
                            st.error(
                                "The backend returned an invalid analysis."
                            )

                        else:

                            st.session_state.latest_result = analysis

                            st.session_state.latest_files_changed = (
                                github_result.get(
                                    "total_changed_files", 0
                                )
                            )

                            st.session_state.latest_analysis_info = {
                                "source": "GitHub Pull Request",
                                "repository": github_result.get(
                                    "repository", "Unknown"
                                ),
                                "pr_number": github_result.get(
                                    "pull_request_number", pr_number
                                ),
                                "pr_title": github_result.get(
                                    "pull_request_title", pr_title
                                ),
                                "analysis_id": github_result.get(
                                    "analysis_id", "Unavailable"
                                ),
                                "python_files": github_result.get(
                                    "python_files_analyzed", []
                                )
                            }

                            st.success(
                                "GitHub Pull Request analyzed successfully!"
                            )

                            st.rerun()

                    except requests.exceptions.HTTPError:

                        st.error(
                            f"PR analysis failed: "
                            f"{analyze_response.status_code}"
                        )

                        try:
                            st.json(analyze_response.json())
                        except ValueError:
                            st.write(analyze_response.text)

                    except requests.exceptions.Timeout:

                        st.error(
                            "Analysis timed out. Please try again."
                        )

                    except requests.exceptions.RequestException as error:

                        st.error(
                            f"Unable to connect to backend: {error}"
                        )

                    except ValueError:

                        st.error(
                            "The backend returned an invalid JSON response."
                        )

    else:

        st.info(
            "No Pull Requests found in this repository."
        )


st.divider()


# --------------------------------------------------
# 7. MANUAL PR ANALYSIS FORM
# --------------------------------------------------

st.header("🔍 Manual Pull Request Analysis")

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
# 8. SEND MANUAL REQUEST TO FASTAPI
# --------------------------------------------------

if submitted:

    if not code.strip():

        st.warning(
            "Please enter Python code before submitting."
        )

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

            st.session_state.latest_files_changed = int(
                files_changed
            )

            st.session_state.latest_analysis_info = None

            st.success(
                "Pull Request analysis completed successfully!"
            )

        except requests.exceptions.HTTPError:

            st.error(
                f"API returned an HTTP error: {response.status_code}"
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

        except ValueError as error:

            st.error(
                f"Unexpected API response: {error}"
            )


# --------------------------------------------------
# 9. DISPLAY LATEST ANALYSIS
# --------------------------------------------------

result = st.session_state.latest_result

if result is not None:

    st.divider()

    st.header("📊 Pull Request Analysis Results")

    # GitHub analysis information

    analysis_info = st.session_state.latest_analysis_info

    if analysis_info:

        st.success(
            "Analysis Source: GitHub Pull Request"
        )

        st.write(
            "**Repository:**",
            analysis_info["repository"]
        )

        st.write(
            "**Pull Request:**",
            f"#{analysis_info['pr_number']} - "
            f"{analysis_info['pr_title']}"
        )

        st.write(
            "**Database Analysis ID:**",
            analysis_info["analysis_id"]
        )

        st.write("**Python Files Analyzed:**")

        for filename in analysis_info["python_files"]:
            st.write(f"- `{filename}`")

    else:

        st.info("Analysis Source: Manual Code Submission")

    static_data = result.get("static_analysis", {})
    risk_data = result.get("risk_analysis", {})
    review_data = result.get("code_review", {})
    mentor_data = result.get("mentorship", {})

    # ----------------------------------------------
    # ANALYSIS METRICS
    # ----------------------------------------------

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
            st.session_state.latest_files_changed
        )

    # ----------------------------------------------
    # RISK ASSESSMENT
    # ----------------------------------------------

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

    # ----------------------------------------------
    # STATIC ANALYSIS
    # ----------------------------------------------

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

    # ----------------------------------------------
    # RISK CONFIDENCE
    # ----------------------------------------------

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

    # ----------------------------------------------
    # AI CODE REVIEW
    # ----------------------------------------------

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
                f"AI Provider: "
                f"{review_data.get('provider', 'Unknown')}"
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

    # ----------------------------------------------
    # DEVELOPER MENTORSHIP
    # ----------------------------------------------

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
                f"AI Provider: "
                f"{mentor_data.get('provider', 'Unknown')}"
            )

        else:

            st.warning(
                mentor_data.get(
                    "message",
                    "Developer mentorship unavailable."
                )
            )


# --------------------------------------------------
# 10. ANALYTICS SECTION
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

    st.info(
        "No saved PR analyses found in the database."
    )


# --------------------------------------------------
# 11. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Cynbit AI Pull Request Intelligence | "
    "AI Code Review • ML Risk Prediction • "
    "RAG Mentorship • LangGraph"
)
