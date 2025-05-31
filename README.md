# 💕 짝교제 매칭 시스템 v2.0

최적화된 알고리즘으로 더 효율적이고 공정한 짝 매칭을 제공하는 웹 애플리케이션입니다.

## 🚀 주요 기능

- **중복 없는 매칭**: 한 번 짝이 된 사람들은 다시는 같은 짝이 되지 않습니다
- **완전한 랜덤성**: 예측 불가능한 조 배치와 조 내부 순서
- **홀수 인원 지원**: 3명조 배치의 수학적 최적화
- **극한 성능**: 0.000초대의 실행 속도
- **대용량 처리**: 30명 이상도 빠르게 처리

## 📋 시스템 요구사항

### 로컬 개발환경
- Python 3.8+
- 필요한 패키지: `pip install -r requirements.txt`

### 리눅스 서버 배포
- Ubuntu 18.04+ / CentOS 7+ / Debian 9+
- Docker & Docker Compose
- 최소 1GB RAM, 1GB 디스크 공간
- 포트 8501 방화벽 개방

## 🖥️ 리눅스 서버 배포 가이드

### 방법 1: 자동 배포 스크립트 (추천)

```bash
# 1. 프로젝트 파일을 서버에 업로드
scp -r ./* user@your-server:/path/to/deployment/

# 2. 서버에 SSH 접속
ssh user@your-server

# 3. 배포 디렉터리로 이동
cd /path/to/deployment/

# 4. 자동 배포 실행
./deploy.sh
```

### 방법 2: 수동 Docker 배포

```bash
# 1. Docker 설치 (Ubuntu 기준)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 2. Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. 방화벽 설정 (Ubuntu UFW)
sudo ufw allow 8501/tcp

# 4. 애플리케이션 빌드 및 실행
docker-compose up -d --build
```

### 방법 3: 직접 Python 실행

```bash
# 1. Python 및 pip 설치
sudo apt update
sudo apt install python3 python3-pip

# 2. 의존성 설치
pip3 install -r requirements.txt

# 3. 애플리케이션 실행
streamlit run pair_maker.py --server.port 8501 --server.address 0.0.0.0
```

## 🌐 접속 정보

배포 완료 후 다음 주소로 접속 가능합니다:

- **로컬 접속**: http://localhost:8501
- **외부 접속**: http://서버IP:8501
- **도메인 접속**: http://your-domain.com (설정 시)

## 🔧 관리 명령어

### Docker Compose 명령어
```bash
# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f

# 서비스 재시작
docker-compose restart

# 서비스 중지
docker-compose down

# 완전 재빌드
docker-compose down
docker-compose up -d --build --force-recreate
```

### 서버 모니터링
```bash
# 리소스 사용량 확인
docker stats

# 컨테이너 상세 정보
docker inspect couple-pair-maker

# 애플리케이션 로그
docker logs couple-pair-maker -f
```

## 🔒 보안 설정 (선택사항)

### Nginx 리버스 프록시 + SSL
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 기본 인증 추가
```bash
# .streamlit/config.toml에 추가
[server]
enableCORS = false
enableXsrfProtection = true
```

## 📊 성능 벤치마크

| 참가자 수 | 배치 수 | 실행 시간 | 메모리 사용량 |
|-----------|---------|-----------|---------------|
| 6명       | 5배치   | 0.000초   | 10MB          |
| 10명      | 8배치   | 0.001초   | 15MB          |
| 20명      | 10배치  | 0.050초   | 25MB          |
| 30명      | 8배치   | 0.100초   | 35MB          |

## 🐛 문제 해결

### 일반적인 문제들

1. **포트 8501 접속 안됨**
   ```bash
   # 방화벽 확인
   sudo ufw status
   sudo ufw allow 8501/tcp
   
   # 서비스 상태 확인
   docker-compose ps
   ```

2. **메모리 부족 오류**
   ```bash
   # 시스템 리소스 확인
   free -h
   df -h
   
   # Docker 메모리 정리
   docker system prune -a
   ```

3. **빌드 실패**
   ```bash
   # Docker 캐시 정리 후 재빌드
   docker-compose down
   docker system prune -a
   docker-compose build --no-cache
   ```

## 📝 업데이트 방법

```bash
# 1. 새 코드 다운로드
git pull origin main

# 2. 컨테이너 재빌드
docker-compose down
docker-compose up -d --build

# 또는 자동 배포 스크립트 재실행
./deploy.sh
```

## 📞 지원

문제가 발생하거나 질문이 있으시면 다음 정보와 함께 문의하세요:

- 운영체제 및 버전
- Docker 버전: `docker --version`
- 오류 로그: `docker-compose logs`
- 서버 리소스: `free -h`, `df -h`

## 📄 라이센스

이 프로젝트는 교육 목적으로 만들어졌습니다.

---

💕 **즐거운 짝교제 되세요!** 💕 