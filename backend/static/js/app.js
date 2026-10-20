/**
 * TexClassifier AI — Frontend Application Logic
 * Modern vanilla JS • Drag & drop • Real-time inference & metrics
 */

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('file-input');
  const btnBrowse = document.getElementById('btn-browse');
  const dropzoneUnloaded = document.getElementById('dropzone-unloaded');
  const dropzoneLoaded = document.getElementById('dropzone-loaded');
  const previewImage = document.getElementById('preview-image');
  const previewMeta = document.getElementById('preview-meta');
  const btnChangeImage = document.getElementById('btn-change-image');
  const btnClassify = document.getElementById('btn-classify');
  const btnSpinner = document.getElementById('btn-spinner');
  const btnText = document.getElementById('btn-text');
  
  const statusLabel = document.getElementById('status-label');
  const deviceLabel = document.getElementById('device-label');
  const systemStatusPill = document.getElementById('system-status-pill');

  const idleState = document.getElementById('idle-state');
  const loadingState = document.getElementById('loading-state');
  const resultsContent = document.getElementById('results-content');
  const loadingStepText = document.getElementById('loading-step-text');

  // Winner card elements
  const winnerName = document.getElementById('winner-name');
  const winnerConfidence = document.getElementById('winner-confidence');
  const winnerCategory = document.getElementById('winner-category');
  const winnerTagline = document.getElementById('winner-tagline');
  const winnerDescription = document.getElementById('winner-description');
  const specBreathability = document.getElementById('spec-breathability');
  const specDurability = document.getElementById('spec-durability');
  const specStretch = document.getElementById('spec-stretch');
  const specTexture = document.getElementById('spec-texture');

  // Sections
  const podiumGrid = document.getElementById('podium-grid');
  const patchesGallery = document.getElementById('patches-gallery');
  const spectrumList = document.getElementById('spectrum-list');
  const careWashing = document.getElementById('care-washing');
  const careDrying = document.getElementById('care-drying');
  const careIroning = document.getElementById('care-ironing');
  const jsonContent = document.getElementById('json-content');
  const btnCopyJson = document.getElementById('btn-copy-json');

  // Metrics
  const metricTotalTime = document.getElementById('metric-total-time');
  const metricPatchTime = document.getElementById('metric-patch-time');
  const metricModelTime = document.getElementById('metric-model-time');
  const metricDeviceRam = document.getElementById('metric-device-ram');
  const metricDeviceSub = document.getElementById('metric-device-sub');

  // Modal
  const catalogModal = document.getElementById('catalog-modal');
  const btnOpenCatalog = document.getElementById('btn-open-catalog');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const catalogList = document.getElementById('catalog-list');

  // State
  let currentFile = null;
  let currentSampleId = null;
  let latestResult = null;

  // Initialize
  checkSystemHealth();
  setupDragAndDrop();
  setupSampleClickHandlers();
  setupCatalogModal();

  // --- Health Check ---
  async function checkSystemHealth() {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        statusLabel.textContent = `EfficientNet-B0 Online (${data.classes_count} classes)`;
        deviceLabel.textContent = data.system.device.split('(')[0].trim() || 'Mac (ARM64)';
      } else {
        statusLabel.textContent = 'Server starting...';
      }
    } catch (err) {
      statusLabel.textContent = 'Offline / Connecting...';
      console.warn('Health check error:', err);
    }
  }

  // --- Drag and Drop Handlers ---
  function setupDragAndDrop() {
    btnBrowse.addEventListener('click', () => fileInput.click());
    dropzone.addEventListener('click', (e) => {
      if (e.target !== btnChangeImage && !currentFile && !currentSampleId) {
        fileInput.click();
      }
    });

    fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileSelect(e.target.files[0]);
      }
    });

    btnChangeImage.addEventListener('click', (e) => {
      e.stopPropagation();
      fileInput.click();
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add('drag-active');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove('drag-active');
      });
    });

    dropzone.addEventListener('drop', (e) => {
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleFileSelect(e.dataTransfer.files[0]);
      }
    });

    btnClassify.addEventListener('click', runClassification);
  }

  function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
      alert('Please select a valid image file (JPEG, PNG, WebP).');
      return;
    }

    currentFile = file;
    currentSampleId = null;
    clearActiveSampleCards();

    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
      
      const img = new Image();
      img.onload = () => {
        previewMeta.textContent = `${img.width} × ${img.height} • ${(file.size / 1024).toFixed(0)} KB`;
      };
      img.src = e.target.result;

      dropzoneUnloaded.classList.add('hidden');
      dropzoneLoaded.classList.remove('hidden');
      btnClassify.removeAttribute('disabled');
    };
    reader.readAsDataURL(file);
  }

  // --- Sample Click Handlers ---
  function setupSampleClickHandlers() {
    const sampleCards = document.querySelectorAll('.sample-card');
    sampleCards.forEach(card => {
      card.addEventListener('click', () => {
        const sampleId = card.getAttribute('data-sample-id');
        currentSampleId = sampleId;
        currentFile = null;

        // Visual selection
        clearActiveSampleCards();
        card.classList.add('active');

        // Set preview
        const thumbImg = card.querySelector('img');
        if (thumbImg) {
          previewImage.src = thumbImg.src;
          previewMeta.textContent = `${card.querySelector('.sample-name').textContent} (Sample Preset)`;
          dropzoneUnloaded.classList.add('hidden');
          dropzoneLoaded.classList.remove('hidden');
        }

        btnClassify.removeAttribute('disabled');

        // Automatically trigger classification on sample click
        runClassification();
      });
    });
  }

  function clearActiveSampleCards() {
    document.querySelectorAll('.sample-card').forEach(c => c.classList.remove('active'));
  }

  // --- Run Classification ---
  async function runClassification() {
    if (!currentFile && !currentSampleId) return;

    // UI Loading state
    idleState.classList.add('hidden');
    resultsContent.classList.add('hidden');
    loadingState.classList.remove('hidden');

    btnClassify.setAttribute('disabled', 'true');
    btnSpinner.classList.remove('hidden');
    btnText.innerHTML = '<span>Processing...</span>';

    // Step animation text
    let stepCount = 0;
    const steps = [
      'Extracting 7 garment interior patches & eroding edges...',
      'Scaling texture crops to 224×224 resolution...',
      'Computing EfficientNet-B0 forward pass & multi-patch logits...',
      'Applying temperature calibration (T=1.0) & synthesizing metrics...'
    ];
    const stepInterval = setInterval(() => {
      stepCount = (stepCount + 1) % steps.length;
      loadingStepText.textContent = steps[stepCount];
    }, 450);

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

      clearInterval(stepInterval);

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || `Server returned ${response.status}`);
      }

      const result = await response.json();
      latestResult = result;
      renderResults(result);

    } catch (err) {
      clearInterval(stepInterval);
      alert(`Classification error: ${err.message}`);
      loadingState.classList.add('hidden');
      idleState.classList.remove('hidden');
    } finally {
      btnClassify.removeAttribute('disabled');
      btnSpinner.classList.add('hidden');
      btnText.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
        </svg>
        Re-classify Fabric Material
      `;
    }
  }

  // --- Render Results ---
  function renderResults(data) {
    loadingState.classList.add('hidden');
    resultsContent.classList.remove('hidden');

    const pred = data.prediction;
    const profile = pred.profile;
    const metrics = data.metrics;

    // 1. Winner Hero Card
    winnerName.textContent = pred.name;
    winnerConfidence.innerHTML = `${pred.confidence.toFixed(1)}<span class="pct">%</span>`;
    winnerCategory.textContent = pred.category;
    winnerTagline.textContent = pred.tagline;
    winnerDescription.textContent = profile.description || '';

    // Quick specs
    const props = profile.properties || {};
    specBreathability.textContent = props.breathability || 'Medium';
    specDurability.textContent = props.durability || 'High';
    specStretch.textContent = props.stretch || 'Low';
    specTexture.textContent = props.texture || 'Natural';

    // 2. Top-3 Podium
    podiumGrid.innerHTML = '';
    (data.top_3 || []).forEach((item, idx) => {
      const card = document.createElement('div');
      card.className = `podium-card ${idx === 0 ? 'rank-1' : ''}`;
      card.innerHTML = `
        <div class="podium-rank">#${idx + 1}</div>
        <div class="podium-name">${item.name}</div>
        <div class="podium-score">${item.confidence.toFixed(1)}%</div>
        <div class="podium-bar-track">
          <div class="podium-bar-fill" style="width: ${Math.min(100, item.confidence)}%"></div>
        </div>
      `;
      podiumGrid.appendChild(card);
    });

    // 3. Inference & Hardware Metrics
    metricTotalTime.innerHTML = `${metrics.total_latency_ms} <span class="metric-unit">ms</span>`;
    metricPatchTime.innerHTML = `${metrics.patch_extraction_ms} <span class="metric-unit">ms</span>`;
    metricModelTime.innerHTML = `${metrics.model_inference_ms} <span class="metric-unit">ms</span>`;
    metricDeviceRam.innerHTML = `CPU <span class="metric-unit">${metrics.ram_used_percent}% RAM</span>`;
    metricDeviceSub.textContent = `${metrics.device.split('(')[0].trim()} • ${metrics.patches_analyzed} Patches`;

    // 4. 7-Patch Inspector Gallery
    patchesGallery.innerHTML = '';
    (data.patches || []).forEach((p, idx) => {
      const patchEl = document.createElement('div');
      patchEl.className = 'patch-item';
      patchEl.title = `Patch #${p.patch_index} (Garment Interior)`;
      patchEl.innerHTML = `
        <img src="${p.data_uri}" alt="Patch ${p.patch_index}" />
        <span class="patch-label">P${p.patch_index}</span>
      `;
      // Click patch to preview full size in modal or alert
      patchEl.addEventListener('click', () => {
        previewImage.src = p.data_uri;
        previewMeta.textContent = `Patch #${p.patch_index} Crop (${p.width}×${p.height})`;
      });
      patchesGallery.appendChild(patchEl);
    });

    // 5. 14-Class Spectrum
    spectrumList.innerHTML = '';
    (data.all_classes || []).forEach(item => {
      const row = document.createElement('div');
      row.className = 'spectrum-row';
      row.innerHTML = `
        <span class="spectrum-rank">#${item.rank}</span>
        <span class="spectrum-name">${item.name}</span>
        <div class="spectrum-track">
          <div class="spectrum-fill" style="width: ${Math.max(1.5, Math.min(100, item.confidence))}%"></div>
        </div>
        <span class="spectrum-val">${item.confidence.toFixed(2)}%</span>
      `;
      spectrumList.appendChild(row);
    });

    // 6. Care Guide
    const care = profile.care || {};
    careWashing.textContent = care.washing || 'Follow garment care tag';
    careDrying.textContent = care.drying || 'Air dry recommended';
    careIroning.textContent = care.ironing || 'Low heat iron if required';

    // 7. Developer JSON Inspector
    jsonContent.textContent = JSON.stringify(data, null, 2);

    // Scroll slightly to results if on mobile
    if (window.innerWidth < 1080) {
      resultsContent.scrollIntoView({ behavior: 'smooth' });
    }
  }

  // --- Copy JSON Button ---
  btnCopyJson.addEventListener('click', (e) => {
    e.stopPropagation();
    if (latestResult) {
      navigator.clipboard.writeText(JSON.stringify(latestResult, null, 2))
        .then(() => {
          btnCopyJson.textContent = 'Copied!';
          setTimeout(() => btnCopyJson.textContent = 'Copy JSON', 2000);
        })
        .catch(err => console.error('Failed to copy JSON:', err));
    }
  });

  // --- 14 Classes Catalogue Modal ---
  async function setupCatalogModal() {
    btnOpenCatalog.addEventListener('click', async () => {
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
    });

    btnCloseModal.addEventListener('click', () => {
      catalogModal.classList.add('hidden');
    });

    catalogModal.addEventListener('click', (e) => {
      if (e.target === catalogModal) {
        catalogModal.classList.add('hidden');
      }
    });
  }
});
