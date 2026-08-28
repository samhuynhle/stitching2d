// Stitching2D Three.js Interactive 3D Product Preview Engine
// Features cross-linked 2D-to-3D interactive piece glowing & highlight synchronization

let scene, camera, renderer, controls;
let current3DModelGroup = null;
let is3DInitialized = false;
let animationFrameId = null;

// State
let openAmount = 1.0; // 1.0 = fully open, 0.0 = magnetic snapped shut
let isXRayMode = false;
let isWireframe = false;
let activeLayer = "all"; // "all", "exterior", "baffles", "lining"
let highlightedPieceId = null;

function init3DViewer() {
  const container = document.getElementById('threeCanvasContainer');
  if (!container || is3DInitialized) return;

  // 1. Scene setup
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf1f5f9);

  // 2. Camera setup
  const width = container.clientWidth || 800;
  const height = container.clientHeight || 550;
  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.set(22, 18, 26);

  // 3. Renderer setup
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  // 4. OrbitControls
  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.maxPolarAngle = Math.PI / 2 + 0.1;
  controls.target.set(0, 5, 0);

  // 5. Lighting
  setupLights();

  // 6. Ground Studio Grid & Floor
  setupGround();

  // 7. Event listeners
  window.addEventListener('resize', onWindowResize);
  setup3DControls();

  is3DInitialized = true;
  animate();

  if (currentProjectData) {
    build3DModel(currentProjectData);
    if (currentPieceId) highlight3DPiece(currentPieceId);
  }
}

function setupLights() {
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
  scene.add(ambientLight);

  const mainLight = new THREE.DirectionalLight(0xfff5ea, 1.2);
  mainLight.position.set(20, 35, 25);
  mainLight.castShadow = true;
  mainLight.shadow.mapSize.width = 2048;
  mainLight.shadow.mapSize.height = 2048;
  mainLight.shadow.bias = -0.0001;
  scene.add(mainLight);

  const fillLight = new THREE.DirectionalLight(0xe0f2fe, 0.6);
  fillLight.position.set(-20, 20, -20);
  scene.add(fillLight);

  const bottomBounce = new THREE.DirectionalLight(0xffffff, 0.3);
  bottomBounce.position.set(0, -10, 0);
  scene.add(bottomBounce);
}

function setupGround() {
  const floorGeo = new THREE.PlaneGeometry(80, 80);
  const floorMat = new THREE.MeshStandardMaterial({
    color: 0xe2e8f0,
    roughness: 0.9,
    metalness: 0.1,
  });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.05;
  floor.receiveShadow = true;
  scene.add(floor);

  const grid = new THREE.GridHelper(60, 30, 0x94a3b8, 0xcbd5e1);
  grid.position.y = 0.0;
  scene.add(grid);
}

function onWindowResize() {
  const container = document.getElementById('threeCanvasContainer');
  if (!container || !renderer || !camera) return;
  const width = container.clientWidth;
  const height = container.clientHeight;
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
}

function setup3DControls() {
  const snapSlider = document.getElementById('snapSlider');
  if (snapSlider) {
    snapSlider.addEventListener('input', (e) => {
      openAmount = parseFloat(e.target.value);
      if (currentProjectData) build3DModel(currentProjectData);
    });
  }

  const xrayBtn = document.getElementById('toggleXrayBtn');
  if (xrayBtn) {
    xrayBtn.addEventListener('click', () => {
      isXRayMode = !isXRayMode;
      xrayBtn.classList.toggle('active', isXRayMode);
      if (currentProjectData) build3DModel(currentProjectData);
    });
  }

  const wireframeBtn = document.getElementById('toggleWireframeBtn');
  if (wireframeBtn) {
    wireframeBtn.addEventListener('click', () => {
      isWireframe = !isWireframe;
      wireframeBtn.classList.toggle('active', isWireframe);
      if (currentProjectData) build3DModel(currentProjectData);
    });
  }

  const layerSelect = document.getElementById('layerViewSelect');
  if (layerSelect) {
    layerSelect.addEventListener('change', (e) => {
      activeLayer = e.target.value;
      if (currentProjectData) build3DModel(currentProjectData);
    });
  }
}

