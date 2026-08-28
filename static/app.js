// Stitching2D Client Application

let currentProjectId = null;
let currentProjectData = null;
let currentPieceId = null;
let currentZoom = 1.0;
let nestingDataCache = null;

// DOM Elements
const projectSelect = document.getElementById('projectSelect');
const unitBadge = document.getElementById('unitBadge');
const pieceCountBadge = document.getElementById('pieceCountBadge');
const fabricCountBadge = document.getElementById('fabricCountBadge');
const sidebarPieceCount = document.getElementById('sidebarPieceCount');
const pieceList = document.getElementById('pieceList');
const pieceInspector = document.getElementById('pieceInspector');
const activePieceTitle = document.getElementById('activePieceTitle');
const svgStage = document.getElementById('svgStage');
const zoomLevelText = document.getElementById('zoomLevelText');

// Toggles
const toggleCutLine = document.getElementById('toggleCutLine');
const toggleDimensions = document.getElementById('toggleDimensions');
const toggleGrainline = document.getElementById('toggleGrainline');
const toggleAttachments = document.getElementById('toggleAttachments');

// Tab Navigation
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initZoomControls();
  initLayerToggles();
  loadProjectList();
});

function initTabs() {
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      document.getElementById(targetId).classList.add('active');

      if (targetId === 'threeTab') {
        setTimeout(() => {
          init3DViewer();
          onWindowResize();
        }, 50);
      }
      if (targetId === 'nestingTab') loadNestingView();
      if (targetId === 'seamTab') loadSeamLogicView();
      if (targetId === 'bomTab') loadBOMView();
      if (targetId === 'notesTab') loadNotesView();
    });
  });
}

function initZoomControls() {
  document.getElementById('zoomInBtn').addEventListener('click', () => {
    currentZoom = Math.min(3.0, currentZoom + 0.2);
    applyZoom();
  });
  document.getElementById('zoomOutBtn').addEventListener('click', () => {
    currentZoom = Math.max(0.4, currentZoom - 0.2);
    applyZoom();
  });
  document.getElementById('resetZoomBtn').addEventListener('click', () => {
    currentZoom = 1.0;
    applyZoom();
  });
}

function applyZoom() {
  svgStage.style.transform = `scale(${currentZoom})`;
  zoomLevelText.textContent = `${Math.round(currentZoom * 100)}%`;
}

function initLayerToggles() {
  [toggleCutLine, toggleDimensions, toggleGrainline, toggleAttachments].forEach(chk => {
    chk.addEventListener('change', () => {
      if (currentPieceId) renderActivePieceSvg();
    });
  });
}

// Project Loading
async function loadProjectList() {
  try {
    const res = await fetch('/api/projects');
    const data = await res.json();
    projectSelect.innerHTML = '';

    data.projects.forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.id;
      opt.textContent = p.name;
      projectSelect.appendChild(opt);
    });

    if (data.projects.length > 0) {
      currentProjectId = data.projects[0].id;
      loadProject(currentProjectId);
    }

    projectSelect.addEventListener('change', (e) => {
      currentProjectId = e.target.value;
      loadProject(currentProjectId);
    });
  } catch (err) {
    console.error('Failed to load projects:', err);
  }
}

async function loadProject(projectId) {
  try {
    const res = await fetch(`/api/projects/${projectId}`);
    currentProjectData = await res.json();
    nestingDataCache = null;

    // Update Header Badges
    unitBadge.textContent = currentProjectData.units.toUpperCase();
    pieceCountBadge.textContent = `${currentProjectData.pieces.length} Pieces`;
    fabricCountBadge.textContent = `${currentProjectData.fabrics.length} Fabrics`;
    sidebarPieceCount.textContent = currentProjectData.pieces.length;

    renderPieceList();

    if (currentProjectData.pieces.length > 0) {
      selectPiece(currentProjectData.pieces[0].id);
    }

    if (is3DInitialized && typeof build3DModel === 'function') {
      build3DModel(currentProjectData);
    }
  } catch (err) {
    console.error('Failed to load project details:', err);
  }
}

function renderPieceList() {
  pieceList.innerHTML = '';
  currentProjectData.pieces.forEach(p => {
    const card = document.createElement('div');
    card.className = `piece-card ${p.id === currentPieceId ? 'active' : ''}`;
    card.dataset.pieceId = p.id;

    card.innerHTML = `
      <div class="piece-card-header">
        <span class="piece-card-title">${p.name}</span>
        <span class="piece-card-category">${p.category}</span>
      </div>
      <div class="piece-card-meta">
        <span>Qty: ${p.quantity}${p.mirror ? ' (Mirror)' : ''}</span>
        <span>SA: ${p.default_seam_allowance}"</span>
      </div>
    `;

    card.addEventListener('click', () => selectPiece(p.id));
    pieceList.appendChild(card);
  });
}

