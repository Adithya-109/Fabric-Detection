/**
 * Fabric Classifier — Frontend Application Logic
 * Premium Textile Classification & Vision Platform
 */

document.addEventListener('DOMContentLoaded', () => {

  /* ───────────────────────────────────────
     1. State Management
  ─────────────────────────────────────── */
  let currentView     = 'landing';
  let currentFile     = null;
  let currentSampleId = null;
  let latestResult    = null;
  let isClassifying   = false;
  let patchSlideIndex = 0;
  let totalPatches    = 0;
  const PATCHES_VISIBLE = 4;

  /* ───────────────────────────────────────
     2. Element Selectors
  ─────────────────────────────────────── */
  // Views
  const viewLanding   = document.getElementById('view-landing');
  const viewDashboard = document.getElementById('view-dashboard');

  // Navigation
  const tabHome       = document.getElementById('tab-home');
  const tabDash       = document.getElementById('tab-dashboard');
  const tabCatalog    = document.getElementById('tab-catalog');
  const tabContact    = document.getElementById('tab-contact');
  const navBrand      = document.getElementById('nav-brand');
  const btnLaunch     = document.getElementById('btn-launch');
  const btnLogin      = document.getElementById('btn-login');
  const themeBtn      = document.getElementById('theme-btn');
  
  // Landing Page Elements
  const heroUpload    = document.getElementById('hero-upload');
  const heroFileInput = document.getElementById('hero-file-input');
  const heroSamples   = document.getElementById('hero-sample-thumbs');
  const btnEnterDash  = document.getElementById('btn-enter-dashboard');

  // Dashboard Sidebar & Header
  const sbHome        = document.getElementById('sb-home');
  const sbUpload      = document.getElementById('sb-upload');
  const sbCatalog     = document.getElementById('sb-catalog');
  const sbDiag        = document.getElementById('sb-diag');
  const sbExit        = document.getElementById('sb-exit');
  const btnBack       = document.getElementById('btn-back-landing');

  // Ingestion Card
  const dropzone        = document.getElementById('dropzone');
  const dashFileInput   = document.getElementById('dash-file-input');
  const previewImg      = document.getElementById('preview-img');
  const ingestionBadge  = document.getElementById('ingestion-badge');
  const imgFilename     = document.getElementById('img-filename');
  const imgMeta         = document.getElementById('img-meta');
  const ingestionMeta   = document.getElementById('ingestion-meta');
  const qsPills         = document.querySelectorAll('.qs-pill');
  const btnClassify     = document.getElementById('btn-classify');
  const classifySpinner = document.getElementById('classify-spinner');
  const classifyLabel   = document.getElementById('classify-label');

  // Processing Visualizer Card
  const ringFill      = document.getElementById('ring-fill');
  const ringPct       = document.getElementById('ring-pct');
  const visBadge      = document.getElementById('vis-badge');
  const visDesc       = document.getElementById('vis-desc');
  const stepPatch     = document.getElementById('step-patch');
  const stepPreproc   = document.getElementById('step-preprocess');
  const stepInfer     = document.getElementById('step-inference');
  const stepAgg       = document.getElementById('step-aggregation');

  // Prediction Card
  const cardPrediction = document.getElementById('card-prediction');
  const predFabric     = document.getElementById('pred-fabric');
  const predCategory   = document.getElementById('pred-category');
  const predScore      = document.getElementById('pred-score');
  const predBarFill    = document.getElementById('pred-bar-fill');
  const predTagline    = document.getElementById('pred-tagline');
  const confBadge      = document.getElementById('conf-badge');
  const pvBreath       = document.getElementById('pv-breathability');
  const pvDurab        = document.getElementById('pv-durability');
  const pvStretch      = document.getElementById('pv-stretch');
  const pvTexture      = document.getElementById('pv-texture');

  // Contenders Card
  const cardContenders = document.getElementById('card-contenders');
  const contendersEl   = document.getElementById('contenders');
  const btnShowDist    = document.getElementById('btn-show-dist');
  const fullDistEl     = document.getElementById('full-dist');

  // 7-Patch Multi-Crop
  const cardPatches    = document.getElementById('card-patches');
  const patchTrack     = document.getElementById('patch-track');
  const patchPrev      = document.getElementById('patch-prev');
  const patchNext      = document.getElementById('patch-next');
  const sliderDots     = document.getElementById('slider-dots');

  // Diagnostics Card
  const cardDiag       = document.getElementById('card-diagnostics');
  const dPatch         = document.getElementById('d-patch');
  const dPredStat      = document.getElementById('d-pred-stat');
  const dModel         = document.getElementById('d-model');
  const dRes           = document.getElementById('d-res');
  const dDevSub        = document.getElementById('d-device-sub');

  // JSON Drawer
  const cardJson       = document.getElementById('card-json');
  const jsonToggle     = document.getElementById('json-toggle');
  const jsonBody       = document.getElementById('json-body');
  const jsonArrow      = document.getElementById('json-arrow');
  const jsonPre        = document.getElementById('json-pre');
  const btnCopyJson    = document.getElementById('btn-copy-json');

  // Taxonomy Modal
  const catalogModal   = document.getElementById('catalog-modal');
  const modalClose     = document.getElementById('modal-close');
  const catalogList    = document.getElementById('catalog-list');

  // Toast
  const toast          = document.getElementById('toast');

  /* ───────────────────────────────────────
     3. Helper: Percentage Normalizer
  ─────────────────────────────────────── */
  function normalizePct(val) {
    if (typeof val !== 'number' || isNaN(val)) return 0;
    return val > 1.0 ? val : val * 100;
  }

  /* ───────────────────────────────────────
     4. Theme Switcher (Guideline 1)
  ─────────────────────────────────────── */
  function initTheme() {
    const saved = localStorage.getItem('tex_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);

    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const cur = document.documentElement.getAttribute('data-theme') || 'dark';
        const next = cur === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('tex_theme', next);
      });
    }
  }

  /* ───────────────────────────────────────
     5. Ambient Interactive Particles (Guideline 2)
  ─────────────────────────────────────── */
  let particleHoverBoost = false;

  function initParticles() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W, H;
    let particles = [];

    function resize() {
      W = canvas.width  = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const count = 55;
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        baseR: Math.random() * 1.6 + 0.6,
        r: Math.random() * 1.6 + 0.6,
        alpha: Math.random() * 0.45 + 0.15
      });
    }

    function renderFrame() {
      ctx.clearRect(0, 0, W, H);
      const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
      const col = isDark ? '56, 189, 248' : '79, 70, 229';

      particles.forEach(p => {
        const speedMult = particleHoverBoost ? 2.0 : 1.0;
        p.x += p.vx * speedMult;
        p.y += p.vy * speedMult;

        if (p.x < 0) p.x = W;
        if (p.x > W) p.x = 0;
        if (p.y < 0) p.y = H;
        if (p.y > H) p.y = 0;

        const targetR = particleHoverBoost ? p.baseR * 1.8 : p.baseR;
        p.r += (targetR - p.r) * 0.1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${col}, ${p.alpha})`;
        ctx.fill();
      });

      requestAnimationFrame(renderFrame);
    }
    renderFrame();

    // Hook hero upload hover effects (Guideline 2: ambient expansion & ±15px move)
    if (heroUpload) {
      heroUpload.addEventListener('mouseenter', () => {
        particleHoverBoost = true;
        document.body.classList.add('hero-upload-hovered');
      });
      heroUpload.addEventListener('mouseleave', () => {
        particleHoverBoost = false;
        document.body.classList.remove('hero-upload-hovered');
      });
    }
  }

  /* ───────────────────────────────────────
     6. Navigation & View Routing
  ─────────────────────────────────────── */
  function showView(view) {
    currentView = view;
    if (view === 'landing') {
      viewLanding.classList.remove('hidden');
      viewDashboard.classList.add('hidden');
      if (tabHome) tabHome.classList.add('active');
      if (tabDash) tabDash.classList.remove('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      viewLanding.classList.add('hidden');
      viewDashboard.classList.remove('hidden');
      if (tabHome) tabHome.classList.remove('active');
      if (tabDash) tabDash.classList.add('active');
      checkHealth();
    }
  }

  function initNavigation() {
    if (tabHome)      tabHome.addEventListener('click',      () => showView('landing'));
    if (tabDash)      tabDash.addEventListener('click',      () => showView('dashboard'));
    if (tabCatalog)   tabCatalog.addEventListener('click',   openCatalogModal);
    if (tabContact)   tabContact.addEventListener('click',   () => showToast('Fabric Classifier', 'success'));
    if (navBrand)     navBrand.addEventListener('click',     () => showView('landing'));
    if (btnLaunch)    btnLaunch.addEventListener('click',    () => showView('dashboard'));
    if (btnLogin)     btnLogin.addEventListener('click',     () => showView('dashboard'));
    if (btnEnterDash) btnEnterDash.addEventListener('click', () => showView('dashboard'));
    if (btnBack)      btnBack.addEventListener('click',      () => showView('landing'));

    // Sidebar
    if (sbHome)   sbHome.addEventListener('click',   () => scrollToDashboardTop());
    if (sbUpload) sbUpload.addEventListener('click', () => { if (dropzone) dropzone.click(); });
    if (sbCatalog)sbCatalog.addEventListener('click',openCatalogModal);
    if (sbDiag)   sbDiag.addEventListener('click',   () => scrollToDiagnostics());
    if (sbExit)   sbExit.addEventListener('click',   () => showView('landing'));
  }

  function scrollToDashboardTop() {
    const main = document.querySelector('.dash-grid');
    if (main) main.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function scrollToDiagnostics() {
    if (cardDiag) cardDiag.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  /* ───────────────────────────────────────
     7. Image Ingestion & Sample Handling
  ─────────────────────────────────────── */
  const SAMPLE_PRESETS = {
    'poly_cotton_check': {
      title: 'Check Weave Fabric',
      meta: 'Poly-cotton gingham check preset · 1000×1000',
      url: '/api/samples/poly_cotton_check.jpeg'
    },
    'denim_sample': {
      title: 'Denim Twill',
      meta: 'Diagonal twill indigo denim preset · 1000×1000',
      url: '/api/samples/denim_sample.jpg'
    },
    'silk_sample': {
      title: 'Silk Satin',
      meta: 'Glossy fluid silk sheen preset · 1000×1000',
      url: '/api/samples/silk_sample.jpg'
    },
    'wool_knit_sample': {
      title: 'Wool Knit',
      meta: 'Natural looped wool yarn preset · 1000×1000',
      url: '/api/samples/wool_knit_sample.jpg'
    }
  };

  function initUploadHandlers() {
    // Hero Drag & Drop / Click
    if (heroUpload) {
      heroUpload.addEventListener('click', () => heroFileInput.click());
      heroUpload.addEventListener('dragover', e => {
        e.preventDefault();
        heroUpload.style.borderColor = 'var(--cyan)';
      });
      heroUpload.addEventListener('dragleave', () => {
        heroUpload.style.borderColor = '';
      });
      heroUpload.addEventListener('drop', e => {
        e.preventDefault();
        heroUpload.style.borderColor = '';
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
          onFileSelected(file);
          showView('dashboard');
        }
      });
      heroFileInput.addEventListener('change', e => {
        const file = e.target.files[0];
        if (file) {
          onFileSelected(file);
          showView('dashboard');
        }
      });
    }

    // Hero Sample Thumbnails
    if (heroSamples) {
      heroSamples.querySelectorAll('.sample-thumb').forEach(btn => {
        btn.addEventListener('click', () => {
          const sid = btn.dataset.sample;
          selectSample(sid);
          showView('dashboard');
        });
      });
    }

    // Dashboard Dropzone
    if (dropzone) {
      dropzone.addEventListener('click', () => dashFileInput.click());
      dropzone.addEventListener('dragover', e => {
        e.preventDefault();
        dropzone.style.borderColor = 'var(--cyan)';
      });
      dropzone.addEventListener('dragleave', () => {
        dropzone.style.borderColor = '';
      });
      dropzone.addEventListener('drop', e => {
        e.preventDefault();
        dropzone.style.borderColor = '';
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
          onFileSelected(file);
        }
      });
      dashFileInput.addEventListener('change', e => {
        const file = e.target.files[0];
        if (file) onFileSelected(file);
      });
    }

    // Quick Test Sample Pills
    qsPills.forEach(pill => {
      pill.addEventListener('click', () => {
        const sid = pill.dataset.sample;
        selectSample(sid);
      });
    });

    // Classify Button
    if (btnClassify) {
      btnClassify.addEventListener('click', executeClassification);
    }
  }

  // Result cards stay empty until an image has been classified.
  function setDashboardEmpty(isEmpty) {
    if (viewDashboard) viewDashboard.classList.toggle('dash-empty', isEmpty);
  }

  function showIngestedImage(url, title, meta) {
    if (previewImg) previewImg.src = url;
    if (imgFilename) imgFilename.textContent = title;
    if (imgMeta) imgMeta.textContent = meta;
    if (ingestionMeta) ingestionMeta.classList.remove('hidden');
    if (dropzone) dropzone.classList.add('has-image');
    if (btnClassify) btnClassify.disabled = false;
    setDashboardEmpty(true);
    resetVisualizer();
    if (visBadge) { visBadge.textContent = 'Idle'; visBadge.style.color = ''; }
    if (visDesc) visDesc.textContent = 'Image received';
  }

  function onFileSelected(file) {
    currentFile = file;
    currentSampleId = null;
    qsPills.forEach(p => p.classList.remove('active'));

    const kb = (file.size / 1024).toFixed(1);
    showIngestedImage(URL.createObjectURL(file), file.name, `Uploaded file · ${kb} KB · ${file.type || 'Image'}`);
    setIngestionState('ready');
    executeClassification();
  }

  function selectSample(sampleId) {
    currentSampleId = sampleId;
    currentFile = null;

    qsPills.forEach(p => {
      p.classList.toggle('active', p.dataset.sample === sampleId);
    });

    const info = SAMPLE_PRESETS[sampleId];
    if (info) showIngestedImage(info.url, info.title, info.meta);
    setIngestionState('ready');
    executeClassification();
  }

  function setIngestionState(state) {
    if (!ingestionBadge) return;
    ingestionBadge.className = 'badge';
    if (state === 'ready') {
      ingestionBadge.classList.add('badge-ready');
      ingestionBadge.textContent = 'Ready';
    } else if (state === 'processing') {
      ingestionBadge.classList.add('badge-processing');
      ingestionBadge.textContent = 'Processing';
    } else if (state === 'done') {
      ingestionBadge.classList.add('badge-done');
      ingestionBadge.textContent = 'Done';
    }
  }

  /* ───────────────────────────────────────
     8. Circular Progress Visualizer (Guideline 3)
  ─────────────────────────────────────── */
  const CIRCLE_CIRCUMFERENCE = 326.73;

  function setProgressPercent(pct) {
    if (!ringFill) return;
    const clamped = Math.max(0, Math.min(100, pct));
    const offset = CIRCLE_CIRCUMFERENCE * (1 - clamped / 100);
    ringFill.style.strokeDashoffset = offset;
    if (ringPct) ringPct.textContent = `${Math.round(clamped)}%`;
  }

  function resetVisualizer() {
    setProgressPercent(0);
    [stepPatch, stepPreproc, stepInfer, stepAgg].forEach(s => {
      if (s) s.classList.remove('active', 'done');
    });
    if (visBadge) {
      visBadge.textContent = 'Processing';
      visBadge.style.color = 'var(--cyan)';
    }
    if (visDesc) visDesc.textContent = 'Preparing image...';
  }

  const PIPELINE_STAGES = [
    { el: stepPatch,   dot: 'dot-patch',       pct: 20, desc: 'Preparing the image...', ms: 300 },
    { el: stepPreproc, dot: 'dot-preprocess',  pct: 45, desc: 'Normalizing the image...', ms: 250 },
    { el: stepInfer,   dot: 'dot-inference',   pct: 85, desc: 'Running the model...',                ms: 700 },
    { el: stepAgg,     dot: 'dot-aggregation', pct: 98, desc: 'Scoring the fabric classes...',        ms: 200 }
  ];

  function runVisualizerAnimation() {
    let idx = 0;
    function next() {
      if (idx >= PIPELINE_STAGES.length || !isClassifying) return;
      const stage = PIPELINE_STAGES[idx];

      PIPELINE_STAGES.forEach(s => {
        if (s.el && !s.el.classList.contains('done')) s.el.classList.remove('active');
      });
      if (stage.el) stage.el.classList.add('active');
      if (visDesc) visDesc.textContent = stage.desc;

      const startPct = idx === 0 ? 0 : PIPELINE_STAGES[idx - 1].pct;
      const endPct   = stage.pct;
      const duration = stage.ms;
      const startTime = performance.now();

      function stepFrame(now) {
        const elapsed = Math.min((now - startTime) / duration, 1);
        const ease = 1 - Math.pow(1 - elapsed, 3);
        setProgressPercent(startPct + (endPct - startPct) * ease);
        if (elapsed < 1 && isClassifying) {
          requestAnimationFrame(stepFrame);
        } else if (isClassifying) {
          if (stage.el) {
            stage.el.classList.remove('active');
            stage.el.classList.add('done');
          }
          idx++;
          if (idx < PIPELINE_STAGES.length) next();
        }
      }
      requestAnimationFrame(stepFrame);
    }
    next();
  }

  async function completeVisualizer() {
    setProgressPercent(100);
    [stepPatch, stepPreproc, stepInfer, stepAgg].forEach(s => {
      if (s) { s.classList.remove('active'); s.classList.add('done'); }
    });
    if (visBadge) {
      visBadge.textContent = 'Done';
      visBadge.style.color = 'var(--emerald)';
    }
    if (visDesc) visDesc.textContent = 'Classification successfully verified';
    return new Promise(r => setTimeout(r, 200));
  }

  /* ───────────────────────────────────────
     9. Execute Inference Pipeline
  ─────────────────────────────────────── */
  async function executeClassification() {
    if (isClassifying) return;
    isClassifying = true;

    // Button loading state
    if (btnClassify) btnClassify.disabled = true;
    if (classifySpinner) classifySpinner.classList.remove('hidden');
    if (classifyLabel) classifyLabel.textContent = 'Analyzing Garment…';
    setIngestionState('processing');

    setDashboardEmpty(true);
    resetVisualizer();
    runVisualizerAnimation();

    try {
      let response;
      if (currentFile) {
        const formData = new FormData();
        formData.append('image', currentFile);
        response = await fetch('/api/predict', { method: 'POST', body: formData });
      } else {
        response = await fetch('/api/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sample_id: currentSampleId })
        });
      }

      const data = await response.json();
      if (data.error) throw new Error(data.error);

      latestResult = data;
      await completeVisualizer();

      // Display results with sequential fade-up (Guideline 3)
      renderClassificationResult(data);
      setDashboardEmpty(false);
      triggerSequentialFade();

      setIngestionState('done');
      showToast('Garment classified successfully!', 'success');

    } catch (err) {
      console.error('Classification error:', err);
      showToast(`Error: ${err.message}`, 'error');
      setIngestionState('ready');
      resetVisualizer();
    } finally {
      isClassifying = false;
      if (btnClassify) btnClassify.disabled = false;
      if (classifySpinner) classifySpinner.classList.add('hidden');
      if (classifyLabel) classifyLabel.textContent = 'Classify Fabric';
    }
  }

  /* ───────────────────────────────────────
     10. Sequential Fade-In (Guideline 3)
  ─────────────────────────────────────── */
  function triggerSequentialFade() {
    const cards = [cardPrediction, cardContenders, cardPatches, cardDiag, cardJson];
    cards.forEach(card => {
      if (!card) return;
      card.classList.remove('stagger-in');
      void card.offsetWidth; // Force reflow
      card.classList.add('stagger-in');
    });
  }

  /* ───────────────────────────────────────
     11. Render Classification Results
  ─────────────────────────────────────── */
  function renderClassificationResult(data) {
    const top = data.prediction || data.top_class || {};
    const name = top.name || top.class_name || '—';
    const confScore = normalizePct(top.confidence);
    const pctString = `${confScore.toFixed(2)}%`;
    const category = top.category || top.profile?.category || 'Natural Textile Fiber';
    const tagline = top.tagline || top.profile?.tagline || '';
    const profile = top.profile || {};
    const properties = profile.properties || top.properties || {};

    // 1. Prediction Card
    if (predFabric)   predFabric.textContent = name.toUpperCase();
    if (predCategory) predCategory.textContent = `(${category})`;
    if (predScore)    predScore.textContent = pctString;
    if (predBarFill)  predBarFill.style.width = `${Math.min(confScore, 100).toFixed(1)}%`;
    if (confBadge)    confBadge.textContent = pctString;
    if (predTagline)  predTagline.textContent = profile.description || tagline || 'Classified fabric characteristics.';

    if (pvBreath)  pvBreath.textContent  = properties.breathability || 'High';
    if (pvDurab)   pvDurab.textContent   = properties.durability    || 'High';
    if (pvStretch) pvStretch.textContent = properties.stretch       || 'Low';
    if (pvTexture) pvTexture.textContent = properties.texture       || 'Soft natural hand';

    // 2. Top-3 Contenders
    const top3 = data.top_3 || data.top3 || [];
    renderContendersList(top3, data.all_classes || []);

    // 4. 7-Patch Multi-Crop Carousel (Guideline 4)
    const patches = data.patches || [];
    renderPatchesCarousel(patches);

    // 5. Diagnostic Metrics (4 Stat Cards)
    const timing = data.timing || {};
    const metrics = data.metrics || {};
    const imgInfo = data.image_info || {};

    const patchTime = timing.patch_ms || metrics.patch_extraction_ms || 0;
    const modelTime = timing.model_ms || metrics.model_inference_ms || 0;

    if (dPatch)    dPatch.textContent    = `${patchTime.toFixed(2)}`;
    if (dPredStat) dPredStat.textContent = pctString;
    if (dModel)    dModel.textContent    = `${modelTime.toFixed(2)}`;
    if (dRes)      dRes.textContent      = imgInfo.width ? `${imgInfo.width}×${imgInfo.height}` : '—';

    // 6. JSON Drawer with Color Syntax Highlighting (Guideline 4)
    if (jsonPre) {
      jsonPre.innerHTML = syntaxHighlightJson(JSON.stringify(data, null, 2));
    }
  }

  /* ───────────────────────────────────────
     12. Render Contenders List
  ─────────────────────────────────────── */
  function renderContendersList(top3, allClasses) {
    if (!contendersEl) return;
    if (!top3 || top3.length === 0) {
      contendersEl.innerHTML = '<p style="color:var(--text-f);font-size:0.8rem">No contenders returned</p>';
      return;
    }

    const maxConf = normalizePct(top3[0]?.confidence) || 100;
    const fillClasses = ['c-fill-1', 'c-fill-2', 'c-fill-3'];
    const colors = ['var(--cyan)', 'var(--indigo)', 'var(--emerald)'];

    contendersEl.innerHTML = top3.slice(0, 3).map((item, i) => {
      const c = normalizePct(item.confidence);
      const pct = `${c.toFixed(2)}%`;
      const barWidth = Math.min((c / maxConf) * 100, 100).toFixed(1);
      const cName = item.name || item.class_name || 'Fabric';

      return `
        <div class="contender-row">
          <div class="contender-hdr">
            <span class="contender-name">${cName}</span>
            <span class="rank-num">#${i + 1}</span>
          </div>
          <div class="c-bar-bg">
            <div class="c-bar-fill ${fillClasses[i]}" style="width:${barWidth}%"></div>
          </div>
          <span class="contender-pct" style="color:${colors[i]}">${pct}</span>
        </div>`;
    }).join('');

    // Full 14-Class Distribution
    if (allClasses && allClasses.length > 0 && fullDistEl && btnShowDist) {
      fullDistEl.innerHTML = allClasses.slice().sort((a,b) => {
        return normalizePct(b.confidence) - normalizePct(a.confidence);
      }).map(cls => {
        const c = normalizePct(cls.confidence);
        const barW = Math.max(c, 0.5).toFixed(1);
        const name = cls.name || cls.class_name;
        return `
          <div class="full-dist-item">
            <span class="fdi-name">${name}</span>
            <div class="fdi-bar-bg"><div class="fdi-bar-fill" style="width:${barW}%"></div></div>
            <span class="fdi-pct">${c.toFixed(2)}%</span>
          </div>`;
      }).join('');
    }
  }

  // Distribution Toggle Button
  if (btnShowDist && fullDistEl) {
    btnShowDist.addEventListener('click', () => {
      const isOpen = !fullDistEl.classList.contains('hidden');
      fullDistEl.classList.toggle('hidden', isOpen);
      btnShowDist.textContent = isOpen ? 'Show Full Distribution (14 classes)' : 'Hide Distribution';
    });
  }

  /* ───────────────────────────────────────
     13. 7-Patch Multi-Crop Carousel (Guideline 4)
  ─────────────────────────────────────── */
  function renderPatchesCarousel(patches) {
    if (!patchTrack) return;
    if (!patches || patches.length === 0) {
      patchTrack.innerHTML = '<div class="patch-placeholder"><p>No patches available</p></div>';
      return;
    }

    totalPatches = patches.length;
    patchSlideIndex = 0;

    patchTrack.innerHTML = patches.map((p, i) => {
      const src = p.data_uri || (p.image_base64 ? `data:image/jpeg;base64,${p.image_base64}` : p.image_url);
      const idx = p.patch_index || i + 1;
      return `
        <div class="patch-item" data-index="${i}">
          <img src="${src}" alt="Patch ${idx}" title="Fabric crop #${idx} (${p.width || 224}×${p.height || 224})">
          <span class="patch-label">Patch ${idx}</span>
        </div>`;
    }).join('');

    updateSliderState();
  }

  function updateSliderState() {
    if (!patchTrack) return;
    const itemWidth = 141; // 125px width + 16px gap
    const maxOffset = Math.max(0, (totalPatches - PATCHES_VISIBLE) * itemWidth);
    const targetOffset = Math.min(patchSlideIndex * itemWidth, maxOffset);

    // Smooth transform translateX (Guideline 4)
    patchTrack.style.transform = `translateX(-${targetOffset}px)`;

    // Update dots
    if (sliderDots) {
      const numSteps = Math.max(1, totalPatches - PATCHES_VISIBLE + 1);
      sliderDots.innerHTML = Array.from({ length: numSteps }, (_, i) => `
        <div class="s-dot ${i === patchSlideIndex ? 'active' : ''}"></div>
      `).join('');
    }
  }

  if (patchPrev) {
    patchPrev.addEventListener('click', () => {
      if (patchSlideIndex > 0) {
        patchSlideIndex--;
        updateSliderState();
      }
    });
  }

  if (patchNext) {
    patchNext.addEventListener('click', () => {
      const maxIndex = Math.max(0, totalPatches - PATCHES_VISIBLE);
      if (patchSlideIndex < maxIndex) {
        patchSlideIndex++;
        updateSliderState();
      }
    });
  }

  /* ───────────────────────────────────────
     14. JSON Accordion Drawer (Guideline 4)
  ─────────────────────────────────────── */
  if (jsonToggle) {
    jsonToggle.addEventListener('click', () => {
      if (!jsonBody) return;
      const isOpen = jsonBody.classList.contains('open');
      jsonBody.classList.toggle('open', !isOpen);
      if (jsonArrow) jsonArrow.classList.toggle('open', !isOpen);
    });
  }

  if (btnCopyJson) {
    btnCopyJson.addEventListener('click', e => {
      e.stopPropagation();
      if (!latestResult) {
        showToast('No classification results to copy', 'error');
        return;
      }
      navigator.clipboard.writeText(JSON.stringify(latestResult, null, 2))
        .then(() => showToast('JSON copied to clipboard!', 'success'))
        .catch(() => showToast('Failed to copy JSON', 'error'));
    });
  }

  // Syntax Highlighting for Raw JSON block
  function syntaxHighlightJson(jsonStr) {
    if (!jsonStr) return '';
    jsonStr = jsonStr.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return jsonStr.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, match => {
      let cls = 'json-number';
      if (/^"/.test(match)) {
        if (/:$/.test(match)) {
          cls = 'json-key';
        } else {
          cls = 'json-string';
        }
      } else if (/true|false/.test(match)) {
        cls = 'json-bool';
      } else if (/null/.test(match)) {
        cls = 'json-null';
      }
      return `<span class="${cls}">${match}</span>`;
    });
  }

  /* ───────────────────────────────────────
     15. 14 Fabrics Taxonomy Modal
  ─────────────────────────────────────── */
  function initTaxonomyModal() {
    if (modalClose)   modalClose.addEventListener('click', closeCatalogModal);
    if (catalogModal) catalogModal.addEventListener('click', e => {
      if (e.target === catalogModal) closeCatalogModal();
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeCatalogModal();
    });
  }

  async function openCatalogModal() {
    if (!catalogModal) return;
    catalogModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';

    if (catalogList && catalogList.children.length === 0) {
      catalogList.innerHTML = '<p style="color:var(--text-f);font-size:0.85rem">Loading taxonomy...</p>';
      try {
        const res = await fetch('/api/classes');
        const data = await res.json();
        const classes = data.classes || [];
        catalogList.innerHTML = classes.map(cls => `
          <div class="catalog-item">
            <span class="catalog-name">${cls.name}</span>
            <span class="catalog-cat">${cls.category || 'Textile Material'}</span>
            <p class="catalog-tagline">${cls.tagline || ''}</p>
          </div>
        `).join('');
      } catch (err) {
        catalogList.innerHTML = '<p style="color:var(--rose);font-size:0.85rem">Failed to load classes</p>';
      }
    }
  }

  function closeCatalogModal() {
    if (catalogModal) catalogModal.classList.add('hidden');
    document.body.style.overflow = '';
  }

  /* ───────────────────────────────────────
     16. Health & Diagnostics Check
  ─────────────────────────────────────── */
  async function checkHealth() {
    try {
      const res = await fetch('/api/health');
      const data = await res.json();
      const sys = data.system || {};
      const dev = sys.device || 'Apple Silicon (CPU)';
      const arch = sys.architecture || 'ARM64';

      if (dDevSub)    dDevSub.textContent    = `${dev} • ${arch}`;
    } catch {
      showToast('Cannot reach the server — check that it is running', 'error');
    }
  }

  /* ───────────────────────────────────────
     17. Toast Notifications
  ─────────────────────────────────────── */
  let toastTimer = null;
  function showToast(message, type = 'success') {
    if (!toast) return;
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.className = 'toast';
    }, 3200);
  }

  /* ───────────────────────────────────────
     18. App Initialization
  ─────────────────────────────────────── */
  initTheme();
  initParticles();
  initNavigation();
  initUploadHandlers();
  initTaxonomyModal();
  checkHealth();

  // The dashboard starts empty: nothing is shown until the user provides an image.
  setDashboardEmpty(true);
});
