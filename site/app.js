/* =========================================================================
   Psychohistory — interactive site logic (vanilla JS + Plotly)
   Sections: sim primitives -> hero/canon -> demos A/B/C -> coverage
             -> classifier -> wiring.  No framework. No build step.
   ========================================================================= */

'use strict';

const DATA = window.PSYCHO_DATA;

/* Foundation palette (kept in sync with styles.css) */
const C = {
  bg:    '#070b14', panel: '#0c1322', grid: '#1c2a44',
  ink:   '#d7e0ef', dim: '#93a3bf', faint: '#65748f',
  gold:  '#e8b24a', cyan: '#48c9d6', green: '#6fcf86',
  amber: '#e8a14a', red: '#e86a5a', violet: '#b08be0'
};

/* shared Plotly layout defaults for the dark theme */
function baseLayout(extra) {
  return Object.assign({
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor:  'rgba(0,0,0,0)',
    font: { family: 'Inter, system-ui, sans-serif', color: C.dim, size: 12 },
    margin: { l: 52, r: 18, t: 18, b: 44 },
    xaxis: { gridcolor: C.grid, zerolinecolor: C.grid, linecolor: C.grid },
    yaxis: { gridcolor: C.grid, zerolinecolor: C.grid, linecolor: C.grid },
    showlegend: false
  }, extra || {});
}
const PLOT_CFG = { displayModeBar: false, responsive: true };
const hasPlotly = typeof Plotly !== 'undefined';

/* =========================================================================
   1. VERIFIED SIM PRIMITIVES  (ported faithfully from the Python engine)
   ========================================================================= */

/* Deterministic PRNG so sims are reproducible across runs. */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}

/* Box–Muller Gaussian draws, caching the second value. */
function makeGauss(rng){let s=null;return function(){if(s!==null){const v=s;s=null;return v;}let u,v,r;do{u=2*rng()-1;v=2*rng()-1;r=u*u+v*v;}while(r>=1||r===0);const f=Math.sqrt(-2*Math.log(r)/r);s=v*f;return u*f;};}

/* K coupled bistable blocks integrated by Euler–Maruyama.
   dx_i = (theta*x_i - x_i^3 + W*(mean - x_i)) dt + sigma dW.
   Returns final state x and the post-burn snapshots `win`. */
function runBlocks(K,W,{theta=1,sigma=0.5,T=1300,dt=0.01,seed=2,burn=700,x0=null}={}){
  const rng=mulberry32(seed),g=makeGauss(rng),sdt=Math.sqrt(dt);
  let x=new Float64Array(K); if(x0){x.set(x0);} else {for(let i=0;i<K;i++)x[i]=0.1*g();}
  const win=[];
  for(let t=0;t<T;t++){let m=0;for(let i=0;i<K;i++)m+=x[i];m/=K;
    const xn=new Float64Array(K);
    for(let i=0;i<K;i++){const xi=x[i];xn[i]=xi+dt*(theta*xi-xi*xi*xi+W*(m-xi))+sdt*sigma*g();}
    x=xn; if(t>=burn) win.push(x);}
  return {x,win};
}

/* Synchrony S, the CORRECT N_eff (macro variance-ratio), and the MISLEADING
   Pearson N_eff — computed from the snapshot window. */
function blockMetrics(win,K){
  const Tw=win.length;
  // S = mean_t | mean_i sign(x_i) |  (correct synchrony order parameter)
  let Ssum=0; const csm=new Float64Array(Tw);
  for(let t=0;t<Tw;t++){let ms=0;for(let i=0;i<K;i++)ms+=Math.sign(win[t][i]);ms/=K;csm[t]=ms;Ssum+=Math.abs(ms);}
  const S=Ssum/Tw;
  // N_eff correct = mean Var_t(single-block sign) / Var_t(pop-mean sign), clipped [1,K]
  let varSingle=0; for(let i=0;i<K;i++){let s=0,ss=0;for(let t=0;t<Tw;t++){const sg=Math.sign(win[t][i]);s+=sg;ss+=1;}const m=s/Tw;varSingle+=(ss/Tw-m*m);} varSingle/=K;
  let cm=0,cs=0; for(let t=0;t<Tw;t++){cm+=csm[t];cs+=csm[t]*csm[t];} cm/=Tw; const varMean=cs/Tw-cm*cm;
  let neffCorrect = varMean>1e-9 ? varSingle/varMean : 1; neffCorrect=Math.max(1,Math.min(K,neffCorrect));
  // N_eff Pearson (MISLEADING): standardized-sum trick on raw x
  const mean=new Float64Array(K),sd=new Float64Array(K);
  for(let i=0;i<K;i++){let s=0;for(let t=0;t<Tw;t++)s+=win[t][i];mean[i]=s/Tw;}
  for(let i=0;i<K;i++){let s=0;for(let t=0;t<Tw;t++){const d=win[t][i]-mean[i];s+=d*d;}sd[i]=Math.sqrt(s/Tw);}
  let ez=0; for(let t=0;t<Tw;t++){let Z=0;for(let i=0;i<K;i++){if(sd[i]>1e-9)Z+=(win[t][i]-mean[i])/sd[i];}ez+=Z*Z;} ez/=Tw;
  let rbar=(ez-K)/(K*(K-1)); if(rbar<0)rbar=0; const neffPearson=K/(1+(K-1)*rbar);
  return {S,neffCorrect,neffPearson,rbar};
}

/* MFG reaction cartoon: run-probability T(f) given expected run-fraction f.
   a = imitation gain, c = baseline propensity, d = guarantee weight, e = bias. */
function reaction(f,g=0,a=8,c=1.6,d=6,e=3){return 1/(1+Math.exp(-(a*f+c-d*g-e)));}

/* Fixed points of T(f)-f on [0,1] by sign-change scan. */
function fixedPoints(g,c=1.6,a=8,d=6,e=3){const out=[];let pf=reaction(0,g,a,c,d,e)-0;for(let k=1;k<=400;k++){const f=k/400;const v=reaction(f,g,a,c,d,e)-f;if(Math.sign(v)!==Math.sign(pf)&&pf!==0){out.push(f);}pf=v;}return out;}

