from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="Account Plan Generator API",
    description="Backend for Company Research Assistant",
    version="1.0"
)

# include routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}