function selectPiece(pieceId) {
  currentPieceId = pieceId;
  document.querySelectorAll('.piece-card').forEach(c => {
    c.classList.toggle('active', c.dataset.pieceId === pieceId);
  });

  const piece = currentProjectData.pieces.find(p => p.id === pieceId);
  if (!piece) return;

  activePieceTitle.textContent = piece.name;
  renderPieceInspector(piece);
  renderActivePieceSvg();

  if (typeof highlight3DPiece === 'function') {
    highlight3DPiece(pieceId);
  }
}

function renderPieceInspector(piece) {
  const xs = piece.vertices.map(v => v.x);
  const ys = piece.vertices.map(v => v.y);
  const w = (Math.max(...xs) - Math.min(...xs)).toFixed(2);
  const h = (Math.max(...ys) - Math.min(...ys)).toFixed(2);

  pieceInspector.innerHTML = `
    <div class="inspector-row">
      <span class="inspector-label">Piece ID</span>
      <span class="inspector-value">${piece.id}</span>
    </div>
    <div class="inspector-row">
      <span class="inspector-label">Dimensions</span>
      <span class="inspector-value">${w}" × ${h}"</span>
    </div>
    <div class="inspector-row">
      <span class="inspector-label">Fabric Layer</span>
      <span class="inspector-value">${piece.fabric_id}</span>
    </div>
    <div class="inspector-row">
      <span class="inspector-label">Cut Quantity</span>
      <span class="inspector-value">${piece.quantity} ${piece.mirror ? '(1 + 1 Mirror)' : ''}</span>
    </div>
    <div class="inspector-row">
      <span class="inspector-label">Default Seam Allowance</span>
      <span class="inspector-value">${piece.default_seam_allowance}"</span>
    </div>
    <div class="inspector-row">
      <span class="inspector-label">Attachments</span>
      <span class="inspector-value">${piece.attachments ? piece.attachments.length : 0} items</span>
    </div>
  `;
}

async function renderActivePieceSvg() {
  if (!currentProjectId || !currentPieceId) return;

  const url = `/api/projects/${currentProjectId}/svg/${currentPieceId}` +
    `?show_cut_line=${toggleCutLine.checked}` +
    `&show_dimensions=${toggleDimensions.checked}` +
    `&show_grainline=${toggleGrainline.checked}` +
    `&show_attachments=${toggleAttachments.checked}`;

  try {
    const res = await fetch(url);
    const svgText = await res.text();
    svgStage.innerHTML = svgText;
  } catch (err) {
    console.error('Failed to load piece SVG:', err);
    svgStage.innerHTML = '<p class="error">Failed to load SVG vector.</p>';
  }
}

// Tab 2: Fabric Nesting
async function loadNestingView() {
  const container = document.getElementById('nestingCanvasContainer');
  const fabricSelect = document.getElementById('nestingFabricSelect');
  const statsContainer = document.getElementById('nestingStats');

  try {
    const res = await fetch(`/api/projects/${currentProjectId}/nesting?t=${Date.now()}`);
    nestingDataCache = await res.json();

    fabricSelect.innerHTML = '';
    const fabKeys = Object.keys(nestingDataCache);

    fabKeys.forEach(fabId => {
      const opt = document.createElement('option');
      opt.value = fabId;
      opt.textContent = nestingDataCache[fabId].fabric_name;
      fabricSelect.appendChild(opt);
    });

    const renderSelectedFabric = (fabId) => {
      const layout = nestingDataCache[fabId];
      if (!layout) return;

      statsContainer.innerHTML = `
        <span class="pill pill-units">Bolt: ${layout.bolt_width}"</span>
        <span class="pill pill-count">Cut Length: ${layout.total_cut_length_yards} yds (${layout.total_cut_length}")</span>
        <span class="pill pill-fabrics">Utilization: ${layout.utilization_rate_percent}%</span>
      `;
      container.innerHTML = layout.svg;
    };

    if (fabKeys.length > 0) {
      renderSelectedFabric(fabKeys[0]);
    }

    fabricSelect.onchange = (e) => renderSelectedFabric(e.target.value);
  } catch (err) {
    console.error('Failed to load nesting layout:', err);
  }
}

