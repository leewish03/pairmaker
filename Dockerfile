# Python 3.11을 기반으로 하는 공식 이미지 사용
FROM python:3.11-slim

# 작업 디렉터리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY pair_maker.py .

# Streamlit 설정 디렉터리 생성
RUN mkdir -p ~/.streamlit

# Streamlit 설정 파일 생성
RUN echo "\
[general]\n\
email = \"\"\n\
\n\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = 8501\n\
address = 0.0.0.0\n\
\n\
[theme]\n\
base = \"light\"\n\
" > ~/.streamlit/config.toml

# 포트 8501 노출
EXPOSE 8501

# 헬스체크 추가
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Streamlit 애플리케이션 실행
CMD ["streamlit", "run", "pair_maker.py", "--server.port=8501", "--server.address=0.0.0.0"] 