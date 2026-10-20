/**
 * TexClassifier AI — Frontend Application Logic
 * Light/Dark Mode • Floating Fiber Particles • Multi-Patch Slider • Real-time Inference
 */

document.addEventListener('DOMContentLoaded', () => {
  // --- View Elements ---
  const landingView = document.getElementById('landing-view');
  const dashboardView = document.getElementById('dashboard-view');
  const tabLanding = document.getElementById('tab-landing');
  const tabDashboard = document.getElementById('tab-dashboard');
  const tabCatalog = document.getElementById('tab-catalog');
  const btnNavLaunch = document.getElementById('btn-nav-launch');
  const btnScrollDashboard = document.getElementById('btn-scroll-dashboard');
  const btnDashBackLanding = document.getElementById('btn-dash-back-landing');
  const btnSideHome = document.getElementById('btn-side-home');
  const btnSideExit = document.getElementById('btn-side-exit');

  // --- Theme Toggle ---
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  
  // --- Hero Upload Elements ---
  const heroUploadCard = document.getElementById('hero-upload-card');
  const heroFileInput = document.getElementById('hero-file-input');
  
  // --- Dashboard Elements ---
  const dashDropzone = document.getElementById('dash-dropzone');
  const dashFileInput = document.getElementById('dash-file-input');
  const dashPreviewImg = document.getElementById('dash-preview-img');
  const dashFilenameLabel = document.getElementById('dash-filename-label');
  const dashFileMeta = document.getElementById('dash-file-meta');
  const dashClassifyBtn = document.getElementById('btn-dash-classify');
  const dashSpinner = document.getElementById('dash-spinner');
  const dashClassifyLabel = document.getElementById('dash-classify-label');
  const samplePills = document.querySelectorAll('.sample-pill');

  // Visualizer / Loader
  const spinnerPct = document.getElementById('spinner-pct');
  const visualizerStepTitle = document.getElementById('visualizer-step-title');
  const visualizerStepDesc = document.getElementById('visualizer-step-desc');
  const dynamicProgressFill = document.getElementById('dynamic-progress-fill');

  // Prediction & Contenders
  const predCategory = document.getElementById('pred-category');
  const predName = document.getElementById('pred-name');
  const predScore = document.getElementById('pred-score');
  const predTagline = document.getElementById('pred-tagline');
  const contendersList = document.getElementById('contenders-list');

  // 7-Patch Slider
  const sliderTrack = document.getElementById('slider-track');
  const sliderPrev = document.getElementById('slider-prev');
  const sliderNext = document.getElementById('slider-next');
  const sliderDots = document.getElementById('slider-dots');

  // Diagnostics
  const diagTotalTime = document.getElementById('diag-total-time');
  const diagModelTime = document.getElementById('diag-model-time');
  const diagPatchTime = document.getElementById('diag-patch-time');
  const diagRamFootprint = document.getElementById('diag-ram-footprint');
  const diagRamSub = document.getElementById('diag-ram-sub');

  // JSON Accordion
  const jsonAccordionHeader = document.getElementById('json-accordion-header');
  const jsonAccordionBody = document.getElementById('json-accordion-body');
  const accordionArrow = document.getElementById('accordion-arrow');
  const dashJsonCode = document.getElementById('dash-json-code');
  const btnCopyJson = document.getElementById('btn-copy-json');

  // Modal
  const catalogModal = document.getElementById('catalog-modal');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const catalogList = document.getElementById('catalog-list');
  const btnSideCatalog = document.getElementById('btn-side-catalog');

  // Status & Health
  const statusLabel = document.getElementById('status-label');

  // State
  let currentFile = null;
  let currentSampleId = 'poly_cotton_check';
  let latestResult = null;
  let currentSlideIndex = 0;
  const patchesPerView = 5;

  // Initialize features
  initTheme();
  initFiberCanvas();
  initNavigation();
  initUploadHandlers();
  initSlider();
  initJsonAccordion();
  initCatalogModal();
  checkSystemHealth();

  // --------------------------------------------------------------------------
  // 1. Theme Management (Light / Dark Mode)
  // --------------------------------------------------------------------------
  function initTheme() {
    const savedTheme = localStorage.getItem('tex_theme') || 'dark';
    setTheme(savedTheme);

    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      setTheme(newTheme);
    });
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('tex_theme', theme);
  }

  // --------------------------------------------------------------------------
  // 2. View Switching (Landing Hero <-> Dashboard)
  // --------------------------------------------------------------------------
  function initNavigation() {
    function showLanding() {
      landingView.classList.remove('hidden');
      dashboardView.classList.add('hidden');
      tabLanding.classList.add('active');
      tabDashboard.classList.remove('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function showDashboard() {
      landingView.classList.add('hidden');
      dashboardView.classList.remove('hidden');
      tabLanding.classList.remove('active');
      tabDashboard.classList.add('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    tabLanding.addEventListener('click', showLanding);
    tabDashboard.addEventListener('click', showDashboard);
    btnNavLaunch.addEventListener('click', showDashboard);
    btnScrollDashboard.addEventListener('click', showDashboard);
    btnDashBackLanding.addEventListener('click', showLanding);
    btnSideHome.addEventListener('click', showDashboard);
    btnSideExit.addEventListener('click', showLanding);

    tabCatalog.addEventListener('click', openCatalog);
    btnSideCatalog.addEventListener('click', openCatalog);
  }

  // --------------------------------------------------------------------------
  // 3. Floating Textile Fiber Canvas Particles
  // --------------------------------------------------------------------------
  function initFiberCanvas() {
    const canvas = document.getElementById('fiber-particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];
    const particleCount = 28;

    function resize() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // Particle constructor representing a floating textile fiber / speck
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        length: 8 + Math.random() * 20,
        angle: Math.random() * Math.PI * 2,
        speed: 0.15 + Math.random() * 0.35,
        curve: (Math.random() - 0.5) * 0.04,
        opacity: 0.15 + Math.random() * 0.45,
        colorHue: Math.random() > 0.5 ? 210 : 250 // cyan or indigo
      });
    }

    function animate() {
      ctx.clearRect(0, 0, width, height);

      const isLight = document.documentElement.getAttribute('data-theme') === 'light';
      const baseOpacityMultiplier = isLight ? 0.3 : 0.8;

      particles.forEach(p => {
        p.angle += p.curve;
        p.x += Math.cos(p.angle) * p.speed;
        p.y += Math.sin(p.angle) * p.speed;

        // Wrap around borders
        if (p.x < -40) p.x = width + 40;
        if (p.x > width + 40) p.x = -40;
        if (p.y < -40) p.y = height + 40;
        if (p.y > height + 40) p.y = -40;

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.angle);
        ctx.beginPath();
        ctx.moveTo(-p.length / 2, 0);
        ctx.quadraticCurveTo(0, 3, p.length / 2, 0);

        ctx.strokeStyle = `hsla(${p.colorHue}, 85%, 65%, ${p.opacity * baseOpacityMultiplier})`;
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.restore();
      });

      requestAnimationFrame(animate);
    }
    animate();
  }

  // --------------------------------------------------------------------------
  // 4. File Upload & Sample Handlers
  // --------------------------------------------------------------------------
  function initUploadHandlers() {
    // Landing Page Card
    heroUploadCard.addEventListener('click', () => heroFileInput.click());
    heroFileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileSelect(e.target.files[0]);
      }
    });

    // Dashboard Dropzone
    dashDropzone.addEventListener('click', () => dashFileInput.click());
    dashFileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileSelect(e.target.files[0]);
      }
    });

    // Drag and Drop
    [heroUploadCard, dashDropzone].forEach(dropArea => {
      ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropArea.classList.add('drag-active');
        });
      });

      ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropArea.classList.remove('drag-active');
        });
      });

      dropArea.addEventListener('drop', (e) => {
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
          handleFileSelect(e.dataTransfer.files[0]);
        }
      });
    });

    // Dashboard Quick Test Sample Pills
    samplePills.forEach(pill => {
      pill.addEventListener('click', () => {
        samplePills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');

        currentSampleId = pill.getAttribute('data-sample');
        currentFile = null;

        const sampleNames = {
          'poly_cotton_check': 'Check Pattern (Linen/Poly)',
          'denim_sample': 'Blue Denim (Indigo Twill)',
          'silk_sample': 'Emerald Silk (Satin Sheen)',
          'wool_knit_sample': 'Chunky Wool Knit'
        };

        dashFilenameLabel.textContent = sampleNames[currentSampleId] || 'Preset Sample';
        dashFileMeta.textContent = '800 × 800 • Preset Garment';
        dashPreviewImg.src = `/api/samples/${currentSampleId === 'poly_cotton_check' ? 'poly_cotton_check.jpeg' : currentSampleId + '.jpg'}`;

        runClassification();
      });
    });

    // Primary CTA Button
    dashClassifyBtn.addEventListener('click', runClassification);

    // Floating sample card on landing page click
    const floatSampleCard = document.getElementById('float-sample-card');
    if (floatSampleCard) {
      floatSampleCard.addEventListener('click', () => {
        currentSampleId = 'poly_cotton_check';
        currentFile = null;
        switchToDashboardAndClassify();
      });
    }
  }

  function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
      alert('Please upload a valid image file (JPEG, PNG, WebP).');
      return;
    }

    currentFile = file;
    currentSampleId = null;
    samplePills.forEach(p => p.classList.remove('active'));

    const reader = new FileReader();
    reader.onload = (e) => {
      dashPreviewImg.src = e.target.result;
      dashFilenameLabel.textContent = file.name;
      dashFileMeta.textContent = `${(file.size / 1024).toFixed(0)} KB • Custom Upload`;

      switchToDashboardAndClassify();
    };
    reader.readAsDataURL(file);
  }

  function switchToDashboardAndClassify() {
    landingView.classList.add('hidden');
    dashboardView.classList.remove('hidden');
    tabLanding.classList.remove('active');
    tabDashboard.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });

    runClassification();
  }

  // --------------------------------------------------------------------------
  // 5. Run Classification & Animated Pipeline
  // --------------------------------------------------------------------------
  async function runClassification() {
    if (!currentFile && !currentSampleId) return;

    // UI Loading state
    dashClassifyBtn.setAttribute('disabled', 'true');
    dashSpinner.classList.remove('hidden');
    dashClassifyLabel.textContent = 'Processing...';

    // Reset progress visualizer to 0% and animate
    spinnerPct.textContent = '10%';
    dynamicProgressFill.style.width = '10%';
    visualizerStepTitle.textContent = 'Ingesting Garment';
    visualizerStepDesc.textContent = 'Preprocessing image tensor and validating alpha channel borders...';

    const steps = [
      { pct: 35, title: '7-Patch Interior Crop', desc: 'Eroding zippers & edges; extracting 7 square interior texture crops.' },
      { pct: 65, title: 'EfficientNet-B0 Forward Pass', desc: 'Evaluating texture crops across 14 garment material heads on Apple Silicon.' },
      { pct: 90, title: 'Temperature Calibration', desc: 'Scaling logits (T=1.0) and computing Top-3 confidence metrics.' }
    ];

    let currentStep = 0;
    const progressInterval = setInterval(() => {
      if (currentStep < steps.length) {
        const s = steps[currentStep];
        spinnerPct.textContent = `${s.pct}%`;
        dynamicProgressFill.style.width = `${s.pct}%`;
        visualizerStepTitle.textContent = s.title;
        visualizerStepDesc.textContent = s.desc;
        currentStep++;
      }
    }, 280);

    try {
      let response;
      if (currentFile) {
        const formData = new FormData();
        formData.append('image', currentFile);
        response = await fetch('/api/predict', {
          method: 'POST',
          body: formData
        });
      } else if (currentSampleId) {
        response = await fetch('/api/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sample_id: currentSampleId })
        });
      }

      clearInterval(progressInterval);

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || `Server error: ${response.status}`);
      }

      const result = await response.json();
      latestResult = result;

      // Finish progress animation to 100%
      spinnerPct.textContent = '100%';
      dynamicProgressFill.style.width = '100%';
      visualizerStepTitle.textContent = 'Multi-Patch Analysis';
      visualizerStepDesc.textContent = 'Extracting 7 garment interior patches, eroding zippers/edges, and averaging softmax logits.';

      renderDashboardResults(result);

    } catch (err) {
      clearInterval(progressInterval);
      alert(`Classification error: ${err.message}`);
    } finally {
      dashClassifyBtn.removeAttribute('disabled');
      dashSpinner.classList.add('hidden');
      dashClassifyLabel.textContent = 'Classify Fabric Material';
    }
  }

  // --------------------------------------------------------------------------
  // 6. Render Dashboard Results & Staggered Animations
  // --------------------------------------------------------------------------
  function renderDashboardResults(data) {
    const pred = data.prediction;
    const profile = pred.profile;
    const metrics = data.metrics;

    // 1. Prediction Card
    predCategory.textContent = pred.category || 'Fabric Material';
    predName.textContent = pred.name.toUpperCase();
    predScore.textContent = `${pred.confidence.toFixed(2)}%`;
    predTagline.textContent = profile.tagline || profile.description || 'Quality garment fabric.';

    // 2. Top-3 Contenders
    contendersList.innerHTML = '';
    const fills = ['fill-1', 'fill-2', 'fill-3'];
    (data.top_3 || []).forEach((item, idx) => {
      const row = document.createElement('div');
      row.className = `contender-row rank-${idx + 1}`;
      row.innerHTML = `
        <div class="contender-header">
          <span class="contender-name"><span class="rank-dot"></span> ${item.name}</span>
          <span class="contender-rank">#${idx + 1}</span>
        </div>
        <div class="contender-bar-track">
          <div class="contender-bar-fill ${fills[idx] || 'fill-1'}" style="width: ${Math.min(100, item.confidence)}%"></div>
        </div>
        <span class="contender-score">${item.confidence.toFixed(2)}%</span>
      `;
      contendersList.appendChild(row);
    });

    // 3. 7-Patch Multi-Crop Slider
    renderPatchSlider(data.patches || []);

    // 4. Diagnostic Metrics
    diagTotalTime.innerHTML = `${metrics.total_latency_ms} <span class="unit">ms</span>`;
    diagModelTime.innerHTML = `${metrics.model_inference_ms} <span class="unit">ms</span>`;
    diagPatchTime.innerHTML = `${metrics.patch_extraction_ms} <span class="unit">ms</span>`;
    diagRamFootprint.innerHTML = `Apple Silicon <span class="unit">CPU</span>`;
    diagRamSub.textContent = `${metrics.device.split('(')[0].trim()} • ${metrics.ram_used_percent}% RAM`;

    // 5. JSON Inspector
    dashJsonCode.textContent = JSON.stringify(data, null, 2);
  }

  // --------------------------------------------------------------------------
  // 7. 7-Patch Multi-Crop Slider Carousel
  // --------------------------------------------------------------------------
  function initSlider() {
    sliderPrev.addEventListener('click', () => {
      if (currentSlideIndex > 0) {
        currentSlideIndex--;
        updateSliderPosition();
      }
    });

    sliderNext.addEventListener('click', () => {
      const totalPatches = sliderTrack.children.length;
      if (currentSlideIndex < totalPatches - patchesPerView) {
        currentSlideIndex++;
        updateSliderPosition();
      }
    });
  }

  function renderPatchSlider(patches) {
    sliderTrack.innerHTML = '';
    currentSlideIndex = 0;

    patches.forEach((p, idx) => {
      const item = document.createElement('div');
      item.className = 'slider-patch-item';
      item.title = `Patch #${p.patch_index} (Click to inspect)`;
      item.innerHTML = `
        <img src="${p.data_uri}" alt="Patch ${p.patch_index}" />
        <span class="slider-patch-badge">P${p.patch_index}</span>
      `;
      item.addEventListener('click', () => {
        dashPreviewImg.src = p.data_uri;
        dashFileMeta.textContent = `Patch #${p.patch_index} Crop (${p.width}×${p.height})`;
      });
      sliderTrack.appendChild(item);
    });

    updateSliderPosition();
  }

  function updateSliderPosition() {
    const itemWidth = sliderTrack.children[0] ? sliderTrack.children[0].offsetWidth + 14 : 134;
    sliderTrack.style.transform = `translateX(-${currentSlideIndex * itemWidth}px)`;

    // Update dots
    sliderDots.innerHTML = '';
    const totalDots = Math.max(1, sliderTrack.children.length - patchesPerView + 1);
    for (let i = 0; i < totalDots; i++) {
      const dot = document.createElement('span');
      dot.className = `slider-dot ${i === currentSlideIndex ? 'active' : ''}`;
      dot.addEventListener('click', () => {
        currentSlideIndex = i;
        updateSliderPosition();
      });
      sliderDots.appendChild(dot);
    }
  }

  // --------------------------------------------------------------------------
  // 8. JSON Accordion Drawer & Copy
  // --------------------------------------------------------------------------
  function initJsonAccordion() {
    jsonAccordionHeader.addEventListener('click', () => {
      const isOpen = jsonAccordionBody.classList.contains('open');
      if (isOpen) {
        jsonAccordionBody.classList.remove('open');
        accordionArrow.classList.remove('open');
      } else {
        jsonAccordionBody.classList.add('open');
        accordionArrow.classList.add('open');
      }
    });

    btnCopyJson.addEventListener('click', (e) => {
      e.stopPropagation();
      if (latestResult) {
        navigator.clipboard.writeText(JSON.stringify(latestResult, null, 2))
          .then(() => {
            btnCopyJson.textContent = 'Copied!';
            setTimeout(() => btnCopyJson.textContent = 'Copy JSON', 2000);
          })
          .catch(err => console.error('Copy failed:', err));
      }
    });
  }

  // --------------------------------------------------------------------------
  // 9. 14 Fabrics Catalog Modal
  // --------------------------------------------------------------------------
  function initCatalogModal() {
    btnCloseModal.addEventListener('click', () => catalogModal.classList.add('hidden'));
    catalogModal.addEventListener('click', (e) => {
      if (e.target === catalogModal) catalogModal.classList.add('hidden');
    });

    const floatCatalogCard = document.getElementById('float-catalog-card');
    if (floatCatalogCard) {
      floatCatalogCard.addEventListener('click', openCatalog);
    }
  }

  async function openCatalog() {
    catalogModal.classList.remove('hidden');
    if (catalogList.children.length === 0) {
      try {
        const res = await fetch('/api/classes');
        const data = await res.json();
        catalogList.innerHTML = '';
        (data.classes || []).forEach(c => {
          const item = document.createElement('div');
          item.className = 'catalog-item';
          item.innerHTML = `
            <div class="catalog-head">
              <span class="catalog-name">${c.name}</span>
              <span class="catalog-index">Class ${c.index}</span>
            </div>
            <div class="catalog-cat">${c.category}</div>
            <div class="catalog-tagline">${c.tagline}</div>
          `;
          catalogList.appendChild(item);
        });
      } catch (err) {
        catalogList.innerHTML = '<p>Failed to load classes catalogue.</p>';
      }
    }
  }

  // --------------------------------------------------------------------------
  // 10. System Health Check
  // --------------------------------------------------------------------------
  async function checkSystemHealth() {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        statusLabel.textContent = `EfficientNet-B0 Ready (${data.classes_count} classes)`;
      }
    } catch (err) {
      statusLabel.textContent = 'Connecting...';
    }
  }

  // Initial classification run on load to populate the dashboard state
  runClassification();
});
