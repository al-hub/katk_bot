from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/kakao")
async def kakao_webhook(req: Request):
    # 지금은 payload(req.json())를 안 써도 됨. 그냥 고정 응답만.
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": "Hello World 👋"}}
            ]
        }
    }

