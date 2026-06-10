"""File Search 기반 RAG 챗봇 — 참고용 완성본.

Gemini File Search가 청킹·임베딩·인덱싱·검색을 모두 대신하므로,
이 서버가 하는 일은 사실상 두 가지뿐입니다.
  1) 문서를 File Search Store에 업로드 (인덱싱은 자동)
  2) 질문이 오면 FileSearch 도구를 붙여 generate_content 호출

실행 전에 GEMINI_API_KEY 환경 변수가 필요합니다.
  로컬:    GEMINI_API_KEY=... uvicorn main:app --reload
  Cloud Run: 배포 시 --set-env-vars GEMINI_API_KEY=... 로 전달
"""

import os
import tempfile
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
from pydantic import BaseModel

STORE_DISPLAY_NAME = os.environ.get("STORE_NAME", "rag-chatbot-store")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client()  # GEMINI_API_KEY 환경 변수를 자동으로 읽는다
app = FastAPI(title="File Search RAG Chatbot")

_store = None


def get_store():
    """display_name으로 스토어를 찾고 없으면 생성한다.

    스토어의 실제 이름(name)은 자동 생성 ID라서 재시작 후 재사용하려면
    display_name으로 검색하는 get-or-create 패턴이 필요하다.
    중복 생성을 API가 막아주지 않으므로 멱등성은 클라이언트 책임.
    """
    global _store
    if _store is None:
        for store in client.file_search_stores.list():
            if store.display_name == STORE_DISPLAY_NAME:
                _store = store
                break
        else:
            _store = client.file_search_stores.create(
                config={"display_name": STORE_DISPLAY_NAME}
            )
    return _store


class ChatTurn(BaseModel):
    role: str  # "user" 또는 "model"
    text: str


class ChatRequest(BaseModel):
    history: list[ChatTurn] = []
    question: str


@app.post("/api/upload")
async def upload(file: UploadFile):
    """문서를 스토어에 업로드한다. 청킹/임베딩/인덱싱은 전부 자동."""
    suffix = Path(file.filename or "document").suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        op = client.file_search_stores.upload_to_file_search_store(
            file=tmp_path,
            file_search_store_name=get_store().name,
            config={"display_name": file.filename},
        )
        # 업로드는 long-running operation — 인덱싱이 끝날 때까지 폴링한다.
        # 문서 하나에 수십 초가 걸릴 수 있다.
        while not op.done:
            time.sleep(3)
            op = client.operations.get(op)
    finally:
        os.unlink(tmp_path)

    return {"status": "indexed", "file": file.filename}


@app.get("/api/store")
def store_info():
    """인덱싱 현황 — 스토어 객체만으로 모니터링 UI를 만들 수 있다."""
    s = client.file_search_stores.get(name=get_store().name)
    return {
        "display_name": s.display_name,
        "active_documents": s.active_documents_count,
        "pending_documents": s.pending_documents_count,
        "failed_documents": s.failed_documents_count,
        "size_bytes": s.size_bytes,
    }


@app.post("/api/chat")
def chat(req: ChatRequest):
    """검색 + 생성이 한 번의 generate_content 호출로 끝난다.

    대화 히스토리를 contents에 쌓아 보내면 "그럼 그건 왜 그래?" 같은
    후속 질문에서도 모델이 알아서 검색 질의를 다시 만든다.
    """
    contents = [
        types.Content(role=t.role, parts=[types.Part(text=t.text)])
        for t in req.history
    ]
    contents.append(
        types.Content(role="user", parts=[types.Part(text=req.question)])
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    file_search=types.FileSearch(
                        file_search_store_names=[get_store().name]
                    )
                )
            ]
        ),
    )

    answer = response.text or ""
    sources = []

    # grounding_metadata: 답변의 어느 구간이 어느 문서 청크에서 왔는지
    meta = response.candidates[0].grounding_metadata if response.candidates else None
    if meta and meta.grounding_chunks:
        for chunk in meta.grounding_chunks:
            ctx = chunk.retrieved_context
            if ctx:
                sources.append({
                    "title": ctx.title,        # 업로드 시 display_name이 그대로 출처 제목이 된다
                    "text": (ctx.text or "")[:500],
                })

    if meta and meta.grounding_supports:
        # 주의: segment의 start/end_index는 문자 위치가 아니라 UTF-8 "바이트" 위치다.
        # 한글(글자당 3바이트)에 문자 인덱스로 [n] 마커를 꽂으면 전부 어긋난다.
        raw = answer.encode("utf-8")
        supports = sorted(
            meta.grounding_supports,
            key=lambda s: s.segment.end_index or 0,
            reverse=True,  # 뒤에서부터 삽입해야 앞쪽 위치가 밀리지 않는다
        )
        for support in supports:
            end = support.segment.end_index or 0
            ids = support.grounding_chunk_indices or []
            marker = "".join(f"[{i + 1}]" for i in ids).encode("utf-8")
            raw = raw[:end] + marker + raw[end:]
        answer = raw.decode("utf-8")

    return {"answer": answer, "sources": sources}


# 같은 폴더의 static/index.html을 화면으로 제공
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")
