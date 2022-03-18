from fastapi import APIRouter, HTTPException
from server.services.conversation.conversation import Dialogue
router = APIRouter()


@router.post("/api/v1/dialog")
async def dialog(input_text: str = "hej"):
    try:
        response = Dialogue().get_dialog_response(input_text)
    except Exception as exception:
        raise HTTPException(status_code=404, detail=exception)
    else:
        return response