/* Classify fixed points as stable / unstable from slope of T at f. */
function fpStability(f,g,c){
  const h=1e-3, t1=reaction(f-h,g,8,c,6,3), t2=reaction(f+h,g,8,c,6,3);
  const slope=(t2-t1)/(2*h);
  return slope<1 ? 'stable' : 'unstable';
}

/* =========================================================================
   2. HERO + CANON (from PSYCHO_DATA + the framework table)
   ========================================================================= */

function fillHero(){
  const cov=DATA.coverage;
  const pct=Math.round(100*cov.modelable/cov.total);
  const nLayers=Object.keys(cov.layers).length;
  document.getElementById('headlineStat').innerHTML =
    `<b>${cov.modelable}/${cov.total}</b> of r/AskEconomics top posts route to the framework.`;
  const chips=[
    {num: pct+'%', lbl: 'modelable coverage'},
    {num: cov.structural, lbl: 'fully-structural readings'},
    {num: nLayers, lbl: 'active layers (L0–L6)'}
  ];
  document.getElementById('heroChips').innerHTML = chips.map(ch=>
    `<div class="statchip"><div class="num">${ch.num}</div><div class="lbl">${ch.lbl}</div></div>`).join('');
}

const CANON_ROWS = [
  ['Psychohistory', 'Statistical mechanics of populations / mean-field theory', 'whole engine'],
  ['Axiom 1 — "sufficiently large for valid statistical treatment"', 'Law of large numbers — but over <b>blocks</b>, so N_eff ≈ K', 'R3 · L3'],
  ['Axiom 2 — "unaware… so reactions be truly random"', 'Reflexivity / Lucas critique — randomness = independence the LLN needs', 'R2 · L4'],
  ['Seldon Plan', 'Mean-field equilibrium trajectory ρ* (publishable forecast = MFG fixed point)', 'R2 · L4 · L7'],
  ['Seldon Crises', 'Bifurcations / critical transitions (forced choice points where ξ, χ diverge)', 'L5'],
  ['The Mule', 'OOD agent / model misspecification (zero-prior-mass type; more data does not help)', 'L5'],
  ['Second Foundation', 'Controller — closed-loop corrector (Kalman / optimal control), not a forecasting agency', 'control mode'],
  ['Gaia / Galaxia', 'Total-observability, fully-coupled limit — N_eff → 1 by design; zero sim-to-real gap', 'trilemma · L5'],
  ['Prime Radiant', 'The live system of governing equations + phase-portrait dashboard of the state Ξ', 'engine · L7'],
  ['Seldon trial (publish existence, hide contents)', 'Information release as a control input; publish only the fixed-point components', 'R2 · control']
];

function fillCanon(){
  document.getElementById('canonBody').innerHTML = CANON_ROWS.map(r=>
    `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td></tr>`).join('');
}

/* =========================================================================
   3. DEMO A — attention conservation + belief drift
   ========================================================================= */

const A_N = 12, A_TARGET = 6; // topic #7 is index 6
let aState = null, aStep = 0, aTimer = null, aDrift = 0.5;

function aInit(){
  // uniform probability vector
  aState = new Float64Array(A_N).fill(1 / A_N);
  aStep = 0;
}

/* One step of the graph master equation. Each topic exchanges mass with its
   ring neighbours (conservative Laplacian, rows sum to zero) plus a belief
   drift that biases flow toward the target topic. Total mass is invariant. */
function aStepOnce(){
  const p = aState, n = A_N, t = A_TARGET, drift = aDrift;
  const flow = new Float64Array(n);
  const diff = 0.04;            // symmetric diffusion to neighbours
  for (let i = 0; i < n; i++) {
    const L = (i - 1 + n) % n, R = (i + 1) % n;
    flow[i] += diff * (p[L] - p[i]) + diff * (p[R] - p[i]);
  }
  // belief drift: pull a fraction of every non-target topic's mass toward target
  for (let i = 0; i < n; i++) {
    if (i === t) continue;
    const move = drift * 0.05 * p[i];   // proportional, so it can never go negative
    flow[i] -= move;
    flow[t] += move;
  }
  for (let i = 0; i < n; i++) p[i] += flow[i];
  // renormalize defensively against float drift (keeps total at exactly 1)
  let s = 0; for (let i = 0; i < n; i++) s += p[i];
  for (let i = 0; i < n; i++) p[i] /= s;
  aStep++;
}

function aRender(){
  const p = Array.from(aState);
  let total = p.reduce((a,b)=>a+b,0);
  let hhi = p.reduce((a,b)=>a+b*b,0);
  const colors = p.map((_,i)=> i===A_TARGET ? C.cyan : C.gold);
  if (hasPlotly) {
    Plotly.react('chartA', [{
      type:'bar',
      x: p.map((_,i)=>'T'+(i+1)),
      y: p,
      marker:{ color: colors, line:{ width:0 } }
    }], baseLayout({
      yaxis:{ range:[0,1], gridcolor:C.grid, title:{ text:'attention share', font:{size:11} } },
      xaxis:{ gridcolor:'rgba(0,0,0,0)' }
    }), PLOT_CFG);
  }
  document.getElementById('aTotal').textContent = total.toFixed(6);
  document.getElementById('aPeak').textContent  = p[A_TARGET].toFixed(3);
  document.getElementById('aHHI').textContent   = hhi.toFixed(3);
  document.getElementById('aStep').textContent  = aStep;
  const v = document.getElementById('aVerdict');
  if (p[A_TARGET] > 0.4) {
    v.className = 'verdict good';
    v.innerHTML = `<b>Conserved &amp; concentrated.</b> Topic #7 now holds ${(p[A_TARGET]*100).toFixed(0)}% of attention — drawn entirely from the others. The total never moved off 1.000000.`;
  } else {
    v.className = 'verdict good';
    v.innerHTML = `<b>Conserved.</b> Attention is reallocated, never created — the total is invariant to the drift.`;
  }
}

