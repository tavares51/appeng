from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models import ChatRequest
from bot import process_message
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.post(
    "/chat/",
    responses={
        200: {"description": "Mensagem processada com sucesso"},
        400: {"description": "Requisição malformada"},
        500: {"description": "Erro interno do servidor"},
    }
)
async def send_message(chat: ChatRequest):
    try:
        if not chat.message:
            raise HTTPException(status_code=400, detail="Mensagem não pode estar vazia.")
        response = process_message(chat.message)
        return {"response": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

app.include_router(router)