
from typing import TypedDict, Any
import time

from langgraph.graph import StateGraph, START, END

from app.analyzer.code_analyzer import analyze_code
from app.ml.risk_predictor import predict_pr_risk
from app.ai.code_reviewer import review_code
from app.ai.developer_mentor import mentor_developer


class PRState(TypedDict):
    code: str
    files_changed: int
    lines_added: int
    lines_deleted: int
    question: str

    static_analysis: dict[str, Any]
    risk_analysis: dict[str, Any]
    code_review: dict[str, Any]
    mentorship: dict[str, Any]
    final_report: dict[str, Any]


def static_analysis_node(state: PRState):
    """Analyze Python code for static issues."""

    result = analyze_code(state["code"])

    return {
        "static_analysis": result
    }


def risk_prediction_node(state: PRState):
    """Predict the PR risk using the existing ML model."""

    analysis = state["static_analysis"]

    if not analysis["valid"]:
        return {
            "risk_analysis": {
                "success": False,
                "message": "Risk prediction skipped because of syntax errors."
            }
        }

    result = predict_pr_risk(
        files_changed=state["files_changed"],
        lines_added=state["lines_added"],
        lines_deleted=state["lines_deleted"],
        detected_issues=analysis["total_issues"]
    )

    return {
        "risk_analysis": {
            "success": True,
            **result
        }
    }


def code_review_node(state: PRState):
    """Generate an AI-powered code review."""

    result = review_code(state["code"])

    return {
        "code_review": result
    }


def mentorship_node(state: PRState):
    """Retrieve relevant knowledge and generate developer guidance."""

    question = state.get("question", "").strip()

    if not question:
        question = (
            "Explain the important issues in this Python code "
            "and how a junior developer can improve it."
        )

    result = mentor_developer(
    question=question,
    code=state["code"]
    )
    return {
        "mentorship": result
    }


def final_report_node(state: PRState):
    """Combine all workflow results into one report."""

    return {
        "final_report": {
            "static_analysis": state["static_analysis"],
            "risk_analysis": state["risk_analysis"],
            "code_review": state["code_review"],
            "mentorship": state["mentorship"]
        }
    }


def build_pr_workflow():
    """Build and compile the LangGraph workflow."""

    workflow = StateGraph(PRState)

    workflow.add_node("static_analysis", static_analysis_node)
    workflow.add_node("risk_prediction", risk_prediction_node)
    workflow.add_node("code_review", code_review_node)
    workflow.add_node("mentorship", mentorship_node)
    workflow.add_node("final_report", final_report_node)

    workflow.add_edge(START, "static_analysis")
    workflow.add_edge("static_analysis", "risk_prediction")
    workflow.add_edge("risk_prediction", "code_review")
    workflow.add_edge("code_review", "mentorship")
    workflow.add_edge("mentorship", "final_report")
    workflow.add_edge("final_report", END)

    return workflow.compile()


pr_workflow = build_pr_workflow()


def run_pr_workflow(
    code: str,
    files_changed: int,
    lines_added: int,
    lines_deleted: int,
    question: str = ""
):
    """Run the complete PR intelligence workflow."""

    initial_state = {
        "code": code,
        "files_changed": files_changed,
        "lines_added": lines_added,
        "lines_deleted": lines_deleted,
        "question": question
    }

    result = pr_workflow.invoke(initial_state)

    return result["final_report"]