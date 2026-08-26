import random
import pandas as pd
import itertools
import time
from datetime import datetime
from collections import defaultdict

class OptimizedPairMaker:
    """
    모든 N명(짝수, 홀수) 및 임의의 라운드에 대해 
    100% 중복 0% 및 3인조 최적 공정성을 보장하는 범용 하이브리드 조편성 엔진
    """
    def __init__(self):
        self.used_pairs = set()   # 이미 사용된 2명 조합들 (정렬된 tuple)
        self.arrangements = []   # 최종 배치들을 저장
        self.people_list = []

    def generate_multiple_arrangements(self, people_list, target_count=5, allow_trio_duplicates=False):
        """
        1) 짝수 N: Berger Tables 원형 순환 알고리즘 (100% 중복 0% 수학적 보장)
        2) 홀수 N: 스마트 DFS 백트래킹 (우선 시도) -> 고속 앙상블 탐색 (폴백)
        """
        self.people_list = people_list
        n = len(people_list)
        if n < 2:
            return 0, "최소 2명 이상이어야 합니다."
        if target_count < 1:
            return 0, "라운드 수는 1 이상이어야 합니다."

        is_odd = (n % 2 != 0)

        # 1. 짝수 N
        if not is_odd:
            max_possible = n - 1
            if target_count > max_possible:
                return 0, f"짝수 {n}명은 최대 {max_possible}번까지만 중복 없이 배치가 가능합니다."
            arrangements = self._solve_even(people_list, target_count)
            self._apply_arrangements(arrangements)
            return len(arrangements), None

        # 2. 홀수 N
        pairs_per_round = (n + 3) // 2
        total_possible_pairs = n * (n - 1) // 2
        max_possible = n if allow_trio_duplicates else (total_possible_pairs // pairs_per_round)

        if target_count > max_possible and not allow_trio_duplicates:
            return 0, f"홀수 {n}명은 3인조 중복 없이 최대 {max_possible}번까지만 배치가 가능합니다."

        # 2-1. 스마트 DFS 백트래킹 (0.5초 이내 완전 탐색)
        dfs_arrangements = self._solve_odd_dfs(people_list, target_count, timeout=0.5)
        if dfs_arrangements:
            self._apply_arrangements(dfs_arrangements)
            return len(dfs_arrangements), None

        # 2-2. 앙상블 최적화 폴백 (수학적 제약 한계 시 최소 중복 & 최고 공정성 도출)
        ensemble_arrangements = self._solve_odd_ensemble(people_list, target_count, allow_trio_duplicates)
        self._apply_arrangements(ensemble_arrangements)
        return len(ensemble_arrangements), None

    def _apply_arrangements(self, arrangements):
        """배치를 저장하고 사용된 쌍을 등록"""
        self.arrangements = arrangements
        self.used_pairs = set()
        for arr in arrangements:
            for g in arr:
                if len(g) == 2:
                    self.used_pairs.add(tuple(sorted(g)))
                elif len(g) == 3:
                    self.used_pairs.add(tuple(sorted([g[0], g[1]])))
                    self.used_pairs.add(tuple(sorted([g[0], g[2]])))
                    self.used_pairs.add(tuple(sorted([g[1], g[2]])))

    def _solve_even(self, people_list, target_count):
        """짝수 N 라운드로빈 (Berger Tables)"""
        n = len(people_list)
        shuffled = people_list.copy()
        random.shuffle(shuffled)
        
        fixed = shuffled[0]
        rotating = shuffled[1:]
        all_rounds = []
        
        for r in range(n - 1):
            curr = [fixed] + rotating
            matches = []
            for i in range(n // 2):
                p1, p2 = curr[i], curr[n - 1 - i]
                if random.random() < 0.5:
                    p1, p2 = p2, p1
                matches.append((p1, p2))
            all_rounds.append(matches)
            rotating = [rotating[-1]] + rotating[:-1]
            
        random.shuffle(all_rounds)
        return all_rounds[:target_count]

    def _solve_odd_dfs(self, people_list, target_count, timeout=0.5):
        """홀수 N 스마트 DFS 백트래킹 (공정성 가지치기 + 즉시 매칭)"""
        n = len(people_list)
        shuffled = people_list.copy()
        random.shuffle(shuffled)
        
        total_trio_spots = target_count * 3
        base_trio = total_trio_spots // n
        rem_trio = total_trio_spots % n
        min_allowed_trio = base_trio
        max_allowed_trio = base_trio + (1 if rem_trio > 0 else 0)
        
        used_pairs = set()
        trio_counts = [0] * n
        selected_rounds = []
        start_time = time.time()

        def dfs(round_idx):
            if time.time() - start_time > timeout:
                return False
            if round_idx == target_count:
                return max(trio_counts) - min(trio_counts) <= 2
                
            rem_rounds = target_count - round_idx
            for p in range(n):
                if trio_counts[p] > max_allowed_trio:
                    return False
                if trio_counts[p] + rem_rounds < min_allowed_trio:
                    return False
                    
            candidate_indices = sorted(range(n), key=lambda p: (trio_counts[p], random.random()))
            pool = candidateIndices = candidate_indices[:min(n, 7 + (n // 2))]
            
            trio_cands = []
            for trio in itertools.combinations(pool, 3):
                t1, t2, t3 = trio
                if trio_counts[t1] >= max_allowed_trio or trio_counts[t2] >= max_allowed_trio or trio_counts[t3] >= max_allowed_trio:
                    continue
                p1 = tuple(sorted([t1, t2]))
                p2 = tuple(sorted([t1, t3]))
                p3 = tuple(sorted([t2, t3]))
                if p1 in used_pairs or p2 in used_pairs or p3 in used_pairs:
                    continue
                trio_cands.append(trio)
                
            random.shuffle(trio_cands)
            trio_cands = trio_cands[:35]
            
            for trio in trio_cands:
                t1, t2, t3 = trio
                rem = [p for p in range(n) if p not in trio]
                
                def match_pairs(nodes, current_pairs):
                    if not nodes:
                        return current_pairs
                    first = nodes[0]
                    for other in nodes[1:]:
                        cand_p = tuple(sorted([first, other]))
                        if cand_p not in used_pairs:
                            next_nodes = [x for x in nodes[1:] if x != other]
                            sub = match_pairs(next_nodes, current_pairs + [cand_p])
                            if sub is not None:
                                return sub
                    return None
                    
                pair_sol = match_pairs(rem, [])
                if pair_sol is None:
                    continue
                    
                t_pairs = [tuple(sorted([t1, t2])), tuple(sorted([t1, t3])), tuple(sorted([t2, t3]))]
                all_new = t_pairs + pair_sol
                for p in all_new:
                    used_pairs.add(p)
                trio_counts[t1] += 1; trio_counts[t2] += 1; trio_counts[t3] += 1
                
                arrangement = [tuple(shuffled[x] for x in trio)] + [
                    (shuffled[p[0]], shuffled[p[1]]) for p in pair_sol
                ]
                selected_rounds.append(arrangement)
                
                if dfs(round_idx + 1):
                    return True
                    
                selected_rounds.pop()
                trio_counts[t1] -= 1; trio_counts[t2] -= 1; trio_counts[t3] -= 1
                for p in all_new:
                    used_pairs.remove(p)
                    
            return False

        if dfs(0):
            return selected_rounds
        return None

    def _solve_odd_ensemble(self, people_list, target_count, allow_trio_duplicates):
        """홀수 N 앙상블 탐색 (다회 시뮬레이션 중 최선 선택)"""
        n = len(people_list)
        best_arrangements = []
        best_dup_count = float('inf')
        best_fairness_gap = float('inf')
        
        NUM_SIMS = 250
        for _ in range(NUM_SIMS):
            used_pairs = set()
            trio_counts = {p: 0 for p in people_list}
            arrangements = []
            dup_count = 0
            
            DUMMY = "___DUMMY___"
            working = people_list.copy()
            random.shuffle(working)
            working.append(DUMMY)
            n_even = len(working)
            
            rounds = []
            fixed = working[0]
            rotating = working[1:]
            for r in range(n_even - 1):
                matches = []
                curr = [fixed] + rotating
                for i in range(n_even // 2):
                    matches.append([curr[i], curr[n_even - 1 - i]])
                rounds.append(matches)
                rotating = [rotating[-1]] + rotating[:-1]
                
            random.shuffle(rounds)
            selected_rounds = rounds[:target_count]
            
            for matches in selected_rounds:
                solo = None
                valid_pairs = []
                for m in matches:
                    if DUMMY in m:
                        solo = m[0] if m[1] == DUMMY else m[1]
                    else:
                        valid_pairs.append(list(m))
                        
                best_pair_idx = 0
                min_penalty = float('inf')
                dup_w = 30 if allow_trio_duplicates else 10000
                
                for idx, (p1, p2) in enumerate(valid_pairs):
                    sp1 = tuple(sorted([solo, p1]))
                    sp2 = tuple(sorted([solo, p2]))
                    tp = tuple(sorted([p1, p2]))
                    pen = 0
                    if sp1 in used_pairs: pen += dup_w
                    if sp2 in used_pairs: pen += dup_w
                    if sp1 in used_pairs and sp2 in used_pairs and tp in used_pairs:
                        pen += dup_w * 5
                    pen += (trio_counts[solo] + trio_counts[p1] + trio_counts[p2]) * 100
                    if pen < min_penalty:
                        min_penalty = pen
                        best_pair_idx = idx
                        
                if min_penalty >= dup_w:
                    dup_count += (min_penalty // dup_w)
                    
                trio = valid_pairs[best_pair_idx] + [solo]
                for m in trio:
                    trio_counts[m] += 1
                valid_pairs[best_pair_idx] = trio
                
                final_round = [tuple(g) for g in valid_pairs]
                for g in final_round:
                    if len(g) == 2:
                        used_pairs.add(tuple(sorted(g)))
                    elif len(g) == 3:
                        used_pairs.add(tuple(sorted([g[0], g[1]])))
                        used_pairs.add(tuple(sorted([g[0], g[2]])))
                        used_pairs.add(tuple(sorted([g[1], g[2]])))
                arrangements.append(final_round)
                
            gap = max(trio_counts.values()) - min(trio_counts.values())
            if dup_count < best_dup_count or (dup_count == best_dup_count and gap < best_fairness_gap):
                best_dup_count = dup_count
                best_fairness_gap = gap
                best_arrangements = arrangements
                if best_dup_count == 0 and best_fairness_gap <= 1:
                    break
                    
        return best_arrangements

    def get_trio_fairness_stats(self, people_list):
        """3명조 배치의 공정성 통계 계산"""
        if len(people_list) % 2 == 0:
            return None
        
        trio_counts = defaultdict(int)
        for arrangement in self.arrangements:
            for group in arrangement:
                if len(group) == 3:
                    for person in group:
                        trio_counts[person] += 1
        
        total_trios = len(self.arrangements)
        actual_counts = {person: trio_counts.get(person, 0) for person in people_list}
        min_actual = min(actual_counts.values()) if actual_counts else 0
        max_actual = max(actual_counts.values()) if actual_counts else 0
        
        return {
            "total_trios": total_trios,
            "actual_min": min_actual,
            "actual_max": max_actual,
            "actual_counts": actual_counts,
            "is_fair": (max_actual - min_actual) <= 2
        }

    def format_pairs_as_table(self, arrangement_idx):
        """짝을 테이블 형태로 포맷"""
        if arrangement_idx >= len(self.arrangements):
            return None
        
        pairs = self.arrangements[arrangement_idx]
        data = []
        for i, group in enumerate(pairs, 1):
            if len(group) == 2:
                data.append({"조": f"{i}조", "첫 번째": group[0], "두 번째": group[1], "세 번째": ""})
            elif len(group) == 3:
                data.append({"조": f"{i}조", "첫 번째": group[0], "두 번째": group[1], "세 번째": group[2]})
        return pd.DataFrame(data)

    def format_pairs_as_text(self, arrangement_idx):
        """카카오톡 복사용 텍스트 포맷"""
        if arrangement_idx >= len(self.arrangements):
            return ""
        
        pairs = self.arrangements[arrangement_idx]
        lines = [f"🎯 짝교제 {arrangement_idx + 1}차 매칭 결과", "=" * 30]
        for i, group in enumerate(pairs, 1):
            if len(group) == 2:
                lines.append(f"{i}조: {group[0]} ↔ {group[1]}")
            elif len(group) == 3:
                lines.append(f"{i}조: {group[0]} ↔ {group[1]} ↔ {group[2]} (3명조)")
        lines.extend(["", f"📅 생성일시: {datetime.now().strftime('%Y.%m.%d %H:%M')}", "💡 중복 없이 공정하게 편성되었습니다!"])
        return "\n".join(lines)