// Cross-Linked 2D -> 3D Glowing Highlight Controller
function highlight3DPiece(pieceId) {
  highlightedPieceId = pieceId;
  if (!current3DModelGroup) return;

  const isInteriorPiece = pieceId && (pieceId.includes('fleece') || pieceId.includes('baffle') || pieceId.includes('lining'));

  current3DModelGroup.traverse(child => {
    if (child.isMesh && child.userData && child.userData.pieceId) {
      const isMatch = child.userData.pieceId === pieceId || (Array.isArray(child.userData.pieceId) && child.userData.pieceId.includes(pieceId));
      
      if (child.material) {
        if (isMatch) {
          child.material.emissive = new THREE.Color(0x06b6d4); // Vivid Cyan Glow
          child.material.emissiveIntensity = 0.85;
          if (child.material.transparent) child.material.opacity = 1.0;
        } else {
          child.material.emissive = new THREE.Color(0x000000);
          child.material.emissiveIntensity = 0.0;
          
          // If viewing an interior piece, ghost the exterior shell
          if (isInteriorPiece && child.userData.pieceId === 'ext_u_panel') {
            child.material.transparent = true;
            child.material.opacity = 0.25;
          } else if (!isXRayMode) {
            child.material.transparent = false;
            child.material.opacity = 1.0;
          }
        }
      }
    }
  });
}

// Procedural 3D Mesh Generator based on Project Pattern Specification
function build3DModel(project) {
  if (!scene) return;

  if (current3DModelGroup) {
    scene.remove(current3DModelGroup);
    current3DModelGroup.traverse(child => {
      if (child.geometry) child.geometry.dispose();
      if (child.material) {
        if (Array.isArray(child.material)) child.material.forEach(m => m.dispose());
        else child.material.dispose();
      }
    });
  }

  current3DModelGroup = new THREE.Group();

  if (project.id.includes("chalk_bucket") || project.id.includes("chalk_bag")) {
    buildChalkBucket3D(project, current3DModelGroup);
  } else {
    buildGenericPouch3D(project, current3DModelGroup);
  }

  scene.add(current3DModelGroup);

  if (highlightedPieceId) {
    highlight3DPiece(highlightedPieceId);
  }
}

