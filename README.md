# 💕 짝교제 매칭 시스템 백엔드 모듈 (v2.0)

이 모듈은 수학적 Round-Robin(Berger Tables) 알고리즘을 사용하여 100% 매칭 성공과 중복 없는 완벽한 조 편성을 보장하는 알고리즘 엔진입니다. 다른 웹 애플리케이션에 API/모듈 형태로 이식하기 위해 경량화되었습니다.

## 🚀 알고리즘 특징
- **중복 0% 보장**: 수학적으로 설계되어 한 번 만난 사람은 절대 다시 매칭되지 않음
- **결정론적 생성**: 기존 타 알고리즘의 "재시도 후 포기(백트래킹)" 방식이 아닌, 대진표 사전 연산 방식으로 O(1) 수준의 압도적인 생성 속도
- **홀수 3명조 공정성**: 앙상블 탐색 로직(50번 시뮬레이션 후 가장 공정한 편성 반환)으로 3명조 편중 현상 방지

## 📋 파일 구성
* `pair_maker.py`: 핵심 매칭 알고리즘 클래스 `OptimizedPairMaker`가 들어있습니다. 이 파일만 가져가서 사용하시면 됩니다.

## 🛠️ 사용 방법 (How to Use in your code)

```python
from pair_maker import OptimizedPairMaker

# 1. 인스턴스 생성
maker = OptimizedPairMaker()

# 2. 명단과 원하는 매칭 횟수(N라운드) 입력
people = ["철수", "영희", "민수", "지영", "동현", "민지", "준호", "지훈"]
target_round_count = 5 

# 3. 매칭 실행
success_count, err_msg = maker.generate_multiple_arrangements(people, target_count=target_round_count)

if err_msg:
    print(f"매칭 실패: {err_msg}")
else:
    print(f"{success_count}번의 매칭을 성공적으로 생성했습니다!")
    
    # 생성된 배치 결과 (리스트)
    # maker.arrangements 에 저장됨
    for i, arrangement in enumerate(maker.arrangements):
        print(f"\n--- {i+1}라운드 ---")
        print(arrangement)
        # 예시 형태: (('철수', '영희'), ('민수', '지영'), ('동현', '민지', '준호'))
```

## 📦 설치 패키지
이 모듈을 사용하기 위해 복잡한 패키지는 거의 필요 없습니다. `pair_maker.py` 하단의 표 포맷팅(선택적 사용)을 위한 `pandas`만 존재하면 실행됩니다.
```bash
pip install pandas
```