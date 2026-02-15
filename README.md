# KakaoTalk AI Agent (FastAPI + Cloudflare Tunnel)

카카오톡 채널에서 AI 응답을 구현하기 위한 최소 구성 가이드입니다.

## 구성 요소

-   FastAPI (로컬 서버)
-   Uvicorn (ASGI 서버 실행)
-   Cloudflare Tunnel (외부 HTTPS 노출)
-   Kakao i Open Builder (챗봇 + 스킬 연결)
-   카카오톡 채널

------------------------------------------------------------------------

# Architecture Flow

사용자 (카카오톡) → 카카오 서버 → Kakao i Open Builder (시나리오 / 블록)
→ 스킬(Webhook) 호출 → Cloudflare Tunnel (HTTPS → localhost 프록시) →
FastAPI 서버 (app.py) → 카카오 규격 JSON 응답 → 카카오톡 사용자에게 출력

------------------------------------------------------------------------

# Step-by-Step Setup

## 1. FastAPI 서버 작성

app.py

``` python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/kakao")
async def kakao_webhook(req: Request):
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "Hello World 👋"
                    }
                }
            ]
        }
    }
```

## 2. 서버 실행

    uvicorn app:app --host 0.0.0.0 --port 8000

## 3. Cloudflare Tunnel 실행

    cloudflared tunnel --url http://localhost:8000

생성된 주소 예시:

    https://xxxxx.trycloudflare.com/kakao

## 4. 카카오톡 채널 생성

https://business.kakao.com

-   채널 생성
-   공개 설정 ON
-   검색 허용 ON

## 5. Kakao i Open Builder 챗봇 생성

https://chatbot.kakao.com

-   챗봇 생성
-   채널 연결

## 6. 스킬(Webhook) 등록

-   스킬 생성
-   Endpoint URL 입력

```{=html}
<!-- -->
```
    https://xxxxx.trycloudflare.com/kakao

## 7. 시나리오에서 스킬 연결

-   기본 시나리오
-   폴백 블록 선택
-   파라미터 설정 → 스킬 선택
-   저장

## 8. 배포

-   상단 배포 버튼 클릭
-   카카오톡 채널에서 테스트

------------------------------------------------------------------------

# Troubleshooting

## 문제 1: curl -X POST 에러

원인: PowerShell에서 curl은 Invoke-WebRequest 별칭

해결:

    curl.exe -X POST http://localhost:8000/kakao

## 문제 2: cloudflared 인식 안됨

해결: - PowerShell 재시작 - 또는 PC 재부팅

## 문제 3: 카톡에서 처리중...만 표시됨

원인: 스킬 호출이 실제 응답으로 연결되지 않음

해결: - 폴백 블록에서 스킬이 응답으로 설정되었는지 확인 - 저장 후 재배포

## 문제 4: 채널 검색 안됨

해결: - 채널 공개 ON - 검색 허용 ON

## 문제 5: 터널 주소 변경됨

원인: Quick Tunnel은 실행 시마다 랜덤 주소 생성

해결: - 새 URL을 스킬에 다시 등록 - Named Tunnel 사용 고려

------------------------------------------------------------------------

# Summary

이 프로젝트는 Webhook 기반 통신, Reverse Proxy 터널링, Kakao Open
Builder 스킬 연결, ASGI 서버 구조를 이해하기 위한 최소 구성입니다.