function buildChalkBucket3D(project, group) {
  // Dimensions
  const baseW = 10.5;
  const baseD = 8.0;
  const topW = 8.5;
  const currentTopD = 0.2 + (5.8 * openAmount);
  const height = 11.0;

  const halfBW = baseW / 2;
  const halfBD = baseD / 2;
  const halfTW = topW / 2;
  const halfTD = currentTopD / 2;

  // Material helpers (creates individual instances so pieces can glow independently)
  function createCorduraMat() {
    return new THREE.MeshStandardMaterial({
      color: 0x1e293b,
      roughness: 0.85,
      metalness: 0.1,
      wireframe: isWireframe,
      transparent: isXRayMode,
      opacity: isXRayMode ? 0.35 : 1.0,
      side: THREE.DoubleSide
    });
  }

  const ultrasuedeMat = new THREE.MeshStandardMaterial({
    color: 0x0f766e,
    roughness: 0.95,
    metalness: 0.05,
    wireframe: isWireframe,
    side: THREE.DoubleSide
  });

  const fleeceMat = new THREE.MeshStandardMaterial({
    color: 0xf8fafc,
    roughness: 0.98,
    metalness: 0.0,
    wireframe: isWireframe,
    side: THREE.DoubleSide
  });

  const webbingMat = new THREE.MeshStandardMaterial({
    color: 0xd97706,
    roughness: 0.7,
    metalness: 0.2
  });

  const magnetMat = new THREE.MeshStandardMaterial({
    color: 0xe2e8f0,
    roughness: 0.2,
    metalness: 0.9
  });

  const xpacMat = new THREE.MeshStandardMaterial({
    color: 0x0284c7,
    roughness: 0.6,
    metalness: 0.2
  });

  const meshPocketMat = new THREE.MeshStandardMaterial({
    color: 0x334155,
    roughness: 0.9,
    metalness: 0.1,
    wireframe: true,
    side: THREE.DoubleSide
  });

  const dRingMat = new THREE.MeshStandardMaterial({
    color: 0x111827,
    roughness: 0.3,
    metalness: 0.8
  });

  // 1. EXTERIOR CONTINUOUS U-PANEL (Front, Base, Back faces)
  if (activeLayer === "all" || activeLayer === "exterior") {
    // U-Panel: Base + Front Wall + Back Wall
    const uPanelGeo = new THREE.BufferGeometry();
    const uVertices = new Float32Array([
      // Bottom Base (0, 1, 2, 3)
      -halfBW, 0, -halfBD,   halfBW, 0, -halfBD,   halfBW, 0, halfBD,   -halfBW, 0, halfBD,
      // Front Wall Top (4, 5)
      halfTW, height, halfTD,   -halfTW, height, halfTD,
      // Back Wall Top (6, 7)
      -halfTW, height, -halfTD,   halfTW, height, -halfTD
    ]);

    const uIndices = [
      // Base
      0, 2, 1,   0, 3, 2,
      // Front Wall (3, 2, 4, 5)
      3, 4, 2,   3, 5, 4,
      // Back Wall (1, 0, 6, 7)
      1, 6, 0,   1, 7, 6
    ];

    uPanelGeo.setAttribute('position', new THREE.BufferAttribute(uVertices, 3));
    uPanelGeo.setIndex(uIndices);
    uPanelGeo.computeVertexNormals();

    const uPanelMesh = new THREE.Mesh(uPanelGeo, createCorduraMat());
    uPanelMesh.userData = { pieceId: "ext_u_panel" };
    uPanelMesh.castShadow = true;
    uPanelMesh.receiveShadow = true;
    group.add(uPanelMesh);

    // 2. EXTERIOR LEFT SIDE GUSSET
    const leftGussetGeo = new THREE.BufferGeometry();
    const leftVerts = new Float32Array([
      -halfBW, 0, -halfBD,   -halfBW, 0, halfBD,   -halfTW, height, halfTD,   -halfTW, height, -halfTD
    ]);
    leftGussetGeo.setAttribute('position', new THREE.BufferAttribute(leftVerts, 3));
    leftGussetGeo.setIndex([0, 2, 1,   0, 3, 2]);
    leftGussetGeo.computeVertexNormals();

    const leftGussetMesh = new THREE.Mesh(leftGussetGeo, createCorduraMat());
    leftGussetMesh.userData = { pieceId: "ext_side_gusset_left" };
    leftGussetMesh.castShadow = true;
    group.add(leftGussetMesh);

    // 3. EXTERIOR RIGHT SIDE GUSSET
    const rightGussetGeo = new THREE.BufferGeometry();
    const rightVerts = new Float32Array([
      halfBW, 0, halfBD,   halfBW, 0, -halfBD,   halfTW, height, -halfTD,   halfTW, height, halfTD
    ]);
    rightGussetGeo.setAttribute('position', new THREE.BufferAttribute(rightVerts, 3));
    rightGussetGeo.setIndex([0, 2, 1,   0, 3, 2]);
    rightGussetGeo.computeVertexNormals();

    const rightGussetMesh = new THREE.Mesh(rightGussetGeo, createCorduraMat());
    rightGussetMesh.userData = { pieceId: "ext_side_gusset_right" };
    rightGussetMesh.castShadow = true;
    group.add(rightGussetMesh);

    // 4. ULTRASUEDE TOP RIM GASKET COLLAR
    const collarH = 1.25;
    const collarFrontGeo = new THREE.BoxGeometry(topW, collarH, 0.15);
    const collarFront = new THREE.Mesh(collarFrontGeo, ultrasuedeMat.clone());
    collarFront.position.set(0, height - collarH/2, halfTD + 0.05);
    collarFront.userData = { pieceId: "ultrasuede_rim_gasket" };
    group.add(collarFront);

    const collarBack = new THREE.Mesh(collarFrontGeo, ultrasuedeMat.clone());
    collarBack.position.set(0, height - collarH/2, -halfTD - 0.05);
    collarBack.userData = { pieceId: "ultrasuede_rim_gasket" };
    group.add(collarBack);

    // Embedded N52 Magnets
    const magSpacing = 2.0;
    for (let i = -1.5; i <= 1.5; i += 1.0) {
      const magGeo = new THREE.CylinderGeometry(0.35, 0.35, 0.12, 16);
      magGeo.rotateX(Math.PI / 2);
      const magFront = new THREE.Mesh(magGeo, magnetMat);
      magFront.position.set(i * magSpacing, height - 0.65, halfTD + 0.08);
      group.add(magFront);

      const magBack = magFront.clone();
      magBack.position.set(i * magSpacing, height - 0.65, -halfTD - 0.08);
      group.add(magBack);
    }

    // Grab Handles & Pull Tabs
    // Calculate exact tapered wall depth at handle height (y = height - 2.5)
    const handleY = height - 2.5;
    const wallZAtHandle = halfBD + (halfTD - halfBD) * (handleY / height);

    const handleGeo = new THREE.TorusGeometry(1.5, 0.18, 8, 24, Math.PI);
    
    // Front Grab Handle (Arches outwards toward +Z)
    const handleFront = new THREE.Mesh(handleGeo, webbingMat);
    handleFront.position.set(0, handleY, wallZAtHandle + 0.1);
    handleFront.rotation.set(Math.PI / 2, 0, 0);
    handleFront.userData = { pieceId: "ext_u_panel" };
    group.add(handleFront);

    // Rear Grab Handle (Arches outwards toward -Z)
    const handleBack = new THREE.Mesh(handleGeo, webbingMat);
    handleBack.position.set(0, handleY, -wallZAtHandle - 0.1);
    handleBack.rotation.set(-Math.PI / 2, 0, 0);
    handleBack.userData = { pieceId: "ext_u_panel" };
    group.add(handleBack);

    // Pull Tabs at Mouth Rim
    const tabGeo = new THREE.BoxGeometry(0.75, 0.8, 0.1);
    const tabFront = new THREE.Mesh(tabGeo, webbingMat);
    tabFront.position.set(0, height + 0.3, halfTD + 0.05);
    tabFront.userData = { pieceId: "ext_u_panel" };
    group.add(tabFront);

    const tabBack = new THREE.Mesh(tabGeo, webbingMat);
    tabBack.position.set(0, height + 0.3, -halfTD - 0.05);
    tabBack.userData = { pieceId: "ext_u_panel" };
    group.add(tabBack);

    // Rear Roll-Top Compression Webbing Strap (Running down back face)
    const strapGeo = new THREE.BoxGeometry(0.8, 7.5, 0.12);
    const strapMesh = new THREE.Mesh(strapGeo, webbingMat);
    strapMesh.position.set(0, 6.5, -halfBD + 0.25);
    strapMesh.rotation.x = 0.08;
    strapMesh.userData = { pieceId: "ext_u_panel" };
    group.add(strapMesh);

    // 5. FRONT 3D MAGNETIC POCKET (X-Pac VX21) — ELEVATED
    const pW = 7.5;
    const pH = 4.2;
    const pD = 1.0;
    const pocketGeo = new THREE.BoxGeometry(pW, pH, pD);
    const pocketMesh = new THREE.Mesh(pocketGeo, xpacMat.clone());
    pocketMesh.position.set(0, 5.8, halfBD - 0.25);
    pocketMesh.userData = { pieceId: "front_3d_pocket" };
    pocketMesh.castShadow = true;
    group.add(pocketMesh);

    // Pocket Flap (Elevated)
    const flapGeo = new THREE.BoxGeometry(pW + 0.2, 1.2, pD + 0.15);
    const flapMesh = new THREE.Mesh(flapGeo, xpacMat.clone());
    flapMesh.position.set(0, 7.8, halfBD - 0.2);
    flapMesh.userData = { pieceId: "front_pocket_flap" };
    group.add(flapMesh);

    // 6. FRONT 2-INCH UPWARD-FOLDING MAGNETIC BOTTOM STASH FLAP & ELASTIC HINGE
    const bFlapGeo = new THREE.BoxGeometry(baseW, 2.1, 0.18);
    const bFlapMesh = new THREE.Mesh(bFlapGeo, createCorduraMat());
    bFlapMesh.position.set(0, 1.05, halfBD + 0.08);
    bFlapMesh.userData = { pieceId: "basement_floor_panel" };
    group.add(bFlapMesh);

    // 1in Elastic Snap-Back Hinge Indicator (bottom crease)
    const bHingeGeo = new THREE.BoxGeometry(8.0, 0.3, 0.05);
    const bHingeMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.8 });
    const bHingeMesh = new THREE.Mesh(bHingeGeo, bHingeMat);
    bHingeMesh.position.set(0, 0.15, halfBD + 0.15);
    bHingeMesh.userData = { pieceId: "basement_floor_panel" };
    group.add(bHingeMesh);

    // 3x N52 Basement Magnets on 2in Flap Top Hem
    for (let xPos of [-3.5, 0.0, 3.5]) {
      const bMagGeo = new THREE.CylinderGeometry(0.3, 0.3, 0.1, 16);
      bMagGeo.rotateX(Math.PI / 2);
      const bMag = new THREE.Mesh(bMagGeo, magnetMat);
      bMag.position.set(xPos, 1.65, halfBD + 0.18);
      bMag.userData = { pieceId: "basement_floor_panel" };
      group.add(bMag);
    }

    // Center Low-Profile Travel Lock Snap Button (Matte Black Gunmetal)
    const snapGeo = new THREE.CylinderGeometry(0.4, 0.4, 0.15, 16);
    snapGeo.rotateX(Math.PI / 2);
    const snapMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.9, roughness: 0.3 });
    const snapMesh = new THREE.Mesh(snapGeo, snapMat);
    snapMesh.position.set(0, 1.65, halfBD + 0.22);
    snapMesh.userData = { pieceId: "basement_floor_panel" };
    group.add(snapMesh);

    // Basement Flap Quick-Pull Tab (Centered at top of 2in flap)
    const bTabGeo = new THREE.BoxGeometry(0.75, 0.7, 0.1);
    const bTab = new THREE.Mesh(bTabGeo, webbingMat);
    bTab.position.set(0, 2.2, halfBD + 0.1);
    bTab.userData = { pieceId: "basement_floor_panel" };
    group.add(bTab);

    // 7. REAR MESH POCKET
    const rearMeshGeo = new THREE.PlaneGeometry(9.0, 5.0);
    const rearMesh = new THREE.Mesh(rearMeshGeo, meshPocketMat.clone());
    rearMesh.position.set(0, 4.5, -halfBD + 0.1);
    rearMesh.userData = { pieceId: "rear_mesh_pocket" };
    group.add(rearMesh);

    // 7. SIDE GUSSET ATTACHMENTS
    // Left: Top Carabiner Anchor Loop + Dual Elastic Sleeves + Lower Magnetic Docks + Brushes
    // Right: 0.75in D-Ring Key Loop

    // A. Top Carabiner / S-Biner Clip Loop (Left Gusset @ y = 9.0)
    const clipLoopGeo = new THREE.TorusGeometry(0.4, 0.08, 8, 16, Math.PI);
    const clipLoopMesh = new THREE.Mesh(clipLoopGeo, dRingMat);
    clipLoopMesh.position.set(-halfBW + 0.3, 9.0, 0);
    clipLoopMesh.rotation.y = -Math.PI / 2;
    clipLoopMesh.userData = { pieceId: "ext_side_gusset_left" };
    group.add(clipLoopMesh);

    // B. Upper Silicone-Gripper Elastic Sleeves (Left Gusset @ y = 6.0)
    const brushSleeve1 = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 1.8, 12), webbingMat);
    brushSleeve1.position.set(-halfBW + 0.35, 6.0, 1.2);
    brushSleeve1.userData = { pieceId: "ext_side_gusset_left" };
    group.add(brushSleeve1);

    const brushSleeve2 = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.55, 2.0, 12), webbingMat);
    brushSleeve2.position.set(-halfBW + 0.35, 6.0, -1.2);
    brushSleeve2.userData = { pieceId: "ext_side_gusset_left" };
    group.add(brushSleeve2);

    // C. Lower Embedded N52 Magnetic Docks (Left Gusset @ y = 3.0)
    for (let zPos of [1.2, -1.2]) {
      const bDockGeo = new THREE.CylinderGeometry(0.28, 0.28, 0.08, 16);
      bDockGeo.rotateZ(Math.PI / 2);
      const bDock = new THREE.Mesh(bDockGeo, magnetMat);
      bDock.position.set(-halfBW + 0.3, 3.0, zPos);
      bDock.userData = { pieceId: "ext_side_gusset_left" };
      group.add(bDock);
    }

    // D. Detailing Boar's Hair Brush (Small)
    const brushWoodMat = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.6 });
    const brushBristleMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.9 });
    const brushSteelTailMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.95, roughness: 0.2 });

    // Brush 1 (Small Boar's Hair)
    const brushHandle1 = new THREE.Mesh(new THREE.BoxGeometry(0.35, 6.8, 0.22), brushWoodMat);
    brushHandle1.position.set(-halfBW + 0.35, 6.5, 1.2);
    brushHandle1.rotation.z = -0.04;
    group.add(brushHandle1);

    const brushTail1 = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.4, 12), brushSteelTailMat);
    brushTail1.position.set(-halfBW + 0.35, 3.2, 1.2);
    group.add(brushTail1);

    const brushHead1 = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.8, 0.4), brushBristleMat);
    brushHead1.position.set(-halfBW + 0.35, 9.8, 1.2);
    group.add(brushHead1);

    // Brush 2 (Large Boulder Crimp Brush)
    const brushHandle2 = new THREE.Mesh(new THREE.BoxGeometry(0.5, 7.5, 0.3), brushWoodMat);
    brushHandle2.position.set(-halfBW + 0.35, 6.8, -1.2);
    brushHandle2.rotation.z = -0.04;
    group.add(brushHandle2);

    const brushTail2 = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.5, 12), brushSteelTailMat);
    brushTail2.position.set(-halfBW + 0.35, 3.2, -1.2);
    group.add(brushTail2);

    const brushHead2 = new THREE.Mesh(new THREE.BoxGeometry(0.75, 2.2, 0.55), brushBristleMat);
    brushHead2.position.set(-halfBW + 0.35, 10.4, -1.2);
    group.add(brushHead2);

    // E. Right Gusset D-Ring Key Clip Loop
    const dRingGeo = new THREE.TorusGeometry(0.55, 0.1, 8, 16, Math.PI);
    const dRingMesh = new THREE.Mesh(dRingGeo, dRingMat);
    dRingMesh.position.set(halfBW - 0.2, 8.5, 0);
    dRingMesh.rotation.y = Math.PI / 2;
    dRingMesh.rotation.z = Math.PI;
    dRingMesh.userData = { pieceId: "ext_side_gusset_right" };
    group.add(dRingMesh);
  }

  // 8. INTERNAL AERODYNAMIC ANTI-PUFF BAFFLE FLAPS (70D Diamond Ripstop)
  if (activeLayer === "all" || activeLayer === "baffles" || activeLayer === "exterior" || isXRayMode) {
    const baffleMat = new THREE.MeshStandardMaterial({
      color: 0xf59e0b,
      roughness: 0.55,
      metalness: 0.15,
      wireframe: isWireframe,
      side: THREE.DoubleSide
    });

    const baffleW = topW * 0.94;
    const baffleH = 2.2;
    const baffleAngle = 0.4 + (0.7 * (1.0 - openAmount));

    const frontBaffleGeo = new THREE.PlaneGeometry(baffleW, baffleH, 8, 4);
    const frontBaffle = new THREE.Mesh(frontBaffleGeo, baffleMat.clone());
    frontBaffle.position.set(0, height - 1.5, (currentTopD / 2) - 0.25);
    frontBaffle.rotation.x = -baffleAngle;
    frontBaffle.userData = { pieceId: "anti_puff_baffle_flap" };
    group.add(frontBaffle);

    const backBaffleGeo = new THREE.PlaneGeometry(baffleW, baffleH, 8, 4);
    const backBaffle = new THREE.Mesh(backBaffleGeo, baffleMat.clone());
    backBaffle.position.set(0, height - 1.5, -(currentTopD / 2) + 0.25);
    backBaffle.rotation.x = baffleAngle;
    backBaffle.userData = { pieceId: "anti_puff_baffle_flap" };
    group.add(backBaffle);
  }

  // 9. HIGH-LOFT PLUSH FLEECE LINING (Interior Layer)
  if (activeLayer === "all" || activeLayer === "lining" || isXRayMode) {
    const fleeceScale = 0.95;
    const fleeceGeo = new THREE.CylinderGeometry(
      (topW * fleeceScale) / 2.2,
      (baseW * fleeceScale) / 2.2,
      height * 0.9,
      24,
      1,
      true
    );
    fleeceGeo.scale(1, 1, currentTopD / topW);
    const fleeceMesh = new THREE.Mesh(fleeceGeo, fleeceMat.clone());
    fleeceMesh.position.set(0, height * 0.45, 0);
    fleeceMesh.userData = { pieceId: ["fleece_lining_u_panel", "fleece_lining_gussets"] };
    group.add(fleeceMesh);
  }
}