function aRun(){
  if (aTimer) return;
  let n = 0;
  function tick(){
    aStepOnce(); aRender();
    if (++n < 200) { aTimer = requestAnimationFrame(tick); }
    else { aTimer = null; }
  }
  aTimer = requestAnimationFrame(tick);
}
function aResetFn(){
  if (aTimer) { cancelAnimationFrame(aTimer); aTimer = null; }
  aInit(); aRender();
}

function wireDemoA(){
  aInit(); aRender();
  const drift = document.getElementById('aDrift');
  drift.addEventListener('input', ()=>{
    aDrift = parseFloat(drift.value);
    document.getElementById('aDriftVal').textContent = aDrift.toFixed(2);
  });
  document.getElementById('aRun').addEventListener('click', aRun);
  document.getElementById('aReset').addEventListener('click', aResetFn);
}

/* =========================================================================
   4. DEMO B — criticality (the star)
   ========================================================================= */

const B_K = 48;
const B_WSWEEP = [];           // 26 W-values, precomputed once
let bSweep = null;             // {W:[], S:[], Nc:[], Np:[]}
let bRAF = null;

/* Precompute the sweep over 26 coupling values (cached). */
function bComputeSweep(){
  const Ws = [], S = [], Nc = [], Np = [];
  for (let k = 0; k < 26; k++) {
    const W = (2.5 * k) / 25;
    Ws.push(W);
    const tr = runBlocks(B_K, W, { T: 1100, burn: 600, seed: 2 });
    const m = blockMetrics(tr.win, B_K);
    S.push(m.S); Nc.push(m.neffCorrect); Np.push(m.neffPearson);
  }
  bSweep = { W: Ws, S, Nc, Np };
}

/* Cheap skill-horizon proxy: 6 ensembles with tiny IC perturbations; find the
   model-time where ensemble std of the population mean first exceeds 0.8x the
   climatological std. */
function bSkillHorizon(W){
  const seeds = [2,3,4,5,6,7], ens = [], K = B_K, T = 900;
  // base IC from a short run, then perturb
  const base = runBlocks(K, W, { T: 200, burn: 199, seed: 2 }).x;
  const series = [];
  for (const sd of seeds) {
    const rng = mulberry32(sd*97+1), g = makeGauss(rng);
    const x0 = new Float64Array(K);
    for (let i=0;i<K;i++) x0[i] = base[i] + 0.01*g();
    const tr = runBlocks(K, W, { T, burn: 0, seed: sd, x0 });
    // population-mean time series
    const pm = new Float64Array(T);
    for (let t=0;t<T;t++){ let m=0; for(let i=0;i<K;i++) m+=tr.win[t][i]; pm[t]=m/K; }
    series.push(pm);
  }
  // climatological std = std of pop-mean over the tail of seed-2 run
  let cm=0; const tail=series[0]; for(let t=400;t<T;t++) cm+=tail[t]; cm/=(T-400);
  let cv=0; for(let t=400;t<T;t++){const d=tail[t]-cm; cv+=d*d;} cv/=(T-400);
  const climStd = Math.max(0.05, Math.sqrt(cv));
  const thr = 0.8*climStd;
  for (let t=0;t<T;t++){
    let m=0; for(const s of series) m+=s[t]; m/=series.length;
    let v=0; for(const s of series){const d=s[t]-m; v+=d*d;} v=Math.sqrt(v/series.length);
    if (v > thr) return (t*0.01); // dt=0.01 model-time
  }
  return null; // never -> >= max
}

function bSweepChart(curW){
  if (!hasPlotly) return;
  const traces = [
    { x: bSweep.W, y: bSweep.S,  mode:'lines+markers', name:'synchrony S',
      line:{color:C.gold,width:2.5}, marker:{size:4,color:C.gold} },
    { x: bSweep.W, y: bSweep.Nc.map(v=>v/B_K), mode:'lines+markers', name:'N_eff correct (÷K)',
      line:{color:C.cyan,width:2.5}, marker:{size:4,color:C.cyan} },
    { x: bSweep.W, y: bSweep.Np.map(v=>v/B_K), mode:'lines+markers', name:'N_eff Pearson (÷K)',
      line:{color:C.red,width:2,dash:'dot'}, marker:{size:4,color:C.red} }
  ];
  const lay = baseLayout({
    showlegend:true,
    legend:{ orientation:'h', y:1.16, x:0, font:{size:10}, bgcolor:'rgba(0,0,0,0)' },
    margin:{ l:48, r:16, t:42, b:42 },
    xaxis:{ title:{text:'coupling W',font:{size:11}}, gridcolor:C.grid, range:[0,2.5] },
    yaxis:{ title:{text:'value (N_eff normalized by K)',font:{size:11}}, gridcolor:C.grid, range:[0,1.05] },
    shapes:[{ type:'line', x0:curW, x1:curW, y0:0, y1:1.05, line:{color:C.green,width:1.5,dash:'dash'} }],
    annotations:[{ x:curW, y:1.05, text:'W', showarrow:false, font:{color:C.green,size:11}, yanchor:'bottom' }]
  });
  Plotly.react('chartB', traces, lay, PLOT_CFG);
}

function bScatterChart(xvals){
  if (!hasPlotly) return;
  // strip scatter of the K final block values, jittered on y for visibility
  const rng = mulberry32(11);
  const ys = []; for (let i=0;i<xvals.length;i++) ys.push((rng()-0.5)*0.8);
  const cols = xvals.map(v=> v>=0 ? C.cyan : C.amber);
  Plotly.react('chartBscatter', [{
    x: Array.from(xvals), y: ys, mode:'markers', type:'scatter',
    marker:{ size:8, color:cols, opacity:0.8, line:{width:0} }
  }], baseLayout({
    margin:{ l:30, r:16, t:42, b:42 },
    xaxis:{ title:{text:'block state x  (sign = which basin)',font:{size:11}}, gridcolor:C.grid, range:[-2,2], zeroline:true, zerolinecolor:C.faint },
    yaxis:{ visible:false, range:[-1,1] },
    annotations:[{ x:0, y:0.95, xref:'x', yref:'paper', text:'48 blocks at current W', showarrow:false, font:{color:C.dim,size:10} }]
  }), PLOT_CFG);
}