// Tab 3: Seam Logic
async function loadSeamLogicView() {
  const tableBody = document.getElementById('seamsTableBody');
  const headerCard = document.getElementById('seamHeaderCard');

  try {
    const res = await fetch(`/api/projects/${currentProjectId}/seams`);
    const data = await res.json();

    headerCard.innerHTML = `
      <div class="stat-item">
        <span class="stat-label">Total Seams</span>
        <span class="stat-val">${data.total_seams_checked}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Matched (ΔL ≤ 0.05")</span>
        <span class="stat-val" style="color: var(--accent-green)">${data.matched_seams}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Eased (1-8%)</span>
        <span class="stat-val" style="color: var(--accent-amber)">${data.eased_seams}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Mismatches</span>
        <span class="stat-val" style="color: var(--accent-red)">${data.mismatches}</span>
      </div>
    `;

    tableBody.innerHTML = '';
    data.results.forEach(r => {
      const badgeClass = r.status === 'MATCH' ? 'badge-match' : (r.status === 'EASED' ? 'badge-eased' : 'badge-mismatch');
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><span class="${badgeClass}">${r.status}</span></td>
        <td><strong>${r.source_piece_name}</strong><br><code style="font-size: 10px; color: #64748b;">${r.source_edge_id}</code></td>
        <td><strong>${r.target_piece_name}</strong><br><code style="font-size: 10px; color: #64748b;">${r.target_edge_id}</code></td>
        <td>${r.source_length}"</td>
        <td>${r.target_length}"</td>
        <td>${r.length_delta}"</td>
        <td>${r.ease_ratio_percent > 0 ? '+' : ''}${r.ease_ratio_percent}%</td>
        <td>${r.seam_allowance_compatible ? '<span style="color: #16a34a; font-weight: 600;">✅ Match</span>' : '<span style="color: #d97706; font-weight: 600;" title="Different SA (e.g. hem or trim join)">⚠️ Trim/Enclosed</span>'}</td>
      `;
      tableBody.appendChild(tr);
    });

    if (data.results.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #94a3b8; padding: 20px;">No paired edges explicitly configured in this project.</td></tr>';
    }
  } catch (err) {
    console.error('Failed to load seam report:', err);
  }
}

// Tab 4: BOM
async function loadBOMView() {
  const content = document.getElementById('bomContent');
  try {
    const res = await fetch(`/api/projects/${currentProjectId}/bom`);
    const bom = await res.json();

    content.innerHTML = `
      <div class="bom-card">
        <h3>🧵 Fabric Requirements</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>Fabric Name</th>
              <th>Roll Width</th>
              <th>Exact Length</th>
              <th>Recommended (+10% buffer)</th>
              <th>Est. Cost</th>
            </tr>
          </thead>
          <tbody>
            ${bom.fabrics.map(f => `
              <tr>
                <td><strong>${f.fabric_name}</strong></td>
                <td>${f.bolt_width}"</td>
                <td>${f.yardage_exact} yds (${f.cut_length_inches}")</td>
                <td><strong style="color: var(--accent-blue)">${f.yardage_recommended_10pct_waste} yds</strong></td>
                <td>${f.estimated_cost ? `$${f.estimated_cost.toFixed(2)}` : '—'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>

      <div class="bom-card">
        <h3>📏 Webbing, Zippers & Linear Materials</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>Material</th>
              <th>Type</th>
              <th>Width</th>
              <th>Total Length (in)</th>
              <th>Total Length (ft)</th>
              <th>Piece Count</th>
            </tr>
          </thead>
          <tbody>
            ${bom.linear_materials.length > 0 ? bom.linear_materials.map(m => `
              <tr>
                <td><strong>${m.name}</strong></td>
                <td><code>${m.type}</code></td>
                <td>${m.width ? `${m.width}"` : '—'}</td>
                <td>${m.total_length_inches}"</td>
                <td>${m.total_length_feet} ft</td>
                <td>${m.pieces_count}</td>
              </tr>
            `).join('') : '<tr><td colspan="6" style="text-align:center; color:#94a3b8;">No linear attachments</td></tr>'}
          </tbody>
        </table>
      </div>

      <div class="bom-card">
        <h3>🔩 Hardware & Fasteners</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>Item</th>
              <th>Type</th>
              <th>Quantity</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            ${bom.hardware.map(h => `
              <tr>
                <td><strong>${h.name}</strong></td>
                <td>${h.type}</td>
                <td><strong>${h.quantity}</strong></td>
                <td>${h.notes || '—'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>

      <div class="bom-card">
        <h3>🪡 Seam & Thread Consumption Summary</h3>
        <div style="display: flex; gap: 32px; margin-top: 8px;">
          <div class="stat-item">
            <span class="stat-label">Total Seam Perimeter</span>
            <span class="stat-val">${bom.total_seam_length_inches}" (${(bom.total_seam_length_inches/36).toFixed(1)} yds)</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Est. Thread Consumption (ISO 301)</span>
            <span class="stat-val" style="color: var(--accent-indigo)">${bom.estimated_thread_consumption_yards} yds</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Total Cut Pieces</span>
            <span class="stat-val">${bom.total_pieces_to_cut} panels</span>
          </div>
        </div>
      </div>
    `;
  } catch (err) {
    console.error('Failed to load BOM:', err);
  }
}

// Tab 5: Notes
function loadNotesView() {
  const container = document.getElementById('notesContent');
  if (!currentProjectData || !currentProjectData.sewing_notes) {
    container.innerHTML = '<p>No construction notes provided.</p>';
    return;
  }

  container.innerHTML = currentProjectData.sewing_notes.map((note, idx) => `
    <div class="note-card">
      <strong>Step ${idx + 1}</strong>
      <p style="margin-top: 4px; color: var(--text-secondary);">${note}</p>
    </div>
  `).join('');
}
