/**
 * EcoVision Frontend Controller (V & client interaction)
 * Handles webcam stream, image uploading, sample selection, and rendering model output.
 */

let selectedFile = null;
let webcamStream = null;
let totalCo2Saved = 0.0;

// Setup event listeners on DOM load
document.addEventListener("DOMContentLoaded", () => {
  setupDropZone();
  loadRecentHistory();
});

// Tab Switcher
function switchTab(tabId) {
  document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(pnl => pnl.classList.remove("active"));

  const targetBtn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
  const targetPnl = document.getElementById(`tab-${tabId}`);

  if (targetBtn) targetBtn.classList.add("active");
  if (targetPnl) targetPnl.classList.add("active");

  // Stop camera if moving away from webcam tab
  if (tabId !== "webcam" && webcamStream) {
    stopWebcam();
  }
}

// Drag & Drop Handling
function setupDropZone() {
  const dropZone = document.getElementById("dropZone");
  if (!dropZone) return;

  ['dragenter', 'dragover'].forEach(name => {
    dropZone.addEventListener(name, (e) => {
      e.preventDefault();
      dropZone.classList.add("dragover");
    });
  });

  ['dragleave', 'drop'].forEach(name => {
    dropZone.addEventListener(name, (e) => {
      e.preventDefault();
      dropZone.classList.remove("dragover");
    });
  });

  dropZone.addEventListener("drop", (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      processSelectedFile(files[0]);
    }
  });
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    processSelectedFile(file);
  }
}

function processSelectedFile(file) {
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    const preview = document.getElementById("imagePreview");
    const dropContent = document.getElementById("dropContent");
    preview.src = e.target.result;
    preview.style.display = "block";
    dropContent.style.display = "none";

    const btn = document.getElementById("btnUploadClassify");
    btn.disabled = false;
    btn.innerText = `🔍 Classify "${file.name}"`;
  };
  reader.readAsDataURL(file);
}

// Upload & Classify
async function classifyUploadedFile() {
  if (!selectedFile) return;

  setAnalyzingState(true);
  const formData = new FormData();
  formData.append("image", selectedFile);

  try {
    const response = await fetch("/api/classify", {
      method: "POST",
      body: formData
    });
    const result = await response.json();
    if (result.status === "success") {
      renderPrediction(result.data, result.stats);
    } else {
      alert("Classification Error: " + (result.message || result.error));
    }
  } catch (err) {
    alert("Connection Error: " + err.message);
  } finally {
    setAnalyzingState(false);
  }
}

// Webcam Integration
async function startWebcam() {
  const video = document.getElementById("webcamVideo");
  const placeholder = document.getElementById("webcamPlaceholder");
  const btnCapture = document.getElementById("btnCapture");
  const btnStop = document.getElementById("btnStopCam");

  try {
    webcamStream = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: "environment" }
    });
    video.srcObject = webcamStream;
    video.style.display = "block";
    placeholder.style.display = "none";
    btnCapture.style.display = "inline-block";
    btnStop.style.display = "inline-block";
  } catch (err) {
    alert("Unable to access camera: " + err.message + "\nPlease verify browser permissions.");
  }
}

function stopWebcam() {
  if (webcamStream) {
    webcamStream.getTracks().forEach(track => track.stop());
    webcamStream = null;
  }
  const video = document.getElementById("webcamVideo");
  const placeholder = document.getElementById("webcamPlaceholder");
  const btnCapture = document.getElementById("btnCapture");
  const btnStop = document.getElementById("btnStopCam");

  video.style.display = "none";
  placeholder.style.display = "block";
  btnCapture.style.display = "none";
  btnStop.style.display = "none";
}

async function captureAndClassify() {
  const video = document.getElementById("webcamVideo");
  const canvas = document.getElementById("snapshotCanvas");
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const base64Data = canvas.toDataURL("image/jpeg", 0.90);

  setAnalyzingState(true);

  try {
    const response = await fetch("/api/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_base64: base64Data })
    });
    const result = await response.json();
    if (result.status === "success") {
      renderPrediction(result.data, result.stats);
    } else {
      alert("Classification Error: " + (result.message || result.error));
    }
  } catch (err) {
    alert("Inference Error: " + err.message);
  } finally {
    setAnalyzingState(false);
  }
}

// Quick Sample Testing
async function testSample(category) {
  setAnalyzingState(true);
  try {
    const response = await fetch("/api/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sample_path: `${category}/${category}_sample.jpg` })
    });
    const result = await response.json();
    if (result.status === "success") {
      renderPrediction(result.data, result.stats);
    } else {
      alert("Sample test failed: " + (result.message || result.error));
    }
  } catch (err) {
    alert("Sample fetch error: " + err.message);
  } finally {
    setAnalyzingState(false);
  }
}

