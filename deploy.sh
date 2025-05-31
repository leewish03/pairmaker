#!/bin/bash

# 🚀 짝교제 매칭 시스템 배포 스크립트
# 리눅스 서버에서 실행하세요!

echo "🎯 짝교제 매칭 시스템 배포를 시작합니다..."
echo "======================================================"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 에러 핸들링
set -e
trap 'echo -e "${RED}❌ 배포 실패! 라인 $LINENO에서 오류 발생${NC}"' ERR

# 함수 정의
print_status() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 1. 시스템 요구사항 확인
print_status "시스템 요구사항 확인 중..."

# Docker 설치 확인
if ! command -v docker &> /dev/null; then
    print_error "Docker가 설치되지 않았습니다!"
    echo "다음 명령어로 Docker를 설치하세요:"
    echo "curl -fsSL https://get.docker.com -o get-docker.sh"
    echo "sudo sh get-docker.sh"
    echo "sudo usermod -aG docker \$USER"
    exit 1
fi

# Docker Compose 설치 확인
if ! command -v docker-compose &> /dev/null; then
    print_warning "Docker Compose가 설치되지 않았습니다. 설치 중..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

print_success "시스템 요구사항 확인 완료"

# 2. 방화벽 설정 (선택사항)
print_status "방화벽 설정 확인 중..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 8501/tcp
    print_success "포트 8501 방화벽 규칙 추가"
fi

# 3. 로그 디렉터리 생성
print_status "로그 디렉터리 생성 중..."
mkdir -p logs
print_success "로그 디렉터리 생성 완료"

# 4. 기존 컨테이너 정리
print_status "기존 컨테이너 정리 중..."
docker-compose down --remove-orphans 2>/dev/null || true
docker system prune -f
print_success "기존 컨테이너 정리 완료"

# 5. Docker 이미지 빌드 및 실행
print_status "Docker 이미지 빌드 중..."
docker-compose build --no-cache

print_status "애플리케이션 시작 중..."
docker-compose up -d

# 6. 서비스 상태 확인
print_status "서비스 상태 확인 중..."
sleep 10

if docker-compose ps | grep -q "Up"; then
    print_success "✨ 배포 성공!"
    echo ""
    echo "🌐 애플리케이션 접속 정보:"
    echo "   로컬: http://localhost:8501"
    echo "   외부: http://$(curl -s ifconfig.me):8501"
    echo ""
    echo "📋 유용한 명령어들:"
    echo "   로그 확인: docker-compose logs -f"
    echo "   서비스 중지: docker-compose down"
    echo "   서비스 재시작: docker-compose restart"
    echo "   컨테이너 상태: docker-compose ps"
    echo ""
    echo "🎉 짝교제 매칭 시스템이 성공적으로 배포되었습니다!"
else
    print_error "배포 실패! 로그를 확인하세요:"
    docker-compose logs
    exit 1
fi 