function bVerdict(W, Nc){
  const el = document.getElementById('bVerdict');
  if (W < 0.4) {
    el.className = 'verdict good';
    el.innerHTML = `<b>Predictable.</b> Blocks are independent, the law of large numbers holds, N_eff ≈ K. Aggregate statistics average out — open-loop forecasting works.`;
  } else if (W < 1) {
    el.className = 'verdict warn';
    el.innerHTML = `<b>Pre-critical.</b> Synchrony is rising and N_eff is falling — the early-warning regime. Forecast the <em>transition</em>, not yet the branch.`;
  } else {
    el.className = 'verdict crit';
    el.innerHTML = `<b>Critical.</b> N_eff is collapsing toward 1 — the recovered LLN evaporates exactly when stakes are highest. Forecast the transition, not the branch: this is the control regime.`;
  }
}

let bLast = -1;
function bUpdateLive(W){
  // single live run at current W (kept under ~30ms with K=48, modest T)
  const tr = runBlocks(B_K, W, { T: 900, burn: 500, seed: 2 });
  const m = blockMetrics(tr.win, B_K);
  bSweepChart(W);
  bScatterChart(tr.x);
  document.getElementById('bS').textContent  = m.S.toFixed(3);
  document.getElementById('bNc').textContent = m.neffCorrect.toFixed(1);
  document.getElementById('bNp').textContent = m.neffPearson.toFixed(1);
  const tau = bSkillHorizon(W);
  document.getElementById('bTau').textContent = (tau===null) ? '≥ max' : tau.toFixed(1);
  bVerdict(W, m.neffCorrect);
}

function wireDemoB(){
  bComputeSweep();
  const W0 = parseFloat(document.getElementById('bW').value);
  bUpdateLive(W0);
  const slider = document.getElementById('bW');
  slider.addEventListener('input', ()=>{
    const W = parseFloat(slider.value);
    document.getElementById('bWval').textContent = W.toFixed(2);
    // debounce with requestAnimationFrame
    if (bRAF) cancelAnimationFrame(bRAF);
    bRAF = requestAnimationFrame(()=>{ bUpdateLive(W); bRAF = null; });
  });
}

/* =========================================================================
   5. DEMO C — reflexivity fixed points (bank run)
   ========================================================================= */

let cRAF = null;

function cUpdate(){
  const g = parseFloat(document.getElementById('cG').value);
  const c = parseFloat(document.getElementById('cC').value);
  document.getElementById('cGval').textContent = g.toFixed(2);
  document.getElementById('cCval').textContent = c.toFixed(2);

  const N = 201;
  const fs = [], Tf = [], diag = [];
  for (let k = 0; k < N; k++){ const f = k/(N-1); fs.push(f); Tf.push(reaction(f,g,8,c,6,3)); diag.push(f); }
  const fps = fixedPoints(g, c);
  const stable = [], unstable = [];
  for (const f of fps){ (fpStability(f,g,c)==='stable' ? stable : unstable).push(f); }

  if (hasPlotly){
    const traces = [
      { x: fs, y: diag, mode:'lines', line:{color:C.faint,width:1.5,dash:'dash'}, name:'y = f' },
      { x: fs, y: Tf,   mode:'lines', line:{color:C.gold,width:2.5}, name:'T(f)' }
    ];
    if (stable.length)
      traces.push({ x:stable, y:stable, mode:'markers', marker:{size:13,color:C.green,line:{color:'#0a1a10',width:2}}, name:'stable' });
    if (unstable.length)
      traces.push({ x:unstable, y:unstable, mode:'markers', marker:{size:13,color:C.red,symbol:'circle-open',line:{color:C.red,width:2.5}}, name:'unstable' });
    const anns = unstable.map(f=>({ x:f, y:f, text:'unstable threshold', showarrow:true, arrowcolor:C.red, ax:36, ay:-30, font:{color:C.red,size:10} }));
    Plotly.react('chartC', traces, baseLayout({
      showlegend:true,
      legend:{ orientation:'h', y:1.13, x:0, font:{size:10}, bgcolor:'rgba(0,0,0,0)' },
      margin:{ l:48, r:16, t:40, b:44 },
      xaxis:{ title:{text:'expected run-fraction  f',font:{size:11}}, range:[0,1], gridcolor:C.grid },
      yaxis:{ title:{text:'reaction  T(f)',font:{size:11}}, range:[0,1], gridcolor:C.grid },
      annotations: anns
    }), PLOT_CFG);
  }

  // equilibrium readout: the relevant attractor is the highest stable fp
  const eq = stable.length ? Math.max(...stable) : (Tf[Tf.length-1] > 0.5 ? 1 : 0);
  document.getElementById('cNfp').textContent = fps.length;
  document.getElementById('cEq').textContent  = eq.toFixed(3);
  const bistable = fps.length >= 3;
  document.getElementById('cRegime').textContent = bistable ? 'imitative' : 'monotone';

  const v = document.getElementById('cVerdict');
  if (bistable){
    v.className = 'verdict crit';
    v.innerHTML = `<b>Imitative regime — bistable.</b> Three fixed points (run / unstable threshold / no-run). The outcome depends on which basin the system starts in: forecasting fails, control takes over. A push past the threshold tips it either way.`;
  } else if (g > 0.55 && eq < 0.15){
    v.className = 'verdict good';
    v.innerHTML = `<b>Guarantee credible.</b> The deposit guarantee collapsed the fixed point to ≈ 0 — the run is killed. A single unique, publishable, self-consistent forecast: "no run."`;
  } else {
    v.className = 'verdict info';
    v.innerHTML = `<b>Monotone regime — unique fixed point.</b> One equilibrium run-probability (≈ ${eq.toFixed(2)}); the forecast is publishable because it reproduces itself. Raise the guarantee to drive it toward zero, or lower c to expose bistability.`;
  }
}

function wireDemoC(){
  ['cG','cC'].forEach(id=>{
    document.getElementById(id).addEventListener('input', ()=>{
      if (cRAF) cancelAnimationFrame(cRAF);
      cRAF = requestAnimationFrame(()=>{ cUpdate(); cRAF = null; });
    });
  });
  cUpdate();
}

/* =========================================================================
   6. COVERAGE DASHBOARD
   ========================================================================= */