// Render Results
function renderPrediction(data, stats) {
  document.getElementById("resultEmpty").style.display = "none";
  document.getElementById("resultContent").style.display = "block";

  // Category and confidence
  document.getElementById("resEmoji").innerText = data.emoji || "♻️";
  document.getElementById("resCategory").innerText = data.category_name;
  document.getElementById("resConfidence").innerText = `${data.confidence}%`;

  // Smart Bin Guidance
  const binAlert = document.getElementById("binAlert");
  const binIndicator = document.getElementById("binIndicator");
  const binName = document.getElementById("binName");
  const binInstructions = document.getElementById("binInstructions");

  binIndicator.style.backgroundColor = data.bin_color || "#2563EB";
  binName.innerText = data.bin_name;
  binInstructions.innerText = data.instructions;

  if (data.category === "human") {
    binAlert.classList.add("human-alert");
  } else {
    binAlert.classList.remove("human-alert");
  }

  // Impact metrics
  document.getElementById("resRecyclable").innerText = data.disposal_type;
  document.getElementById("resCo2").innerText = `${data.co2_saved_kg} kg CO₂ / kg`;
  document.getElementById("resDecomp").innerText = data.decomposition_time;

  // Cumulative CO2 KPI
  totalCo2Saved += Number(data.co2_saved_kg || 0);
  document.getElementById("kpi-co2").innerText = `${totalCo2Saved.toFixed(2)} kg`;
  document.getElementById("kpi-latency").innerText = `${data.inference_time_ms} ms`;

  if (stats && stats.total_scanned !== undefined) {
    document.getElementById("kpi-total").innerText = stats.total_scanned;
  }

  // Class Probabilities breakdown
  const probList = document.getElementById("probList");
  probList.innerHTML = "";

  const entries = Object.entries(data.probabilities || {}).sort((a, b) => b[1] - a[1]);
  entries.forEach(([cat, pct]) => {
    const isTop = cat === data.category;
    const item = document.createElement("div");
    item.className = "prob-item";
    item.innerHTML = `
      <div class="prob-meta">
        <span style="text-transform: capitalize; ${isTop ? 'font-weight:700; color:#0f172a;' : 'color:#64748b;'}">${cat}</span>
        <span style="${isTop ? 'font-weight:700; color:#059669;' : 'color:#64748b;'}">${pct}%</span>
      </div>
      <div class="prob-track">
        <div class="prob-fill" style="width: ${pct}%; background-color: ${isTop ? (data.bin_color || '#10b981') : '#94a3b8'};"></div>
      </div>
    `;
    probList.appendChild(item);
  });

  loadRecentHistory();
}

// UI State Controller
function setAnalyzingState(isAnalyzing) {
  const badge = document.getElementById("analysisBadge");
  if (isAnalyzing) {
    badge.className = "status-chip success";
    badge.innerText = "⏳ Processing Frame...";
  } else {
    badge.className = "status-chip idle";
    badge.innerText = "✅ Analysis Complete";
  }
}

// Load Recent History Table
async function loadRecentHistory() {
  try {
    const res = await fetch("/api/history");
    const json = await res.json();
    if (json.status === "success" && json.history) {
      const tbody = document.getElementById("historyTableBody");
      if (json.history.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="table-empty">No classification records logged yet.</td></tr>';
        return;
      }
      tbody.innerHTML = json.history.map(item => `
        <tr>
          <td><code style="font-size:0.78rem;">${item.timestamp}</code></td>
          <td><strong>${item.category_name}</strong></td>
          <td><span style="color:#059669; font-weight:600;">${item.confidence}%</span></td>
          <td><span style="text-transform: capitalize; background:#f1f5f9; padding:2px 6px; border-radius:4px; font-size:0.75rem;">${item.source}</span></td>
          <td><span style="font-size:0.8rem; color:#475569;">${item.category === 'organic' ? 'Compost' : 'Recycle'}</span></td>
        </tr>
      `).join("");
    }
  } catch (err) {
    console.error("Failed to fetch history:", err);
  }
}

// Modal functions
function openArchModal() {
  document.getElementById("archModal").style.display = "flex";
}

function closeArchModal(event) {
  if (!event || event.target.id === "archModal" || event.target.className === "modal-close") {
    document.getElementById("archModal").style.display = "none";
  }
}

