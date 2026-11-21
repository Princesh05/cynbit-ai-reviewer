
from fastapi import APIRouter
from app.agents.pr_workflow import run_pr_workflow
from pydantic import BaseModel, Field
from app.ai.developer_mentor import mentor_developer
from app.database.db import initialize_database, save_pr_analysis
from app.ai.code_reviewer import review_code
# Initialize the database when the API starts

initialize_database()

router = APIRouter(prefix="/ai", tags=["AI Code Reviewer"])


class CodeReviewRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        description="Python source code to review"
    )


@router.post("/review")
def ai_code_review(request: CodeReviewRequest):
    result = review_code(request.code)
    return result


class MentorRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Ask a Python programming question"
    )


@router.post("/mentor")
def developer_mentor_endpoint(request: MentorRequest):
    return mentor_developer(request.question)


class PRWorkflowRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        description="Python source code from the Pull Request"
    )

    files_changed: int = Field(..., ge=0)
    lines_added: int = Field(..., ge=0)
    lines_deleted: int = Field(..., ge=0)

    question: str = Field(
        default="",
        description="Optional developer mentorship question"
    )



@router.post("/pr-workflow")
def execute_pr_workflow(request: PRWorkflowRequest):

    # Run the complete PR analysis workflow
    result = run_pr_workflow(
        code=request.code,
        files_changed=request.files_changed,
        lines_added=request.lines_added,
        lines_deleted=request.lines_deleted,
        question=request.question
    )

    # Save the analysis result in SQLite
    analysis_id = save_pr_analysis(
        code=request.code,
        files_changed=request.files_changed,
        lines_added=request.lines_added,
        lines_deleted=request.lines_deleted,
        question=request.question,
        result=result
    )

    # Return the analysis result
    return result