const SCOPE_COLORS = {
  'MODELED': C.green, 'PARTIAL': C.cyan, 'NEEDS-DATA': C.gold,
  'NORMATIVE-AS-VALENCE': C.violet, 'TAUTOLOGY': C.faint
};
const LAYER_NAMES = {
  L0:'L0 valence', L1:'L1 slow stocks', L2:'L2 attention', L3:'L3 blocks',
  L4:'L4 reflexivity', L5:'L5 criticality', L6:'L6 observation'
};

function fillCoverageCharts(){
  const cov = DATA.coverage;
  // scope donut
  const sLabels = Object.keys(cov.scope), sVals = sLabels.map(k=>cov.scope[k]);
  if (hasPlotly){
    Plotly.react('chartScope', [{
      type:'pie', hole:0.58, labels:sLabels, values:sVals, sort:false,
      marker:{ colors: sLabels.map(k=>SCOPE_COLORS[k]||C.dim), line:{color:C.bg,width:2} },
      textinfo:'value', textfont:{color:C.bg,size:12,family:'JetBrains Mono'},
      hovertemplate:'%{label}: %{value}<extra></extra>'
    }], baseLayout({
      showlegend:true, legend:{ font:{size:10}, orientation:'v', x:1, y:0.5 },
      margin:{l:8,r:8,t:8,b:8}, height:300
    }), PLOT_CFG);

    // layer bar (horizontal, sorted desc)
    const lk = Object.keys(cov.layers).sort((a,b)=>cov.layers[a]-cov.layers[b]);
    Plotly.react('chartLayers', [{
      type:'bar', orientation:'h',
      y: lk.map(k=>LAYER_NAMES[k]||k), x: lk.map(k=>cov.layers[k]),
      marker:{ color: lk.map(k=> k==='L1'?C.gold : (k==='L5'?C.red : C.cyan)) },
      text: lk.map(k=>cov.layers[k]), textposition:'outside',
      textfont:{color:C.dim,size:11}
    }], baseLayout({
      margin:{l:110,r:30,t:8,b:30}, height:300,
      xaxis:{ gridcolor:C.grid, range:[0,Math.max(...Object.values(cov.layers))*1.15] },
      yaxis:{ gridcolor:'rgba(0,0,0,0)' }
    }), PLOT_CFG);
  }
}

/* ---- filterable readings table ---- */
let expandedRanks = new Set();

function layerChips(layers){
  return layers.map(l=>`<span class="lchip ${l}">${l}</span>`).join('');
}

function renderTable(){
  const fScope = document.getElementById('fScope').value;
  const fLayer = document.getElementById('fLayer').value;
  const q = document.getElementById('fSearch').value.trim().toLowerCase();
  const body = document.getElementById('readingsBody');
  let rows = DATA.readings.filter(r=>{
    if (fScope && r.scope_verdict !== fScope) return false;
    if (fLayer && !r.active_layers.includes(fLayer)) return false;
    if (q && !r.title.toLowerCase().includes(q)) return false;
    return true;
  });
  document.getElementById('filterCount').textContent = `${rows.length} / ${DATA.readings.length}`;

  body.innerHTML = rows.map(r=>{
    const open = expandedRanks.has(r.rank);
    const head = `<tr class="head-row" data-rank="${r.rank}">
        <td class="expander">${open?'▾':'▸'}</td>
        <td class="r-rank">${r.rank}</td>
        <td class="r-title"><a href="${r.url}" target="_blank" rel="noopener">${escapeHtml(r.title)}</a></td>
        <td>${layerChips(r.active_layers)}</td>
        <td><span class="scope ${r.scope_verdict}">${r.scope_verdict}</span></td>
        <td class="r-score">${r.score.toLocaleString()}</td>
      </tr>`;
    const detail = open ? `<tr class="detail-row"><td></td><td colspan="5"><div class="detail-box">
        <div class="lab">dominant mechanism</div><p class="mech">${escapeHtml(r.dominant_mechanism)}</p>
        <div class="lab">reading</div><p>${escapeHtml(r.reading)}</p>
        <div class="lab">skill horizon</div><p>${escapeHtml(r.skill_horizon)}</p>
        <div class="lab">key falsifier</div><p>${escapeHtml(r.key_falsifier)}</p>
      </div></td></tr>` : '';
    return head + detail;
  }).join('');

  // wire expand toggles
  body.querySelectorAll('.head-row').forEach(tr=>{
    tr.addEventListener('click', e=>{
      if (e.target.tagName === 'A') return; // let links work
      const rank = parseInt(tr.dataset.rank,10);
      if (expandedRanks.has(rank)) expandedRanks.delete(rank); else expandedRanks.add(rank);
      renderTable();
    });
  });
}

function fillFilters(){
  const fScope = document.getElementById('fScope');
  Object.keys(DATA.coverage.scope).forEach(k=>{
    const o=document.createElement('option'); o.value=k; o.textContent=k; fScope.appendChild(o);
  });
  const fLayer = document.getElementById('fLayer');
  Object.keys(DATA.coverage.layers).sort().forEach(k=>{
    const o=document.createElement('option'); o.value=k; o.textContent=(LAYER_NAMES[k]||k); fLayer.appendChild(o);
  });
  ['fScope','fLayer'].forEach(id=>document.getElementById(id).addEventListener('change', renderTable));
  document.getElementById('fSearch').addEventListener('input', renderTable);
}

function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

/* =========================================================================
   7. CLASSIFY YOUR OWN — keyword -> layer router (mirrors the SKILL cue table)
   ========================================================================= */

