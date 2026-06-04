import { useEffect, useState } from 'react';

// ==========================================
// SECTION 1: STYLES
// ==========================================
const STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');
:root{--pm-bg:#f5f3f0;--pm-surface:#fff;--pm-surface-soft:#fefdfc;--pm-surface-muted:#fdf9f7;--pm-text:#3f3a36;--pm-text-strong:#4a423d;--pm-text-muted:#7b7167;--pm-primary:#a07d6c;--pm-primary-soft:#c49a87;--pm-border:#e6e1db;--pm-border-soft:#ede8e3;--pm-shadow:0 4px 20px rgba(138,120,110,.1);--pm-r-lg:20px;--pm-r-md:14px;--pm-r-sm:12px}
*{box-sizing:border-box}
body{margin:0}
.pm-wrap{min-height:100vh;max-width:900px;margin:0 auto;padding:1.2rem 1rem 3rem;background:var(--pm-bg);font-family:'Pretendard',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:var(--pm-text)}
.pm-header{padding:1.5rem 0 1.2rem;text-align:center}
.pm-header-icon{display:inline-block;margin-bottom:.4rem;font-size:2.8rem;animation:pm-toss 1.8s ease-in-out infinite}
@keyframes pm-toss{0%,100%{transform:rotate(0deg) translateY(0)}15%{transform:rotate(-15deg) translateY(-8px)}30%{transform:rotate(10deg) translateY(-3px)}45%{transform:rotate(-5deg) translateY(0)}}
.pm-header h1{margin:0 0 .4rem;font-size:1.9rem;font-weight:700;color:var(--pm-primary)}
.pm-header p{margin:0;font-size:.95rem;color:var(--pm-text-muted)}
.pm-main-nav{display:flex;gap:4px;margin-bottom:1.5rem;padding:4px;background:#eee8e1;border-radius:16px}
.pm-main-tab{flex:1;padding:.75rem;border:none;border-radius:12px;background:transparent;color:var(--pm-text-muted);font:inherit;font-size:.95rem;font-weight:600;cursor:pointer;transition:background .2s,color .2s,box-shadow .2s}
.pm-main-tab.active{background:#fff;color:var(--pm-primary);box-shadow:0 2px 8px rgba(0,0,0,.08)}
.pm-main-tab:hover:not(.active){background:rgba(255,255,255,.5)}
.pm-layout{display:flex;flex-direction:column;gap:1.2rem;width:100%;min-width:0}
.pm-card{min-width:0;padding:1.5rem 1.2rem;background:var(--pm-surface);border-radius:var(--pm-r-lg);box-shadow:var(--pm-shadow)}
.pm-result-card{overflow:hidden}
.pm-step{display:flex;align-items:center;gap:.6rem;margin:1rem 0 .5rem}
.pm-step:first-of-type{margin-top:0}
.pm-step-num{flex-shrink:0;display:flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:999px;background:var(--pm-primary);color:#fff;font-size:.8rem;font-weight:700}
.pm-step label{color:var(--pm-text-strong);font-size:.95rem;font-weight:600}
.pm-textarea-wrap{position:relative;margin-bottom:.5rem}
.pm-textarea{width:100%;height:160px;padding:.9rem;border:1.5px solid var(--pm-border);border-radius:var(--pm-r-md);background:var(--pm-surface-soft);color:var(--pm-text);font:inherit;font-size:1rem;line-height:1.6;resize:vertical;transition:border-color .2s,box-shadow .2s}
.pm-textarea:focus,.pm-num-input:focus{outline:none;border-color:#bfa598;box-shadow:0 0 0 3px rgba(191,165,152,.18)}
.pm-count-badge{position:absolute;right:10px;bottom:10px;pointer-events:none;padding:3px 10px;border-radius:999px;background:#f1ede8;color:var(--pm-text-muted);font-size:.78rem;font-weight:600}
.pm-num-input{width:100%;margin-bottom:1rem;padding:.75rem 1rem;border:1.5px solid var(--pm-border);border-radius:var(--pm-r-md);background:var(--pm-surface-soft);color:var(--pm-text);font:inherit;font-size:1.15rem;font-weight:600;transition:border-color .2s,box-shadow .2s}
.pm-toggle-card{margin-bottom:1rem;padding:1rem 1.1rem;border:1.5px solid #ece4dd;border-radius:var(--pm-r-md);background:var(--pm-surface-muted)}
.pm-toggle-header{display:flex;align-items:center;gap:.8rem}
.pm-toggle-header strong{color:var(--pm-text-strong);font-size:.95rem}
.pm-switch{position:relative;flex-shrink:0;display:inline-block;width:44px;height:24px}
.pm-switch input{width:0;height:0;opacity:0}
.pm-switch-track{position:absolute;inset:0;cursor:pointer;border-radius:999px;background:#d4cec9;transition:background .25s}
.pm-switch-track::before{content:'';position:absolute;top:3px;left:3px;width:18px;height:18px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.2);transition:transform .25s}
.pm-switch input:checked+.pm-switch-track{background:var(--pm-primary)}
.pm-switch input:checked+.pm-switch-track::before{transform:translateX(20px)}
.pm-error{margin-bottom:.8rem;padding:.75rem 1rem;border-left:4px solid #d94f4f;border-radius:var(--pm-r-sm);background:#fdf3f2;color:#d94f4f;font-size:.9rem}
.pm-btn-generate{width:100%;padding:1rem;border:none;border-radius:var(--pm-r-md);background:linear-gradient(135deg,var(--pm-primary),var(--pm-primary-soft));color:#fff;font:inherit;font-size:1.1rem;font-weight:700;letter-spacing:.02em;cursor:pointer;box-shadow:0 4px 14px rgba(160,125,108,.35);transition:transform .2s,box-shadow .2s,opacity .2s}
.pm-btn-generate:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 8px 20px rgba(160,125,108,.4)}
.pm-btn-generate:disabled{opacity:.65;cursor:not-allowed}
.pm-result-title{margin:0 0 1.2rem;padding-bottom:.8rem;border-bottom:2px solid #f3efea;color:var(--pm-text-strong);font-size:1.2rem;font-weight:700}
.pm-fairness{display:flex;align-items:flex-start;gap:.7rem;margin-bottom:1rem;padding:.9rem 1rem;border-radius:var(--pm-r-sm);font-size:.88rem}
.pm-fairness.fair{border:1px solid #c3e5d2;background:#f0f9f4;color:#2b6644}
.pm-fairness.unfair{border:1px solid #e8d89a;background:#fdf8ee;color:#7a5900}
.pm-fairness-text{display:flex;flex-direction:column;gap:.1rem}
.pm-fairness-range{color:inherit;opacity:.92}
.pm-dl-row{display:flex;gap:.75rem;margin-bottom:1rem}
.pm-dl-btn{flex:1;display:flex;align-items:center;justify-content:center;min-width:0;padding:.85rem 1rem;border:none;border-radius:var(--pm-r-md);color:#fff;font:inherit;font-size:.95rem;font-weight:700;cursor:pointer;transition:transform .18s}
.pm-dl-btn:hover{transform:translateY(-1px)}
.pm-dl-btn.csv{background:linear-gradient(135deg,#2f6e50,#4caf7d)}
.pm-dl-btn.img{background:linear-gradient(135deg,#4b5fa6,#7b8fe0)}
.pm-tabs-wrap{width:100%;min-width:0;max-width:100%;margin-bottom:1rem;overflow-x:auto;overflow-y:hidden;padding-bottom:8px;-webkit-overflow-scrolling:touch;scrollbar-width:thin;scrollbar-color:#d8d1ca transparent}
.pm-tabs-wrap::-webkit-scrollbar{height:6px}
.pm-tabs-wrap::-webkit-scrollbar-thumb{background:#d8d1ca;border-radius:999px}
.pm-tabs{display:inline-flex;gap:.4rem;width:max-content;min-width:max-content}
.pm-tab{flex:0 0 auto;padding:.45rem 1rem;border:1.5px solid var(--pm-border);border-radius:999px;background:#fff;color:var(--pm-text-muted);font:inherit;font-size:.9rem;font-weight:600;white-space:nowrap;cursor:pointer;transition:background .18s,border-color .18s,color .18s}
.pm-tab:hover:not(.active){background:#f5f0ec}
.pm-tab.active{border-color:var(--pm-primary);background:var(--pm-primary);color:#fff}
.pm-pairs{display:flex;flex-direction:column;gap:.65rem;margin-bottom:1rem}
.pm-pair{display:flex;align-items:center;gap:.7rem;min-width:0;padding:.85rem 1rem;border:1.5px solid var(--pm-border-soft);border-radius:var(--pm-r-md);background:#fdfcfb;transition:transform .15s}
.pm-pair:hover{transform:translateX(3px)}
.pm-pair.trio{border-color:#f8d4d4;background:#fff8f8}
.pm-pair-num{flex-shrink:0;padding:4px 12px;border-radius:999px;background:#f7ede7;color:var(--pm-primary);font-size:.85rem;font-weight:700}
.pm-pair-names{flex:1;min-width:0;color:var(--pm-text);font-size:1rem;font-weight:500;word-break:keep-all;overflow-wrap:anywhere}
.pm-team-list{display:flex;flex-direction:column;gap:.65rem;margin-bottom:1rem}
.pm-team-row{display:flex;align-items:flex-start;gap:.7rem;min-width:0;padding:.9rem 1rem;border:1.5px solid var(--pm-border-soft);border-radius:var(--pm-r-md);background:#fdfcfb;transition:transform .15s}
.pm-team-row:hover{transform:translateX(3px)}
.pm-team-num{flex-shrink:0;padding:4px 12px;border-radius:999px;background:#e8f0fb;color:#4b5fa6;font-size:.85rem;font-weight:700;margin-top:2px}
.pm-team-members{flex:1;display:flex;flex-wrap:wrap;gap:.4rem;min-width:0}
.pm-member-chip{padding:3px 10px;border-radius:999px;background:#f0ebe5;color:var(--pm-text-strong);font-size:.88rem;font-weight:500}
.pm-btn-copy{width:100%;padding:.85rem;border:none;border-radius:var(--pm-r-md);background:#f5f0ec;color:#5d544f;font:inherit;font-size:.95rem;font-weight:600;cursor:pointer;transition:background .18s}
.pm-btn-copy:hover{background:#ece4dc}
.pm-empty{padding:3rem 1rem;text-align:center;color:#b5afa9}
.pm-empty-icon{display:block;margin-bottom:.8rem;font-size:3rem;opacity:.5}
@media(min-width:720px){.pm-layout{flex-direction:row;align-items:flex-start;gap:1.5rem}.pm-input-card{flex:0 0 340px}.pm-result-card{flex:1;min-width:0}}
@media(max-width:480px){.pm-wrap{padding:1rem .75rem 2.5rem}.pm-header h1{font-size:1.65rem}.pm-card{padding:1.2rem 1rem;border-radius:16px}.pm-btn-generate{padding:.9rem;font-size:1rem}.pm-main-tab{font-size:.85rem;padding:.65rem .5rem}}
`;

// ==========================================
// SECTION 2: CORE ALGORITHMS
// ==========================================
function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ── A. 짝교제(1:1) 매칭 엔진 ──
class OptimizedPairMakerJS {
  constructor() { this.usedPairs = new Set(); this.arrangements = []; }

  generateMultipleArrangements(peopleList, targetCount = 5, allowTrioDuplicates = false) {
    const n = peopleList.length;
    const isOdd = n % 2 !== 0;
    let maxPossible;
    if (isOdd && allowTrioDuplicates) {
      maxPossible = n;
    } else {
      maxPossible = Math.floor(Math.floor((n * (n - 1)) / 2) / Math.floor(n / 2));
    }
    if (targetCount > maxPossible) {
      return { error: `최대 ${maxPossible}번의 배치만 가능합니다. (현재 모드 기준)`, arrangements: [], fairnessStats: null };
    }

    let bestArrangements = [], bestUsedPairs = new Set(), bestScore = Infinity;
    const numSims = isOdd ? 150 : 1;

    for (let sim = 0; sim < numSims; sim++) {
      const simUsedPairs = new Set(), simArrangements = [];
      const roundTrioCounts = {};
      peopleList.forEach(p => { roundTrioCounts[p] = 0; });

      const DUMMY = '___DUMMY___';
      const working = shuffleArray(peopleList);
      if (isOdd) working.push(DUMMY);
      const nEven = working.length, rounds = [];
      const fixed = working[0];
      let rotating = working.slice(1);

      for (let r = 0; r < nEven - 1; r++) {
        const matches = [];
        const curr = [fixed, ...rotating];
        for (let i = 0; i < Math.floor(nEven / 2); i++) {
          let p1 = curr[i], p2 = curr[nEven - 1 - i];
          if (Math.random() < 0.5) [p1, p2] = [p2, p1];
          matches.push([p1, p2]);
        }
        rounds.push(matches);
        rotating = [rotating[rotating.length - 1], ...rotating.slice(0, -1)];
      }

      const selected = shuffleArray(rounds).slice(0, targetCount);
      let totalDup = 0;

      for (const matches of selected) {
        const final = [];
        if (!isOdd) {
          matches.forEach(m => final.push([...m]));
        } else {
          let solo = null;
          const pairs = [];
          matches.forEach(m => {
            if (m.includes(DUMMY)) solo = m[0] === DUMMY ? m[1] : m[0];
            else pairs.push([...m]);
          });
          const dupW = allowTrioDuplicates ? 30 : 100000;
          let bestIdx = 0, minPen = Infinity;
          for (const idx of shuffleArray(Array.from({ length: pairs.length }, (_, i) => i))) {
            const [p1, p2] = pairs[idx];
            const sp1 = [solo, p1].sort().join('|'), sp2 = [solo, p2].sort().join('|'), tp = [p1, p2].sort().join('|');
            let pen = 0;
            if (simUsedPairs.has(sp1)) pen += dupW;
            if (simUsedPairs.has(sp2)) pen += dupW;
            if (simUsedPairs.has(sp1) && simUsedPairs.has(sp2) && simUsedPairs.has(tp)) pen += dupW * 5;
            pen += (roundTrioCounts[solo] + roundTrioCounts[p1] + roundTrioCounts[p2]) * 500;
            if (pen < minPen) { minPen = pen; bestIdx = idx; }
          }
          if (minPen >= dupW) totalDup++;
          const trio = [...pairs[bestIdx], solo];
          trio.forEach(m => { roundTrioCounts[m]++; });
          pairs[bestIdx] = shuffleArray(trio);
          pairs.forEach(g => final.push([...g]));
        }
        final.forEach(g => {
          if (g.length === 2) simUsedPairs.add([...g].sort().join('|'));
          else {
            simUsedPairs.add([g[0], g[1]].sort().join('|'));
            simUsedPairs.add([g[0], g[2]].sort().join('|'));
            simUsedPairs.add([g[1], g[2]].sort().join('|'));
          }
        });
        simArrangements.push(final);
      }

      const counts = Object.values(roundTrioCounts);
      const gap = isOdd ? Math.max(...counts) - Math.min(...counts) : 0;
      const sumSq = isOdd ? counts.reduce((s, v) => s + v * v, 0) : 0;
      const score = totalDup * 50000 + gap * 10000 + sumSq;

      if (score < bestScore) {
        bestScore = score;
        bestArrangements = simArrangements;
        bestUsedPairs = simUsedPairs;
        if (isOdd && totalDup === 0 && gap <= 1) break;
        if (!isOdd && totalDup === 0) break;
      }
    }

    this.arrangements = bestArrangements;
    this.usedPairs = bestUsedPairs;

    let fairnessStats = null;
    if (isOdd) {
      const actual = {};
      peopleList.forEach(p => { actual[p] = 0; });
      bestArrangements.forEach(arr => arr.forEach(g => { if (g.length === 3) g.forEach(m => actual[m]++); }));
      const vals = Object.values(actual);
      const minV = Math.min(...vals), maxV = Math.max(...vals);
      fairnessStats = { min: minV, max: maxV, isFair: maxV - minV <= 1 };
    }
    return { error: null, arrangements: bestArrangements, fairnessStats };
  }
}

// ── B. 단체 팀 매칭 엔진 ──
class OptimizedTeamMakerJS {
  generateArrangements(peopleList, teamCount, rounds, leaders = []) {
    let actualTeamCount = teamCount;
    if (leaders && leaders.length > 0) actualTeamCount = leaders.length;
    
    const n = peopleList.length;
    if (actualTeamCount < 2) return { error: '최소 2팀 이상이어야 합니다.', arrangements: [], dupStats: null };
    if ((!leaders || leaders.length === 0) && actualTeamCount > n) return { error: `팀 수(${actualTeamCount})가 인원수(${n})보다 많을 수 없습니다.`, arrangements: [], dupStats: null };

    const base = n === 0 ? 0 : Math.floor(n / actualTeamCount);
    const rem = n === 0 ? 0 : n % actualTeamCount;
    const sizes = Array.from({ length: actualTeamCount }, (_, i) => base + (i < rem ? 1 : 0));
    const arrangements = [];
    const history = new Set();
    const NUM_SIMS = 1500;

    for (let round = 0; round < rounds; round++) {
      let best = null, bestScore = Infinity;
      for (let sim = 0; sim < NUM_SIMS; sim++) {
        const shuffled = shuffleArray([...peopleList]);
        const candidate = [];
        let idx = 0;
        for (let i = 0; i < sizes.length; i++) {
          const sz = sizes[i];
          const members = shuffled.slice(idx, idx + sz);
          candidate.push((leaders && leaders.length > i) ? [leaders[i], ...members] : members);
          idx += sz;
        }

        let score = 0;
        for (const team of candidate)
          for (let i = 0; i < team.length; i++)
            for (let j = i + 1; j < team.length; j++)
              if (history.has([team[i], team[j]].sort().join('|'))) score++;

        if (score < bestScore) { bestScore = score; best = candidate; if (score === 0) break; }
      }

      arrangements.push(best);
      for (const team of best)
        for (let i = 0; i < team.length; i++)
          for (let j = i + 1; j < team.length; j++)
            history.add([team[i], team[j]].sort().join('|'));
    }

    const pairCounts = {};
    arrangements.forEach(arr => arr.forEach(team => {
      for (let i = 0; i < team.length; i++)
        for (let j = i + 1; j < team.length; j++) {
          const k = [team[i], team[j]].sort().join('|');
          pairCounts[k] = (pairCounts[k] || 0) + 1;
        }
    }));
    const dupPairCount = Object.values(pairCounts).filter(v => v > 1).length;
    return { error: null, arrangements, dupStats: { dupPairCount, isPerfect: dupPairCount === 0 } };
  }
}

// ==========================================
// SECTION 3: DOWNLOAD UTILITIES
// ==========================================
function downloadCSV(arrangements, filename) {
  let maxSz = 0;
  arrangements.forEach(r => r.forEach(g => { maxSz = Math.max(maxSz, g.length); }));
  const headers = ['라운드', '조', ...Array.from({ length: maxSz }, (_, i) => `멤버${i + 1}`)];
  const rows = [headers];
  arrangements.forEach((arr, rIdx) => arr.forEach((g, gIdx) => {
    rows.push([`${rIdx + 1}라운드`, `${gIdx + 1}조`, ...Array.from({ length: maxSz }, (_, i) => g[i] || '')]);
  }));
  const blob = new Blob(['\uFEFF' + rows.map(r => r.map(c => `"${c}"`).join(',')).join('\r\n')], { type: 'text/csv;charset=utf-8;' });
  const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(blob), download: `${filename}.csv` });
  a.click(); URL.revokeObjectURL(a.href);
}

async function downloadAllImages(arrangements, filename) {
  const W = 520, LH = 52, HH = 80, PAD = 32, MAX_TW = W - 108;
  for (let rIdx = 0; rIdx < arrangements.length; rIdx++) {
    const arr = arrangements[rIdx];
    const canvas = document.createElement('canvas');
    canvas.width = W; canvas.height = HH + arr.length * LH + PAD;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#faf9f7'; ctx.fillRect(0, 0, W, canvas.height);
    ctx.fillStyle = '#a07d6c'; ctx.fillRect(0, 0, W, 10);
    ctx.fillStyle = '#4a423d'; ctx.font = 'bold 22px sans-serif'; ctx.textAlign = 'left';
    ctx.fillText(`🎯 ${rIdx + 1}라운드 매칭 결과`, 24, 50);
    ctx.strokeStyle = '#e6e1db'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(24, 68); ctx.lineTo(W - 24, 68); ctx.stroke();

    arr.forEach((group, gIdx) => {
      const bY = HH + gIdx * LH + 8, tY = HH + gIdx * LH + LH * 0.68;
      ctx.fillStyle = '#f7ede7';
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(24, bY, 48, 28, 14); else ctx.rect(24, bY, 48, 28);
      ctx.fill();
      ctx.fillStyle = '#a07d6c'; ctx.font = 'bold 13px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(`${gIdx + 1}조`, 48, tY);

      const text = group.length <= 3 ? group.join(' ↔ ') : group.join(' · ');
      let fs = 15; ctx.font = `${fs}px sans-serif`;
      while (ctx.measureText(text).width > MAX_TW && fs > 9) { fs--; ctx.font = `${fs}px sans-serif`; }
      ctx.fillStyle = '#3f3a36'; ctx.textAlign = 'left';
      ctx.fillText(text, 84, tY);
    });

    await new Promise(r => canvas.toBlob(blob => {
      const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(blob), download: `${filename}_${rIdx + 1}라운드.png` });
      a.click(); URL.revokeObjectURL(a.href); setTimeout(r, 400);
    }, 'image/png'));
  }
}

// ==========================================
// SECTION 4: SUB COMPONENTS
// ==========================================

// ── A. 짝교제(1:1) View ──
function CoupleMatchingView({ names, setNames }) {
  const [targetCount, setTargetCount] = useState('');
  const [allowTrio, setAllowTrio] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [round, setRound] = useState(0);
  const [loading, setLoading] = useState(false);

  const run = () => {
    setError(''); setResult(null);
    const list = names.split('\n').map(s => s.trim()).filter(Boolean);
    if (list.length < 2) { setError('최소 2명 이상 입력해 주세요.'); return; }
    const cnt = parseInt(targetCount, 10);
    if (!cnt || cnt < 1) { setError('횟수를 1 이상 입력해 주세요.'); return; }
    setLoading(true);
    setTimeout(() => {
      const { error: e, arrangements, fairnessStats } = new OptimizedPairMakerJS().generateMultipleArrangements(list, cnt, allowTrio);
      setLoading(false);
      if (e) { setError(e); return; }
      setResult({ arrangements, fairnessStats, odd: list.length % 2 !== 0 }); setRound(0);
    }, 50);
  };

  const copy = () => {
    if (!result) return;
    const g = result.arrangements[round];
    let t = `🎯 짝교제 ${round + 1}차 결과\n${'='.repeat(24)}\n`;
    g.forEach((gr, i) => { t += `${i + 1}조: ${gr.join(' ↔ ')}${gr.length === 3 ? ' (3명조)' : ''}\n`; });
    t += '\n💡 중복 없음!';
    navigator.clipboard.writeText(t).then(() => alert('복사했습니다!'));
  };

  const nc = names.split('\n').filter(s => s.trim()).length;
  return (
    <div className="pm-layout">
      <div className="pm-card pm-input-card">
        <div className="pm-step"><span className="pm-step-num">1</span><label>참가자 명단 입력</label></div>
        <div className="pm-textarea-wrap">
          <textarea className="pm-textarea" value={names} onChange={e => setNames(e.target.value)} placeholder="한 줄에 한 명씩 입력하세요" />
          {nc > 0 && <span className="pm-count-badge">{nc}명</span>}
        </div>
        <div className="pm-step"><span className="pm-step-num">2</span><label>총 섞을 횟수</label></div>
        <input className="pm-num-input" type="number" min="1" value={targetCount} onChange={e => setTargetCount(e.target.value)} placeholder="횟수를 입력하세요" />
        <div className="pm-toggle-card">
          <div className="pm-toggle-header">
            <label className="pm-switch"><input type="checkbox" checked={allowTrio} onChange={e => setAllowTrio(e.target.checked)} /><span className="pm-switch-track"></span></label>
            <strong>3명조 중복 허용 모드</strong>
          </div>
        </div>
        {error && <div className="pm-error">{error}</div>}
        <button className="pm-btn-generate" onClick={run} disabled={loading}>{loading ? '🔄 계산 중...' : '🎲 매칭 시작하기'}</button>
      </div>

      <div className="pm-card pm-result-card">
        <h2 className="pm-result-title">✨ 매칭 결과</h2>
        {!result ? (
          <div className="pm-empty"><div className="pm-empty-icon">🌱</div><p>매칭을 시작해 주세요</p></div>
        ) : (
          <>
            {result.fairnessStats && result.odd && (
              <div className={`pm-fairness ${result.fairnessStats.isFair ? 'fair' : 'unfair'}`}>
                <span>{result.fairnessStats.isFair ? '✅' : '⚠️'}</span>
                <div className="pm-fairness-text">
                  <strong>3명조 공정성</strong>
                  <span className="pm-fairness-range">최소 {result.fairnessStats.min}회 ~ 최대 {result.fairnessStats.max}회</span>
                </div>
              </div>
            )}
            <div className="pm-dl-row">
              <button className="pm-dl-btn csv" onClick={() => downloadCSV(result.arrangements, '짝교제_전체결과')}>📊 엑셀 저장</button>
              <button className="pm-dl-btn img" onClick={() => downloadAllImages(result.arrangements, '짝교제')}>🖼️ 이미지 저장</button>
            </div>
            <div className="pm-tabs-wrap"><div className="pm-tabs">
              {result.arrangements.map((_, i) => (
                <button key={i} className={`pm-tab ${round === i ? 'active' : ''}`} onClick={() => setRound(i)}>{i + 1}차</button>
              ))}
            </div></div>
            <div className="pm-pairs">
              {result.arrangements[round].map((g, i) => (
                <div key={i} className={`pm-pair ${g.length === 3 ? 'trio' : ''}`}>
                  <span className="pm-pair-num">{i + 1}조</span>
                  <span className="pm-pair-names">{g.join(' ↔ ')}</span>
                </div>
              ))}
            </div>
            <button className="pm-btn-copy" onClick={copy}>📋 {round + 1}차 결과 복사</button>
          </>
        )}
      </div>
    </div>
  );
}

// ── B. 단체 팀 매칭 View ──
function TeamMatchingView({ names, setNames, teamLeaders, setTeamLeaders, isLeaderMode, setIsLeaderMode }) {
  const [teamCount, setTeamCount] = useState('');
  const [targetCount, setTargetCount] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [round, setRound] = useState(0);
  const [loading, setLoading] = useState(false);

  const run = () => {
    setError(''); setResult(null);
    const list = names.split('\n').map(s => s.trim()).filter(Boolean);
    const lList = isLeaderMode ? teamLeaders.split('\n').map(s => s.trim()).filter(Boolean) : [];
    
    if (isLeaderMode && lList.length < 2) { setError('조장을 2명 이상 입력해 주세요.'); return; }
    if (!isLeaderMode && list.length < 2) { setError('최소 2명 이상 입력해 주세요.'); return; }
    
    if (isLeaderMode && lList.length > 0 && list.length > 0) {
      const overlaps = list.filter(n => lList.includes(n));
      if (overlaps.length > 0) {
        if (!window.confirm("⚠️ 조장 명단과 일반 참가자 명단에 동일한 이름이 있습니다. 동명이인 입니까?\n\n[확인]을 누르면 이대로 조편성을 진행합니다.")) return;
      }
    }

    const teams = isLeaderMode ? lList.length : parseInt(teamCount, 10);
    if (!teams || teams < 2) { setError('팀 수는 2 이상이어야 합니다.'); return; }
    if (!isLeaderMode && teams > list.length) { setError(`팀 수(${teams})가 인원수(${list.length})보다 많을 수 없습니다.`); return; }

    const rounds = parseInt(targetCount, 10);
    if (!rounds || rounds < 1) { setError('횟수를 1 이상 입력해 주세요.'); return; }
    setLoading(true);
    setTimeout(() => {
      const { error: e, arrangements, dupStats } = new OptimizedTeamMakerJS().generateArrangements(list, teams, rounds, lList);
      setLoading(false);
      if (e) { setError(e); return; }
      setResult({ arrangements, dupStats }); setRound(0);
    }, 100);
  };

  const copy = () => {
    if (!result) return;
    let t = `🎯 팀 매칭 ${round + 1}차 결과\n${'='.repeat(24)}\n`;
    result.arrangements[round].forEach((team, i) => { t += `${i + 1}팀: ${team.join(', ')}\n`; });
    navigator.clipboard.writeText(t).then(() => alert('복사했습니다!'));
  };

  const nc = names.split('\n').filter(s => s.trim()).length;
  const lc = isLeaderMode ? teamLeaders.split('\n').filter(s => s.trim()).length : 0;
  return (
    <div className="pm-layout">
      <div className="pm-card pm-input-card">
        <div className="pm-toggle-card" style={{ marginBottom: '1.2rem' }}>
          <div className="pm-toggle-header">
            <label className="pm-switch"><input type="checkbox" checked={isLeaderMode} onChange={e => setIsLeaderMode(e.target.checked)} /><span className="pm-switch-track"></span></label>
            <strong>조장 지정 모드</strong>
          </div>
        </div>

        {isLeaderMode && (
          <>
            <div className="pm-step"><span className="pm-step-num">👑</span><label>조장 명단 입력</label></div>
            <div className="pm-textarea-wrap" style={{ marginBottom: '1rem' }}>
              <textarea className="pm-textarea" value={teamLeaders} onChange={e => setTeamLeaders(e.target.value)} placeholder="조장 이름을 한 줄에 한 명씩 입력하세요" style={{ height: '90px' }} />
              {lc > 0 && <span className="pm-count-badge">{lc}명 (팀 수 동일)</span>}
            </div>
          </>
        )}

        <div className="pm-step"><span className="pm-step-num">1</span><label>{isLeaderMode ? '일반 참가자 입력' : '참가자 명단 입력'}</label></div>
        <div className="pm-textarea-wrap">
          <textarea className="pm-textarea" value={names} onChange={e => setNames(e.target.value)} placeholder="한 줄에 한 명씩 입력하세요" style={{ height: isLeaderMode ? '140px' : '200px' }} />
          {nc > 0 && <span className="pm-count-badge">{nc}명</span>}
        </div>

        <div className="pm-step"><span className="pm-step-num">2</span><label>나눌 팀 수</label></div>
        {isLeaderMode ? (
          <input className="pm-num-input" type="text" value={lc > 0 ? `${lc}팀 (조장 수대로 자동 지정)` : '조장 수에 따라 자동 지정'} disabled style={{ background: 'var(--pm-bg)', color: 'var(--pm-text-muted)' }} />
        ) : (
          <input className="pm-num-input" type="number" min="2" value={teamCount} onChange={e => setTeamCount(e.target.value)} placeholder="몇 팀으로 나눌지 입력하세요" />
        )}
        <div className="pm-step"><span className="pm-step-num">3</span><label>총 섞을 횟수</label></div>
        <input className="pm-num-input" type="number" min="1" value={targetCount} onChange={e => setTargetCount(e.target.value)} placeholder="횟수를 입력하세요" />
        {error && <div className="pm-error">{error}</div>}
        <button className="pm-btn-generate" onClick={run} disabled={loading}>{loading ? '🔄 계산 중...' : '🎲 팀 배정 시작하기'}</button>
      </div>

      <div className="pm-card pm-result-card">
        <h2 className="pm-result-title">✨ 팀 배정 결과</h2>
        {!result ? (
          <div className="pm-empty"><div className="pm-empty-icon">🌱</div><p>팀 배정을 시작해 주세요</p></div>
        ) : (
          <>
            {result.dupStats && (
              <div className={`pm-fairness ${result.dupStats.isPerfect ? 'fair' : 'unfair'}`}>
                <span>{result.dupStats.isPerfect ? '✅' : '⚠️'}</span>
                <div className="pm-fairness-text">
                  <strong>중복 만남 현황</strong>
                  <span className="pm-fairness-range">
                    {result.dupStats.isPerfect ? '전 라운드 중복 없음!' : `중복된 조합 ${result.dupStats.dupPairCount}쌍 (최소화 완료)`}
                  </span>
                </div>
              </div>
            )}
            <div className="pm-dl-row">
              <button className="pm-dl-btn csv" onClick={() => downloadCSV(result.arrangements, '팀매칭_전체결과')}>📊 엑셀 저장</button>
              <button className="pm-dl-btn img" onClick={() => downloadAllImages(result.arrangements, '팀매칭')}>🖼️ 이미지 저장</button>
            </div>
            <div className="pm-tabs-wrap"><div className="pm-tabs">
              {result.arrangements.map((_, i) => (
                <button key={i} className={`pm-tab ${round === i ? 'active' : ''}`} onClick={() => setRound(i)}>{i + 1}차</button>
              ))}
            </div></div>
            <div className="pm-team-list">
              {result.arrangements[round].map((team, i) => (
                <div key={i} className="pm-team-row">
                  <span className="pm-team-num">{i + 1}팀</span>
                  <div className="pm-team-members">
                    {team.map((m, j) => <span key={j} className="pm-member-chip">{m}</span>)}
                  </div>
                </div>
              ))}
            </div>
            <button className="pm-btn-copy" onClick={copy}>📋 {round + 1}차 결과 복사</button>
          </>
        )}
      </div>
    </div>
  );
}

// ==========================================
// SECTION 5: MAIN APP CONTAINER
// ==========================================
export default function PairMaker() {
  const [tab, setTab] = useState('couple');
  const [names, setNames] = useState('');
  const [teamLeaders, setTeamLeaders] = useState('');
  const [isLeaderMode, setIsLeaderMode] = useState(false);

  useEffect(() => {
    if (!document.getElementById('pm-styles')) {
      const s = document.createElement('style');
      s.id = 'pm-styles';
      s.textContent = STYLES;
      document.head.appendChild(s);
    }
  }, []);

  return (
    <div className="pm-wrap">
      <header className="pm-header">
        <div className="pm-header-icon">🎲</div>
        <h1>그룹교제 조편성</h1>
        <p>중복 없이, 공정하게, 자동으로 섞어드립니다</p>
      </header>

      <nav className="pm-main-nav">
        <button className={`pm-main-tab ${tab === 'couple' ? 'active' : ''}`} onClick={() => setTab('couple')}>
          🎲 1:1 짝교제 조편성
        </button>
        <button className={`pm-main-tab ${tab === 'team' ? 'active' : ''}`} onClick={() => setTab('team')}>
          👥 단체 그룹 조편성
        </button>
      </nav>

      {tab === 'couple'
        ? <CoupleMatchingView names={names} setNames={setNames} />
        : <TeamMatchingView names={names} setNames={setNames} teamLeaders={teamLeaders} setTeamLeaders={setTeamLeaders} isLeaderMode={isLeaderMode} setIsLeaderMode={setIsLeaderMode} />}
    </div>
  );
}
