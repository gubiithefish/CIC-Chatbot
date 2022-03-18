from server.api.routers import nearest_store, dialog, scraper
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Chatbot", version="1")
app.include_router(nearest_store.router)
app.include_router(dialog.router)
app.include_router(scraper.router)
app.mount("/public", StaticFiles(directory="public"), name="public")


if __name__ == "__main__":
    # noinspection PyTypeChecker
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=False)