const CUES = [
  { layer:'L5', demo:'#demoB', words:['bank run','crash','collapse','recession','tipping','panic','runaway','cascade','meltdown','crisis','heading toward'] },
  { layer:'L4', demo:'#demoC', words:['expect','announce','self-fulfilling','forward guidance','credible','anchor','prophecy','signal','guidance','coordination'] },
  { layer:'L3', demo:'#demoB', words:['herd','contagion','bubble','everyone','spread','correlated','tribe','community','mania','harbinger'] },
  { layer:'L2', demo:'#demoA', words:['attention','viral','hype','concentration','inequality','winner-take-all','salience','rich get richer'] },
  { layer:'L0', demo:null,     words:['good','bad','should','fair','just','deserve','moral','ethical','ought'] },
  { layer:'L1', demo:null,     words:['afford','wage','wages','fiscal','gdp','cost','budget','deficit','revenue','debt','productivity','salary','salaries','income','price','rent','tax','taxes','interest rate'] },
  { layer:'L6', demo:null,     words:['how much','exactly','data','statistics','measure','number','figure','percent','rate of'] }
];
const LAYER_ORDER = ['L0','L1','L2','L3','L4','L5','L6'];
const LAYER_BLURB = {
  L0:'valence — resolved per block, not in the absolute',
  L1:'slow stocks — the quiet accounting core',
  L2:'attention transport — conserved carrier, belief = drift',
  L3:'blocks — N_eff over communities, not persons',
  L4:'reflexivity — self-fulfilling fixed points (MFG)',
  L5:'criticality — transitions with early-warning limits',
  L6:'observation/data — go fetch the number'
};

function classify(text){
  const t = ' ' + text.toLowerCase() + ' ';
  const hits = {};       // layer -> matched words
  for (const cue of CUES){
    for (const w of cue.words){
      if (t.includes(w)){ (hits[cue.layer] = hits[cue.layer]||[]).push(w); }
    }
  }
  // L1 is the universal substrate: nearly every economic question has a stock.
  if (Object.keys(hits).length === 0) hits['L1'] = ['(default stock layer)'];
  const layers = LAYER_ORDER.filter(l=>hits[l]);

  // scope verdict guess
  let scope;
  const set = new Set(layers);
  if (set.size === 1 && set.has('L1')) scope = 'PARTIAL';
  else if (set.has('L6') && set.size <= 2) scope = 'NEEDS-DATA';
  else if (set.has('L0') && set.size === 1) scope = 'NORMATIVE-AS-VALENCE';
  else if (set.has('L4') || set.has('L5')) scope = 'PARTIAL';
  else scope = 'PARTIAL';

  // which demo to try (priority L5 > L4 > L3 > L2)
  let demo = null, demoName = '';
  for (const cue of CUES){ if (cue.demo && set.has(cue.layer)){ demo = cue.demo; demoName = {L5:'Demo B · Criticality',L4:'Demo C · Reflexivity',L3:'Demo B · Criticality',L2:'Demo A · Attention'}[cue.layer]; break; } }

  // templated reading
  let reading;
  const dom = layers.find(l=>l!=='L1' && l!=='L6') || layers[0];
  if (set.size === 1 && set.has('L1')){
    reading = `This is a slow-stock question (L1) — demographics, debt, wages, fiscal capacity. The dramatic machinery (criticality, reflexivity) does not apply; it resolves as comparative statics over parameters, and most likely needs a number fetched. The honest verdict is the quiet core, not a forecast of a transition.`;
  } else {
    const names = layers.map(l=>l).join(', ');
    reading = `This routes onto ${names}. The dominant mechanism sits at ${dom} (${LAYER_BLURB[dom]}). ` +
      (set.has('L5') ? `Near a transition, switch the objective from predicting the branch to forecasting the transition — the skill horizon shrinks toward zero and control gains leverage. ` :
       set.has('L4') ? `Because the forecast is an input to the system, only fixed points of the reaction map are publishable; check whether the regime is monotone (unique) or imitative (bistable). ` :
       set.has('L2') ? `Treat attention as a conserved measure with belief as drift — concentration is reallocation, not creation. ` : '') +
      (set.has('L6') ? `At least one figure (L6) must be fetched and cited before the reading is complete.` : `It is structurally modelable with the active layers.`);
  }

  return { layers, scope, demo, demoName, reading, hits };
}

function renderClassify(text){
  const out = document.getElementById('classifyOut');
  if (!text.trim()){ out.classList.add('hidden'); return; }
  const r = classify(text);
  const demoLink = r.demo ? `<a class="suggest-link" href="${r.demo}">▸ try ${r.demoName}</a>` : `<span class="faint suggest-link">no live demo — slow-stock / data layer</span>`;
  out.innerHTML = `
    <div class="lab faint" style="font-family:var(--mono);font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-dim)">active layers</div>
    <div style="margin:6px 0 14px">${r.layers.map(l=>`<span class="lchip ${l}">${l} · ${LAYER_BLURB[l].split(' — ')[0]}</span>`).join(' ')}</div>
    <div style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-bottom:14px">
      <span class="scope ${r.scope}">${r.scope}</span>
      ${demoLink}
    </div>
    <div class="lab faint" style="font-family:var(--mono);font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-dim)">reading</div>
    <p style="margin-top:6px;color:var(--ink-dim)">${escapeHtml(r.reading)}</p>`;
  out.classList.remove('hidden');
}

function wireClassify(){
  document.getElementById('classifyBtn').addEventListener('click', ()=>{
    renderClassify(document.getElementById('classifyInput').value);
  });
  document.getElementById('classifyClear').addEventListener('click', ()=>{
    document.getElementById('classifyInput').value='';
    document.getElementById('classifyOut').classList.add('hidden');
  });
}

/* =========================================================================
   8. SCENARIO — AI & the future of plurality (World Cup vs Pluribus)
   Ports validation/scenarios/mythos_fable/model.py (attention capture ->
   N_eff collapse) + second_foundation (L_eff lineage diversity + OOD shock /
   Second Foundation). Self-contained init: scInit().
   ========================================================================= */

/* The verified Kish / N_eff identity, reused verbatim (same form as elsewhere). */
function nEff(N, rho){ rho = Math.max(0, Math.min(1, rho)); return N / (1 + (N - 1) * rho); }

const SC = {
  years: 10, dt: 1/12,
  Cf0: 1.0, tax: 0.30,           // alignment/safety deployment gap (frontier vs deployed)
  kappa0: 1.0,
  A0: 0.05, churn: 0.10, valScale: 6.0,
  rhoMax: 0.995, p: 1.6,         // homogenization: rho_human = rhoMax * A_ai^p
  tau0: 1.0,
  M: 50                          // deployed-model count (for L_eff = nEff(M, rho_model))
};
let scRAF = null, scShockOn = false;

