from fastapi import FastAPI, Body, status

app = FastAPI()

@app.post("/input", status_code=status.HTTP_204_NO_CONTENT)
def receive_text(text: str = Body(..., media_type="text/plain")):
    print(text)
    return
