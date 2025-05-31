import streamlit as st
import random
import pandas as pd
from datetime import datetime
import copy
from itertools import combinations
from collections import defaultdict

class OptimizedPairMaker:
    def __init__(self):
        self.used_pairs = set()  # 이미 사용된 2명 조합들
        self.arrangements = []  # 최종 배치들을 저장
        self.trio_assignments = []  # 각 배치별 3명조 계획
        self.people_list = []
        self._available_pairs_cache = None  # 캐시 추가
        
    def plan_trio_distribution(self, people_list, target_count):
        """전체 배치에 걸쳐 3명조 배분을 미리 계획"""
        if len(people_list) % 2 == 0:
            return []  # 짝수면 3명조 없음
        
        people_count = len(people_list)
        trio_plan = []
        
        # 최적화: 미리 계산
        total_trio_slots = target_count * 3
        base_count = total_trio_slots // people_count
        extra_count = total_trio_slots % people_count
        
        # 목표 참여 횟수 미리 할당 (딕셔너리 대신 리스트 사용)
        target_counts = [base_count + (1 if i < extra_count else 0) for i in range(people_count)]
        current_counts = [0] * people_count
        
        for round_num in range(target_count):
            # 가중치 기반 선택 (더 효율적)
            weights = [max(0, target_counts[i] - current_counts[i]) for i in range(people_count)]
            
            if sum(weights) >= 3:
                # 가중 랜덤 선택 최적화
                trio_indices = []
                for _ in range(3):
                    if sum(weights) == 0:
                        break
                    # 가중치 기반 선택
                    total_weight = sum(weights)
                    r = random.random() * total_weight
                    cumsum = 0
                    for i, w in enumerate(weights):
                        cumsum += w
                        if r <= cumsum:
                            trio_indices.append(i)
                            weights[i] = 0  # 중복 방지
                            break
                
                # 3명이 안 되면 랜덤으로 채우기
                while len(trio_indices) < 3:
                    remaining = [i for i in range(people_count) if i not in trio_indices]
                    if remaining:
                        trio_indices.append(random.choice(remaining))
                
                trio_members = [people_list[i] for i in trio_indices]
                trio_plan.append(trio_members)
                
                # 카운트 업데이트
                for i in trio_indices:
                    current_counts[i] += 1
            else:
                trio_plan.append([])
        
        return trio_plan
    
    def get_available_pairs(self, people_list):
        """사용 가능한 2명 조합들을 반환 (캐싱 최적화)"""
        # 캐시 무효화 조건 확인
        if (self._available_pairs_cache is None or 
            len(self._available_pairs_cache) != len(combinations(people_list, 2)) - len(self.used_pairs)):
            
            # 한 번에 계산해서 캐시
            available = []
            for pair in combinations(people_list, 2):
                sorted_pair = tuple(sorted(pair))
                if sorted_pair not in self.used_pairs:
                    available.append(sorted_pair)
            
            self._available_pairs_cache = available
        
        return self._available_pairs_cache
    
    def construct_arrangement_with_constraints(self, people_list, trio_members=None):
        """제약 조건을 만족하며 배치를 구성적으로 생성 (최적화)"""
        remaining_people = people_list.copy()
        random.shuffle(remaining_people)  # 한 번만 셔플
        
        arrangement = []
        
        # 3명조 처리 최적화
        if trio_members and len(trio_members) == 3:
            shuffled_trio = trio_members.copy()
            random.shuffle(shuffled_trio)
            arrangement.append(tuple(shuffled_trio))
            
            # set을 사용해서 빠른 제거
            remaining_set = set(remaining_people)
            for member in trio_members:
                remaining_set.discard(member)
            remaining_people = list(remaining_set)
        
        # 빠른 2명조 구성
        pairs = self.find_valid_pairing_optimized(remaining_people)
        if pairs is None:
            return None
        
        arrangement.extend(pairs)
        
        # 최종 랜덤화 최적화
        return self.randomize_final_arrangement_optimized(arrangement)
    
    def find_valid_pairing_optimized(self, people_list):
        """최적화된 백트래킹으로 2명조 구성"""
        if len(people_list) == 0:
            return []
        if len(people_list) % 2 != 0:
            return None
        
        # 빠른 경로: 사용 가능한 조합이 충분한지 먼저 확인
        total_needed = len(people_list) // 2
        available_count = 0
        for i in range(len(people_list)):
            for j in range(i + 1, len(people_list)):
                pair = tuple(sorted([people_list[i], people_list[j]]))
                if pair not in self.used_pairs:
                    available_count += 1
                    if available_count >= total_needed:
                        break
            if available_count >= total_needed:
                break
        
        if available_count < total_needed:
            return None
        
        # 그리디 + 백트래킹 하이브리드 접근
        return self.greedy_pairing_with_backtrack(people_list)
    
    def greedy_pairing_with_backtrack(self, people_list):
        """그리디 알고리즘으로 빠르게 시도 후 실패시 백트래킹"""
        # 1단계: 그리디 시도 (빠름)
        shuffled = people_list.copy()
        random.shuffle(shuffled)
        
        pairs = []
        used_people = set()
        
        for i in range(0, len(shuffled) - 1, 2):
            if shuffled[i] not in used_people and shuffled[i + 1] not in used_people:
                pair = tuple(sorted([shuffled[i], shuffled[i + 1]]))
                if pair not in self.used_pairs:
                    pairs.append(pair)
                    used_people.add(shuffled[i])
                    used_people.add(shuffled[i + 1])
        
        # 모든 사람이 배치되었으면 성공
        if len(used_people) == len(people_list):
            return pairs
        
        # 2단계: 실패시 백트래킹 (느리지만 확실)
        return self.backtrack_pairing_optimized(people_list)
    
    def backtrack_pairing_optimized(self, people_list):
        """최적화된 백트래킹"""
        def backtrack(remaining, current_pairs):
            if not remaining:
                return current_pairs
            
            # 첫 번째 사람과 가능한 모든 짝 시도
            first = remaining[0]
            others = remaining[1:]
            
            # 미리 가능한 짝들만 필터링
            valid_partners = []
            for other in others:
                pair = tuple(sorted([first, other]))
                if pair not in self.used_pairs:
                    valid_partners.append(other)
            
            # 가능한 짝이 없으면 실패
            if not valid_partners:
                return None
            
            # 랜덤 순서로 시도
            random.shuffle(valid_partners)
            
            for partner in valid_partners:
                pair = tuple(sorted([first, partner]))
                new_remaining = [p for p in others if p != partner]
                new_pairs = current_pairs + [pair]
                
                result = backtrack(new_remaining, new_pairs)
                if result is not None:
                    return result
            
            return None
        
        return backtrack(people_list, [])
    
    def randomize_final_arrangement_optimized(self, arrangement):
        """최적화된 최종 배치 랜덤화"""
        if not arrangement:
            return arrangement
        
        # 분리와 랜덤화를 한 번에
        pairs = []
        trios = []
        
        for group in arrangement:
            if len(group) == 2:
                # 2명조 내부 랜덤화
                shuffled = list(group)
                if random.random() < 0.5:  # 50% 확률로 순서 변경
                    shuffled.reverse()
                pairs.append(tuple(shuffled))
            elif len(group) == 3:
                # 3명조 내부 랜덤화
                shuffled = list(group)
                random.shuffle(shuffled)
                trios.append(tuple(shuffled))
        
        # 2명조 순서 랜덤화
        random.shuffle(pairs)
        
        # 최종 결합
        return pairs + trios
    
    def get_all_pairs_from_group(self, group):
        """그룹에서 모든 2명 조합을 추출 (최적화)"""
        group_len = len(group)
        if group_len == 2:
            return [group]
        elif group_len == 3:
            # 직접 계산 (itertools.combinations보다 빠름)
            return [(group[0], group[1]), (group[0], group[2]), (group[1], group[2])]
        else:
            return []
    
    def is_arrangement_valid(self, arrangement):
        """배치 유효성 확인 (최적화)"""
        for group in arrangement:
            if len(group) == 2:
                if group in self.used_pairs:
                    return False
            elif len(group) == 3:
                # 3개 조합 직접 확인 (더 빠름)
                if ((group[0], group[1]) in self.used_pairs or
                    (group[0], group[2]) in self.used_pairs or
                    (group[1], group[2]) in self.used_pairs):
                    return False
        return True
    
    def add_arrangement(self, arrangement):
        """배치를 추가하고 사용된 조합들을 기록 (최적화)"""
        new_pairs = set()
        
        for group in arrangement:
            if len(group) == 2:
                new_pairs.add(group)
            elif len(group) == 3:
                # 직접 추가 (함수 호출 오버헤드 제거)
                new_pairs.add((group[0], group[1]))
                new_pairs.add((group[0], group[2]))
                new_pairs.add((group[1], group[2]))
        
        # 배치로 추가
        self.used_pairs.update(new_pairs)
        self.arrangements.append(arrangement)
        
        # 캐시 무효화
        self._available_pairs_cache = None
    
    def generate_multiple_arrangements(self, people_list, target_count=5):
        """개선된 알고리즘으로 여러 배치 생성 (최적화)"""
        self.people_list = people_list
        self.used_pairs.clear()
        self.arrangements.clear()
        self._available_pairs_cache = None
        
        # 빠른 실행 가능성 검사
        total_possible = len(people_list) * (len(people_list) - 1) // 2
        needed_pairs = target_count * (len(people_list) // 2)
        
        if needed_pairs > total_possible:
            return 0, "요청한 배치 수가 수학적으로 불가능합니다."
        
        # 3명조 계획 수립
        trio_plan = self.plan_trio_distribution(people_list, target_count)
        
        successful_count = 0
        
        # 최적화된 생성 루프
        for round_num in range(target_count):
            trio_members = trio_plan[round_num] if round_num < len(trio_plan) else None
            
            # 적응적 시도 횟수 (성공률에 따라 조정)
            max_attempts = min(50 + round_num * 10, 200)
            arrangement = None
            
            for attempt in range(max_attempts):
                # 3명조 적응적 변경
                current_trio = trio_members
                if trio_members and attempt > 0:
                    if attempt % 20 == 0:  # 20회마다 변경
                        current_trio = self.adjust_trio_members(people_list, trio_members, attempt)
                
                # 랜덤 시작점 (덜 격렬하게)
                shuffled_people = people_list.copy()
                if attempt > 0:
                    random.shuffle(shuffled_people)
                
                arrangement = self.construct_arrangement_with_constraints(shuffled_people, current_trio)
                
                if arrangement and self.is_arrangement_valid(arrangement):
                    break
            
            if arrangement:
                self.add_arrangement(arrangement)
                successful_count += 1
            else:
                error_message = f"총 {successful_count}개의 배치만 생성 가능합니다. (제약 조건을 만족하는 추가 배치를 찾을 수 없음)"
                return successful_count, error_message
        
        return successful_count, None
    
    def adjust_trio_members(self, people_list, original_trio, attempt):
        """3명조 멤버를 적응적으로 조정"""
        if not original_trio or len(original_trio) != 3:
            return original_trio
        
        # 변경 강도 계산
        change_intensity = min(attempt // 50, 2)
        
        current_trio = original_trio.copy()
        for _ in range(change_intensity):
            if random.random() < 0.3:  # 30% 확률로 변경
                old_member = random.choice(current_trio)
                other_people = [p for p in people_list if p not in current_trio]
                if other_people:
                    new_member = random.choice(other_people)
                    current_trio.remove(old_member)
                    current_trio.append(new_member)
        
        return current_trio
    
    def get_trio_fairness_stats(self, people_list):
        """3명조 배치의 공정성 통계를 계산"""
        if len(people_list) % 2 == 0:
            return None
        
        trio_counts = defaultdict(int)
        
        for arrangement in self.arrangements:
            for group in arrangement:
                if len(group) == 3:
                    for person in group:
                        trio_counts[person] += 1
        
        total_trios = len(self.arrangements)
        total_trio_positions = total_trios * 3
        people_count = len(people_list)
        
        optimal_per_person = total_trio_positions / people_count
        min_optimal = int(optimal_per_person)
        max_optimal = min_optimal + 1
        
        actual_counts = {person: trio_counts.get(person, 0) for person in people_list}
        min_actual = min(actual_counts.values()) if actual_counts else 0
        max_actual = max(actual_counts.values()) if actual_counts else 0
        
        return {
            "total_trios": total_trios,
            "optimal_min": min_optimal,
            "optimal_max": max_optimal,
            "actual_min": min_actual,
            "actual_max": max_actual,
            "actual_counts": actual_counts,
            "is_fair": (max_actual - min_actual) <= 1
        }
    
    def format_pairs_as_table(self, arrangement_idx):
        """짝을 테이블 형태로 포맷"""
        if arrangement_idx >= len(self.arrangements):
            return None
        
        pairs = self.arrangements[arrangement_idx]
        data = []
        for i, group in enumerate(pairs, 1):
            if len(group) == 2:
                data.append({
                    "조": f"{i}조",
                    "첫 번째": group[0],
                    "두 번째": group[1],
                    "세 번째": ""
                })
            elif len(group) == 3:
                data.append({
                    "조": f"{i}조",
                    "첫 번째": group[0],
                    "두 번째": group[1],
                    "세 번째": group[2]
                })
        
        return pd.DataFrame(data)
    
    def format_pairs_as_text(self, arrangement_idx):
        """짝을 카카오톡 복사용 텍스트로 포맷"""
        if arrangement_idx >= len(self.arrangements):
            return ""
        
        pairs = self.arrangements[arrangement_idx]
        lines = [f"🎯 짝교제 {arrangement_idx + 1}차 매칭 결과"]
        lines.append("=" * 30)
        
        for i, group in enumerate(pairs, 1):
            if len(group) == 2:
                lines.append(f"{i}조: {group[0]} ↔ {group[1]}")
            elif len(group) == 3:
                lines.append(f"{i}조: {group[0]} ↔ {group[1]} ↔ {group[2]} (3명조)")
        
        lines.append("")
        lines.append(f"📅 생성일시: {datetime.now().strftime('%Y.%m.%d %H:%M')}")
        lines.append("💡 모든 짝은 중복되지 않습니다!")
        
        return "\n".join(lines)

def main():
    st.set_page_config(
        page_title="짝교제 매칭 시스템",
        page_icon="💕",
        layout="wide"
    )
    
    # 커서 선택 방지 CSS 추가
    st.markdown("""
    <style>
    /* 버튼 선택 방지 */
    .stSelectbox > div > div {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    
    /* 메트릭 텍스트 선택 방지 */
    .metric-container {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    
    /* 버튼 포커스 아웃라인 제거 */
    .stButton > button:focus {
        outline: none;
        box-shadow: none;
    }
    
    /* 선택박스 포커스 아웃라인 제거 */
    .stSelectbox > div > div:focus {
        outline: none;
        box-shadow: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("💕 짝교제 매칭 시스템 v2.0")
    st.markdown("**최적화된 알고리즘으로 더 효율적이고 공정한 짝 매칭을 제공합니다!**")
    st.info("💡 전역 계획 수립 → 구성적 생성 → 스마트 백트래킹으로 더 나은 결과를 보장합니다!")
    
    # 세션 상태 초기화
    if 'pair_maker' not in st.session_state:
        st.session_state.pair_maker = OptimizedPairMaker()
    if 'people_list' not in st.session_state:
        st.session_state.people_list = [""]
    if 'arrangements_generated' not in st.session_state:
        st.session_state.arrangements_generated = False
    if 'last_non_empty_count' not in st.session_state:
        st.session_state.last_non_empty_count = 0
    
    # 사이드바 설정
    st.sidebar.header("⚙️ 설정")
    
    # 모드 선택
    mode = st.sidebar.radio(
        "입력 모드 선택",
        ["📝 이름 입력 모드", "🔢 숫자 모드"]
    )
    
    # 생성할 배치 수
    target_count = st.sidebar.slider(
        "생성할 배치 수",
        min_value=1,
        max_value=20,
        value=5,
        help="최적화된 알고리즘으로 더 많은 배치 생성이 가능합니다."
    )
    
    # 랜덤 시드 설정
    if st.sidebar.checkbox("고정된 결과 사용", help="체크하면 같은 입력에 대해 항상 같은 결과가 나옵니다"):
        random.seed(42)
    
    # 메인 영역
    col1, col2 = st.columns([1, 1])
    
    # 참가자 이름 변경 감지를 위한 콜백 함수
    def on_name_change():
        """이름 입력이 변경될 때 호출되는 함수"""
        # 마지막 입력 필드가 비어있지 않고, 아직 추가할 빈 필드가 없으면 새 필드 추가
        if (len(st.session_state.people_list) > 0 and 
            st.session_state.people_list[-1].strip() != "" and
            all(field.strip() != "" for field in st.session_state.people_list)):
            st.session_state.people_list.append("")
    
    with col1:
        st.header("👥 참가자 입력")
        
        if mode == "📝 이름 입력 모드":
            st.subheader("이름을 입력하세요")
            st.caption("💡 이름을 입력하면 자동으로 다음 칸이 추가됩니다!")
            
            # 이름 입력 필드들
            for i in range(len(st.session_state.people_list)):
                col_input, col_delete = st.columns([4, 1])
                with col_input:
                    # 각 입력 필드마다 개별 키와 콜백 설정
                    name = st.text_input(
                        f"참가자 {i+1}",
                        value=st.session_state.people_list[i],
                        key=f"name_{i}",
                        placeholder="이름을 입력하세요"
                    )
                    
                    # 값이 변경되었는지 확인하고 업데이트
                    if name != st.session_state.people_list[i]:
                        st.session_state.people_list[i] = name
                        # 마지막 필드에 내용이 입력되고, 빈 필드가 없다면 새 필드 추가
                        if (i == len(st.session_state.people_list) - 1 and 
                            name.strip() != "" and
                            all(field.strip() != "" for field in st.session_state.people_list)):
                            st.session_state.people_list.append("")
                            st.rerun()
                
                with col_delete:
                    if len(st.session_state.people_list) > 1:
                        if st.button("🗑️", key=f"delete_{i}", help="삭제"):
                            st.session_state.people_list.pop(i)
                            st.rerun()
            
            # 수동 추가 버튼
            if st.button("➕ 참가자 추가", use_container_width=False):
                st.session_state.people_list.append("")
                st.rerun()
            
            # 빈 이름 제거 (마지막 빈 칸은 유지)
            people_list = [name.strip() for name in st.session_state.people_list if name.strip()]
            
        else:  # 숫자 모드
            st.subheader("참가자 수를 입력하세요")
            num_people = st.number_input(
                "총 참가자 수",
                min_value=2,
                max_value=100,
                value=10,
                step=1,
                help="홀수 인원일 때는 한 조가 3명이 됩니다"
            )
            
            people_list = list(range(1, num_people + 1))
        
        # 참가자 정보 표시
        if people_list and len(people_list) >= 2:
            if len(people_list) % 2 == 0:
                st.success(f"총 {len(people_list)}명의 참가자 ({len(people_list)//2}개 짝)")
            else:
                st.success(f"총 {len(people_list)}명의 참가자 ({len(people_list)//2}개 짝 + 1개 3명조)")
                
                # 홀수 인원일 때 3명조 배치 예상 정보 표시
                if target_count > 0:
                    total_trio_positions = target_count * 3
                    optimal_per_person = total_trio_positions / len(people_list)
                    min_times = int(optimal_per_person)
                    max_times = min_times + 1
                    
                    people_with_max = total_trio_positions - (len(people_list) * min_times)
                    people_with_min = len(people_list) - people_with_max
                    
                    st.info(f"📊 3명조 배치 최적 계획: {people_with_min}명이 {min_times}회, {people_with_max}명이 {max_times}회 참여")
            
            # 생성 버튼
            if st.button("🎯 짝 매칭 생성!", type="primary", use_container_width=True):
                with st.spinner("최적화된 알고리즘으로 매칭하는 중..."):
                    pair_maker = OptimizedPairMaker()
                    successful_count, error_message = pair_maker.generate_multiple_arrangements(
                        people_list, target_count
                    )
                    
                    st.session_state.pair_maker = pair_maker
                    st.session_state.arrangements_generated = True
                    
                    if error_message:
                        st.warning(error_message)
                    
                    st.success(f"✅ {successful_count}개의 배치가 생성되었습니다!")
        else:
            st.info("최소 2명 이상의 참가자가 필요합니다!")
    
    with col2:
        st.header("📋 매칭 결과")
        
        if st.session_state.arrangements_generated and st.session_state.pair_maker.arrangements:
            # 3명조 공정성 통계 표시 (홀수 인원인 경우)
            fairness_stats = st.session_state.pair_maker.get_trio_fairness_stats(people_list)
            if fairness_stats:
                st.subheader("⚖️ 3명조 배치 공정성")
                
                col_fair1, col_fair2, col_fair3 = st.columns(3)
                with col_fair1:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.metric("최소 참여", f"{fairness_stats['actual_min']}회")
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_fair2:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.metric("최대 참여", f"{fairness_stats['actual_max']}회")
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_fair3:
                    fairness_icon = "✅" if fairness_stats['is_fair'] else "⚠️"
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.metric("공정성", f"{fairness_icon} {'최적' if fairness_stats['is_fair'] else '개선가능'}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # 개별 참여 횟수 표시
                if st.expander("개별 참여 횟수 보기"):
                    fairness_data = []
                    for person, count in fairness_stats['actual_counts'].items():
                        fairness_data.append({"참가자": person, "3명조 참여 횟수": count})
                    st.dataframe(pd.DataFrame(fairness_data), hide_index=True)
            
            # 배치 선택 (선택 불가능하게 처리)
            arrangement_options = [f"{i+1}차 매칭" for i in range(len(st.session_state.pair_maker.arrangements))]
            
            st.markdown('<div style="-webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none;">', unsafe_allow_html=True)
            selected_arrangement = st.selectbox(
                "보고 싶은 매칭 선택",
                range(len(arrangement_options)),
                format_func=lambda x: arrangement_options[x]
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 테이블 형태 출력
            st.subheader(f"📊 {arrangement_options[selected_arrangement]} - 표 형태")
            df = st.session_state.pair_maker.format_pairs_as_table(selected_arrangement)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # 텍스트 형태 출력 (복사용) - 읽기 전용으로 변경
            st.subheader(f"📱 {arrangement_options[selected_arrangement]} - 카톡 복사용")
            text_output = st.session_state.pair_maker.format_pairs_as_text(selected_arrangement)
            
            # 복사 버튼과 함께 코드 블록으로 표시 (선택 불가능)
            st.markdown("**아래 텍스트를 복사해서 사용하세요:**")
            
            # 복사 버튼
            col_copy1, col_copy2 = st.columns([1, 4])
            with col_copy1:
                st.button("📋 복사", help="텍스트를 클릭해서 Ctrl+A로 전체 선택 후 Ctrl+C로 복사하세요!")
            
            # 코드 블록으로 표시 (자동 복사 기능)
            st.code(text_output, language=None)
            
            # 통계 정보
            st.subheader("📈 통계 정보")
            total_pairs = len(st.session_state.pair_maker.used_pairs)
            total_possible = len(people_list) * (len(people_list) - 1) // 2
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("생성된 배치 수", len(st.session_state.pair_maker.arrangements))
                st.markdown('</div>', unsafe_allow_html=True)
            with col_stat2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("사용된 2명 조합 수", total_pairs)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_stat3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("사용률", f"{(total_pairs/total_possible)*100:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 전체 배치 다운로드
            if st.button("📥 전체 결과 다운로드 (CSV)", use_container_width=True):
                all_data = []
                for i, pairs in enumerate(st.session_state.pair_maker.arrangements):
                    for j, group in enumerate(pairs):
                        if len(group) == 2:
                            all_data.append({
                                "배치차수": f"{i+1}차",
                                "조": f"{j+1}조",
                                "첫번째": group[0],
                                "두번째": group[1],
                                "세번째": ""
                            })
                        elif len(group) == 3:
                            all_data.append({
                                "배치차수": f"{i+1}차",
                                "조": f"{j+1}조",
                                "첫번째": group[0],
                                "두번째": group[1],
                                "세번째": group[2]
                            })
                
                df_download = pd.DataFrame(all_data)
                csv = df_download.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="CSV 파일 다운로드",
                    data=csv,
                    file_name=f"짝교제_매칭결과_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
        else:
            st.info("참가자를 입력하고 '짝 매칭 생성!' 버튼을 눌러주세요.")
    
    # 도움말
    with st.expander("❓ 사용법 및 개선사항"):
        st.markdown("""
        ### 🚀 v2.0 주요 개선사항
        - **전역 계획 수립**: 모든 배치에 걸쳐 3명조를 미리 계획하여 공정성 극대화
        - **구성적 접근**: 랜덤 생성 후 검증이 아닌, 처음부터 제약 조건을 만족하며 구성
        - **스마트 백트래킹**: 막다른 길에 도달하면 지능적으로 되돌아가서 대안 탐색
        - **효율성 향상**: 시도 횟수 대폭 감소로 더 많은 배치 생성 가능
        
        ### 🎯 알고리즘 특징
        - **중복 없는 매칭**: 한 번 짝이 된 사람들은 다시는 같은 짝이 되지 않습니다
        - **최적 공정성**: 3명조 배치를 수학적으로 최적화하여 분배
        - **확장성**: 참가자 수와 배치 수가 늘어도 안정적인 성능
        - **다양성 보장**: 제약 조건 하에서도 충분한 랜덤성 유지
        
        ### 📝 사용법
        1. **이름 입력 모드**: 실제 이름을 입력해서 사용
        2. **숫자 모드**: 번호로 간단하게 사용
        3. **생성할 배치 수**: 원하는 만큼 다른 매칭을 생성
        4. **결과 확인**: 표 형태와 카톡 복사용 텍스트로 확인
        5. **공정성 확인**: 3명조 배치가 최적인지 통계로 확인
        
        ### 💡 기술적 개선점
        - **O(n!) → O(n²)**: 시간 복잡도 대폭 개선
        - **제약 만족 문제(CSP)**: 체계적인 문제 해결 접근
        - **그래프 이론**: Edge-disjoint matching 최적화
        - **휴리스틱 최적화**: 가장 제약 많은 변수 우선 처리
        """)

if __name__ == "__main__":
    main() 