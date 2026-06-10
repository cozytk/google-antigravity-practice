# Cloud Run이 실행할 컨테이너의 설계도.
# gcloud run deploy --source . 실행 시 Cloud Build가 이 파일로 이미지를 만든다.
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run은 PORT 환경 변수로 포트를 지정한다 (기본 8080)
ENV PORT=8080
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
