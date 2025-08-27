from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models.request import PDFInput
from app.models.response import PDFResponse
from app.models.state import PDFChatState
from app.services.workflow import run_blog_workflow
from app.services import workflow_store

router = APIRouter(prefix="/pdf", tags=["PDF"])


def _build_response(workflow_id: str, state: PDFChatState) -> dict:
    """
    Helper to standardize workflow responses.
    """
    return {
        "workflow_id":workflow_id,
        "data":state.get("answer")
    }


@router.post("/start")
async def start_workflow(req: PDFInput, db: Session = Depends(workflow_store.get_db)):
    """
    Start workflow, returns workflow_id and initial state.
    """
    initial_state: PDFChatState = {
        # "input": {"userQuery": req.userquery, "pdfpath": req.pdf_path or ""},
        "userQuery": req.userquery, "pdfpath": req.pdf_path or ""
    }  # type: ignore


    # Save workflow
    workflow_id = workflow_store.create_workflow(db, initial_state)

    # Run until first HITL pause
    state = run_blog_workflow(initial_state,workflow_id)
    workflow_store.update_workflow(db, workflow_id, state)
    return _build_response(workflow_id, state) # type: ignore