function buildGenericPouch3D(project, group) {
  const w = 9.0;
  const h = 6.0;
  const d = 2.5;

  const mat = new THREE.MeshStandardMaterial({
    color: 0x0284c7,
    roughness: 0.7,
    metalness: 0.2,
    wireframe: isWireframe
  });

  const geo = new THREE.BoxGeometry(w, h, d);
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.y = h / 2;
  mesh.castShadow = true;
  group.add(mesh);

  const zipGeo = new THREE.BoxGeometry(w, 0.2, 0.3);
  const zipMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.4 });
  const zip = new THREE.Mesh(zipGeo, zipMat);
  zip.position.set(0, h, 0);
  group.add(zip);
}

function animate() {
  animationFrameId = requestAnimationFrame(animate);
  
  // Pulse the emissive intensity on the highlighted piece
  if (highlightedPieceId && current3DModelGroup) {
    const pulse = 0.65 + (0.35 * Math.sin(Date.now() * 0.007));
    current3DModelGroup.traverse(child => {
      if (child.isMesh && child.userData && child.userData.pieceId) {
        const isMatch = child.userData.pieceId === highlightedPieceId || (Array.isArray(child.userData.pieceId) && child.userData.pieceId.includes(highlightedPieceId));
        if (isMatch && child.material && child.material.emissiveIntensity !== undefined) {
          child.material.emissiveIntensity = pulse;
        }
      }
    });
  }

  if (controls) controls.update();
  if (renderer && scene && camera) {
    renderer.render(scene, camera);
  }
}