/* First time y crosses thr (linear interp). null if never. */
function scCrossing(t, y, thr, rising){
  for (let i = 1; i < t.length; i++){
    const a = y[i-1], b = y[i];
    if (rising && a < thr && thr <= b){ const f = (b!==a)?(thr-a)/(b-a):0; return t[i-1]+f*(t[i]-t[i-1]); }
    if (!rising && a > thr && thr >= b){ const f = (a!==b)?(a-thr)/(a-b):0; return t[i-1]+f*(t[i]-t[i-1]); }
  }
  return null;
}

/* Run the deterministic monthly difference system (mythos_fable model.py). */
function scRun(P){
  const dt = SC.dt, n = Math.round(SC.years/dt) + 1;
  const t = new Float64Array(n), A = new Float64Array(n), rho = new Float64Array(n),
        Neff = new Float64Array(n), tau = new Float64Array(n);
  for (let i=0;i<n;i++) t[i] = i*dt;
  // model-lineage diversity floors how independent humans can be
  const Leff = nEff(SC.M, P.rhoModel);
  const cFloor = 0.85, rhoWithin = 0.10;
  const floor = Math.min(cFloor / Math.max(Leff, 1), 1);
  A[0] = SC.A0;
  const K = P.K;
  const v0overk0 = (SC.Cf0 * (1 - SC.tax)) / SC.kappa0;  // baseline value/cost
  function derive(i){
    // rho_human rises with attention capture A_ai, floored by lineage scarcity (1/L_eff)
    const rhoFromA = SC.rhoMax * Math.pow(A[i], SC.p);
    rho[i] = Math.max(0, Math.min(1, A[i] * (floor + (1 - floor) * rhoWithin) + rhoFromA * (1 - floor)));
    Neff[i] = nEff(K, rho[i]);
    tau[i] = SC.tau0 * (Neff[i] / K);          // skill horizon ~ N_eff/K
  }
  derive(0);
  for (let i=1;i<n;i++){
    // deployed capability and cost at previous step -> squashed value pull
    const Cf = SC.Cf0 * Math.exp(P.g * t[i-1]);
    const Cd = Cf * (1 - SC.tax);
    const kappa = SC.kappa0 * Math.exp(-P.delta * t[i-1]);
    const raw = Cd / kappa;
    const vnorm = raw / (raw + SC.valScale * v0overk0);          // in (0,1)
    const dA = P.alpha * vnorm * (1 - A[i-1]) - SC.churn * A[i-1];
    A[i] = Math.max(0, Math.min(1, A[i-1] + dt * dA));
    derive(i);
  }
  return { t, A, rho, Neff, tau, Leff };
}

function scReadParams(){
  const gx = parseFloat(document.getElementById('scG').value);   // x/yr
  const dx = parseFloat(document.getElementById('scD').value);   // x/yr
  return {
    g: Math.log(gx),
    delta: Math.log(dx),
    alpha: parseFloat(document.getElementById('scA').value),
    rhoModel: parseFloat(document.getElementById('scR').value),
    K: parseFloat(document.getElementById('scK').value),
    gx, dx
  };
}

function scPhase(endNeff){
  // same smooth-vs-critical boundary as Demo B: sub-critical N_eff high; super-critical -> 1
  const el = document.getElementById('scPhase');
  if (endNeff > 10){
    el.className = 'phase-banner worldcup';
    el.innerHTML = 'WORLD CUP <span class="phase-sub">sub-critical: many adversarial blocks survive — the law of large numbers holds, psychohistory is valid.</span>';
  } else if (endNeff > 2){
    el.className = 'phase-banner transition';
    el.innerHTML = 'TRANSITION <span class="phase-sub">near the phase boundary: N_eff falling fast, early-warning regime — forecast the transition, not the branch.</span>';
  } else {
    el.className = 'phase-banner pluribus';
    el.innerHTML = 'PLURIBUS / hive <span class="phase-sub">super-critical: N_eff → 1, the blocks act as one — the recovered LLN evaporates, psychohistory fails.</span>';
  }
}

function scChart(R){
  if (!hasPlotly) return;
  const t = Array.from(R.t);
  const traces = [
    { x: t, y: Array.from(R.A), mode:'lines', name:'A_ai (AI attention share)',
      line:{ color:C.red, width:2.5 }, yaxis:'y' },
    { x: t, y: Array.from(R.Neff), mode:'lines', name:'N_eff (human blocks)',
      line:{ color:C.cyan, width:2.5 }, yaxis:'y2' }
  ];
  const tc = scCrossing(t, Array.from(R.Neff), 10, false);
  const shapes = [];
  if (tc !== null) shapes.push({ type:'line', x0:tc, x1:tc, y0:0, y1:1, yref:'paper',
    line:{ color:C.amber, width:1.5, dash:'dash' } });
  Plotly.react('chartScenario', traces, baseLayout({
    showlegend:true,
    legend:{ orientation:'h', y:1.16, x:0, font:{size:10}, bgcolor:'rgba(0,0,0,0)' },
    margin:{ l:50, r:54, t:42, b:44 },
    xaxis:{ title:{text:'years',font:{size:11}}, gridcolor:C.grid, range:[0,SC.years] },
    yaxis:{ title:{text:'A_ai attention share',font:{size:11}}, range:[0,1], gridcolor:C.grid },
    yaxis2:{ title:{text:'N_eff (log)',font:{size:11}}, overlaying:'y', side:'right',
             type:'log', gridcolor:'rgba(0,0,0,0)', showgrid:false },
    shapes,
    annotations: tc!==null ? [{ x:tc, y:1, yref:'paper', text:'N_eff=10', showarrow:false,
      font:{color:C.amber,size:10}, yanchor:'bottom' }] : []
  }), PLOT_CFG);
}

/* OOD-shock inset: open-loop diverges, closed-loop "Second Foundation" bounded.
   Representative curves driven by current rho_model via L_eff (Part B of the
   second_foundation note): higher L_eff -> lower post-shock error + shorter lag. */
