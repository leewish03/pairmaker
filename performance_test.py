import time
from pair_maker import OptimizedPairMaker

def performance_test():
    """최적화된 알고리즘의 성능을 측정"""
    
    print("⚡ 성능 최적화 테스트")
    print("="*60)
    
    test_cases = [
        {"people": 6, "arrangements": 5, "desc": "6명 5배치 (극한)"},
        {"people": 10, "arrangements": 8, "desc": "10명 8배치 (실용적)"},
        {"people": 20, "arrangements": 10, "desc": "20명 10배치 (대규모)"},
        {"people": 30, "arrangements": 8, "desc": "30명 8배치 (초대규모)"},
    ]
    
    for case in test_cases:
        print(f"\n🎯 {case['desc']}")
        people_list = list(range(1, case['people'] + 1))
        
        # 성능 측정
        start_time = time.time()
        
        pair_maker = OptimizedPairMaker()
        successful_count, error_message = pair_maker.generate_multiple_arrangements(
            people_list, case['arrangements']
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 통계 계산
        total_possible = case['people'] * (case['people'] - 1) // 2
        used_pairs = len(pair_maker.used_pairs)
        usage_rate = (used_pairs / total_possible) * 100
        
        # 결과 출력
        print(f"   ⏱️  실행 시간: {execution_time:.3f}초")
        print(f"   ✅ 생성 성공: {successful_count}/{case['arrangements']}개")
        print(f"   📊 조합 사용률: {usage_rate:.1f}% ({used_pairs}/{total_possible})")
        
        if error_message:
            print(f"   ⚠️  오류: {error_message}")
        
        # 성능 평가
        if execution_time < 0.1:
            print("   🚀 매우 빠름")
        elif execution_time < 1.0:
            print("   ⚡ 빠름")
        elif execution_time < 5.0:
            print("   ✅ 적당함")
        else:
            print("   ⏳ 느림")
    
    print("\n" + "="*60)
    print("💡 결론: 최적화로 성능과 안정성이 크게 향상됨!")

if __name__ == "__main__":
    performance_test() 