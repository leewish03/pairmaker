from pair_maker import OptimizedPairMaker
import random

def test_algorithm_limits():
    """알고리즘의 한계를 테스트"""
    
    print("🧪 알고리즘 한계 테스트 시작")
    print("="*50)
    
    # 테스트 케이스들
    test_cases = [
        {"people": 6, "arrangements": 5, "desc": "6명 5배치 (이론적 한계)"},
        {"people": 8, "arrangements": 7, "desc": "8명 7배치 (28개 중 28개 사용)"},
        {"people": 10, "arrangements": 8, "desc": "10명 8배치 (45개 중 40개 사용)"},
        {"people": 12, "arrangements": 10, "desc": "12명 10배치 (66개 중 60개 사용)"},
    ]
    
    for case in test_cases:
        print(f"\n📊 {case['desc']}")
        people_list = list(range(1, case['people'] + 1))
        
        total_possible = case['people'] * (case['people'] - 1) // 2
        needed = case['arrangements'] * (case['people'] // 2)
        usage_rate = (needed / total_possible) * 100
        
        print(f"   총 가능한 조합: {total_possible}개")
        print(f"   필요한 조합: {needed}개")
        print(f"   사용률: {usage_rate:.1f}%")
        
        # 실제 테스트
        pair_maker = OptimizedPairMaker()
        try:
            successful_count, error_message = pair_maker.generate_multiple_arrangements(
                people_list, case['arrangements']
            )
            
            if successful_count == case['arrangements']:
                print(f"   ✅ 성공: {successful_count}개 배치 생성")
            else:
                print(f"   ⚠️ 부분 성공: {successful_count}/{case['arrangements']}개 배치 생성")
                if error_message:
                    print(f"      오류: {error_message}")
                    
        except Exception as e:
            print(f"   ❌ 실패: {str(e)}")
    
    print("\n" + "="*50)
    print("🔍 결론: 사용률이 70% 이상일 때 문제 발생 가능성 높음")

if __name__ == "__main__":
    test_algorithm_limits() 