function scShockChart(rhoModel){
  if (!hasPlotly) return;
  const Tsteps = 60, tau = 24;             // shock onset
  const t = []; for (let i=0;i<Tsteps;i++) t.push(i);
  const Leff = nEff(SC.M, rhoModel);
  // diversity factor in (0,1]: 1 at monoculture, ->0 as lineages proliferate
  const mono = 1 / Math.max(Leff, 1);
  const bDrift = 0.15;                       // unit-root drift magnitude (open-loop)
  const lag = Math.max(1, Math.round(2 + 14 * mono));   // detection lag grows with monoculture
  const open = [], closed = [];
  for (let i=0;i<Tsteps;i++){
    if (i < tau){ open.push(0); closed.push(0); continue; }
    const dt = i - tau;
    // OPEN-LOOP: linear divergence e ~ |b'|*(t-tau), independent of diversity
    open.push(bDrift * dt);
    // CLOSED-LOOP: error grows during the detection lag, then is detected & corrected.
    // Diversity lowers both the lag and the residual ceiling (partly self-correcting).
    let c;
    if (dt <= lag) c = bDrift * dt;                                  // pre-detection excursion
    else { const ceil = bDrift * lag * (0.25 + 0.75 * mono);          // bounded residual
           c = ceil * Math.exp(-(dt - lag) / 6) + 0.02; }
    closed.push(c);
  }
  Plotly.react('chartShock', [
    { x:t, y:open, mode:'lines', name:'open-loop |error| (diverges)',
      line:{ color:C.red, width:2.2, dash:'dash' } },
    { x:t, y:closed, mode:'lines', name:'closed-loop "Second Foundation" (bounded)',
      line:{ color:C.green, width:2.2 } }
  ], baseLayout({
    showlegend:true,
    legend:{ orientation:'h', y:1.18, x:0, font:{size:10}, bgcolor:'rgba(0,0,0,0)' },
    margin:{ l:48, r:16, t:42, b:40 },
    xaxis:{ title:{text:'steps after shock τ',font:{size:11}}, gridcolor:C.grid },
    yaxis:{ title:{text:'|forecast error|',font:{size:11}}, gridcolor:C.grid },
    shapes:[{ type:'line', x0:tau, x1:tau, y0:0, y1:1, yref:'paper',
              line:{ color:C.amber, width:1.4, dash:'dot' } }],
    annotations:[{ x:tau, y:1, yref:'paper', text:'the Mule', showarrow:false,
                   font:{color:C.amber,size:10}, yanchor:'bottom' }]
  }), PLOT_CFG);

  const intOpen = open.reduce((a,b)=>a+b,0), intClosed = closed.reduce((a,b)=>a+b,0);
  const factor = intClosed>0 ? (intOpen/intClosed) : Infinity;
  document.getElementById('scShockReadout').innerHTML =
    `L_eff = <b>${Leff.toFixed(2)}</b> · detection lag <b>${lag}</b> steps · ` +
    `closed-loop reduction <b>${isFinite(factor)?factor.toFixed(0)+'×':'∞'}</b>. ` +
    `Higher L_eff (lower ρ_model) shrinks both the post-shock error and the lag — ` +
    `diversity is partially self-correcting; a monoculture needs the central controller.`;
}

function scUpdate(){
  const P = scReadParams();
  document.getElementById('scGval').textContent = P.gx.toFixed(2) + '×/yr';
  document.getElementById('scDval').textContent = P.dx.toFixed(0) + '×/yr';
  document.getElementById('scAval').textContent = P.alpha.toFixed(2);
  document.getElementById('scRval').textContent = P.rhoModel.toFixed(2);
  document.getElementById('scKval').textContent = P.K.toFixed(0);

  const R = scRun(P);
  scChart(R);
  const t = Array.from(R.t), Neff = Array.from(R.Neff);
  const endNeff = Neff[Neff.length-1];
  const cross = scCrossing(t, Neff, 10, false);
  document.getElementById('scLeff').textContent = R.Leff.toFixed(2);
  document.getElementById('scNeff').textContent = endNeff.toFixed(2);
  document.getElementById('scCross').textContent =
    cross===null ? '≥ 10 yr' : `${cross.toFixed(2)} yr (~mo ${Math.round(cross*12)})`;
  document.getElementById('scTau').textContent =
    (R.tau[R.tau.length-1]/R.tau[0]).toFixed(3) + '× nominal';
  scPhase(endNeff);
  if (scShockOn) scShockChart(P.rhoModel);
}

function scInit(){
  ['scG','scD','scA','scR','scK'].forEach(id=>{
    document.getElementById(id).addEventListener('input', ()=>{
      if (scRAF) cancelAnimationFrame(scRAF);
      scRAF = requestAnimationFrame(()=>{ scUpdate(); scRAF = null; });
    });
  });
  document.getElementById('scShock').addEventListener('click', ()=>{
    scShockOn = true;
    document.getElementById('scShock').textContent = '⚡ Re-inject OOD shock';
    scShockChart(parseFloat(document.getElementById('scR').value));
  });
  scUpdate();
}

/* =========================================================================
   9. BOOT
   ========================================================================= */

// Multi-page safe: only wire a feature when its anchor element is present on
// the current page. id() is a tiny existence guard so the same app.js can boot
// index / tutorial / math / tests without throwing on missing sections.
const has = id => !!document.getElementById(id);

function boot(){
  if (has('headlineStat')) fillHero();
  if (has('canonBody'))    fillCanon();
  if (has('readingsBody')){ fillFilters(); renderTable(); }
  if (has('chartScope'))   fillCoverageCharts();
  if (has('demoA'))        wireDemoA();
  if (has('demoC'))        wireDemoC();
  if (has('scenarioCard')) scInit();
  if (has('classifyBtn'))  wireClassify();
  // Demo B is heaviest (sweep precompute); defer a tick so the page paints first.
  if (has('demoB')) setTimeout(wireDemoB, 30);

  if (!hasPlotly){
    document.querySelectorAll('.chart').forEach(el=>{
      el.innerHTML = '<div class="offline-note" style="padding:20px">Charts need internet (Plotly CDN). All sliders, numbers, filters and the classifier still work offline.</div>';
    });
  }
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();
