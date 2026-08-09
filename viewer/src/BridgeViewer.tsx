/**
 * three.js scene for a source-governed GLB.
 *
 * Two rules from CONFIDENCE-MODEL.md section 4 are implemented here rather than in a side panel,
 * because they are what stops a schematic from lying:
 *
 *  1. The provenance filter HIDES. It does not fade. A faded outline is still a shape a reader will
 *     trace, and the honest experience of switching INFERRED and ASSUMED off on this model is a
 *     nearly empty frame.
 *  2. INFERRED geometry gets a dashed outline and ASSUMED a dotted one. Dashed lines in three.js
 *     need computeLineDistances() after the geometry is built or LineDashedMaterial silently
 *     renders solid.
 */

import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import type { ModelConfig, PartMeta, Provenance } from './model';

export interface ViewerProps {
  config: ModelConfig;
  assetUrl: string;
  partsById: Map<string, PartMeta>;
  visibleSystems: Set<string>;
  visibleProvenance: Set<Provenance>;
  selectedId: string | null;
  onSelect: (id: string | null) => void;
  showOutlines: boolean;
}

const OUTLINE_DASH: Record<string, { dashSize: number; gapSize: number } | null> = {
  solid: null,
  dashed: { dashSize: 6, gapSize: 4 },
  dotted: { dashSize: 1.2, gapSize: 3.5 },
};

const SELECTED_COLOR = new THREE.Color('#ffd166');

export function BridgeViewer(props: ViewerProps) {
  const mountRef = useRef<HTMLDivElement | null>(null);
  const stateRef = useRef<{
    renderer: THREE.WebGLRenderer;
    scene: THREE.Scene;
    camera: THREE.PerspectiveCamera;
    controls: OrbitControls;
    partNodes: Map<string, THREE.Mesh | THREE.Line>;
    outlines: Map<string, THREE.Object3D>;
    baseMaterials: Map<string, THREE.Material[]>;
    dispose: () => void;
  } | null>(null);

  // ---- one-time scene construction -------------------------------------------------
  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    // An explicit initial size: a headless page may never fire ResizeObserver, and a canvas sized
    // only from that ends up zero-width, which makes screenshots fail with no visible cause.
    renderer.setSize(mount.clientWidth || 1280, mount.clientHeight || 720, false);
    renderer.setClearColor(0x0f1216, 1);
    mount.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x0f1216, 2000, 6000);

    const camera = new THREE.PerspectiveCamera(
      45,
      (mount.clientWidth || 1280) / (mount.clientHeight || 720),
      props.config.camera.near,
      props.config.camera.far,
    );
    camera.position.set(...props.config.camera.position);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(...props.config.camera.target);
    controls.enableDamping = true;
    controls.maxDistance = props.config.camera.far * 0.5;
    controls.update();

    scene.add(new THREE.HemisphereLight(0xbfd4e8, 0x1b2026, 2.0));
    const key = new THREE.DirectionalLight(0xffffff, 1.6);
    key.position.set(-600, 800, 700);
    scene.add(key);

    const grid = new THREE.GridHelper(4000, 40, 0x2a3340, 0x1b222b);
    (grid.material as THREE.Material).transparent = true;
    (grid.material as THREE.Material).opacity = 0.35;
    scene.add(grid);

    const partNodes = new Map<string, THREE.Mesh | THREE.Line>();
    const outlines = new Map<string, THREE.Object3D>();
    const baseMaterials = new Map<string, THREE.Material[]>();

    const loader = new GLTFLoader();
    loader.load(
      props.assetUrl,
      (gltf) => {
        scene.add(gltf.scene);
        gltf.scene.traverse((obj) => {
          const meta = props.partsById.get(obj.name);
          if (!meta) return;
          // Line-mode glTF primitives arrive as LineSegments, not Mesh. Registering only meshes
          // left the suspenders, floor beams, railings and the whole reference frame outside the
          // filter and unpickable, while appearing to work because the towers did hide.
          const isMesh = (obj as THREE.Mesh).isMesh === true;
          const isLine = (obj as THREE.Line).isLine === true;
          if (!isMesh && !isLine) return;
          const renderable = obj as THREE.Mesh | THREE.Line;
          partNodes.set(meta.part_id, renderable);
          baseMaterials.set(
            meta.part_id,
            Array.isArray(renderable.material) ? renderable.material : [renderable.material],
          );

          const style = props.config.provenance[meta.provenance];
          const dash = OUTLINE_DASH[style?.outline ?? 'solid'];
          if (dash && isMesh) {
            const edges = new THREE.EdgesGeometry(renderable.geometry as THREE.BufferGeometry, 25);
            const line = new THREE.LineSegments(
              edges,
              new THREE.LineDashedMaterial({
                color: 0xdfe7ef,
                dashSize: dash.dashSize,
                gapSize: dash.gapSize,
                transparent: true,
                opacity: 0.85,
              }),
            );
            // Without this the dashes render as a solid line, silently.
            line.computeLineDistances();
            renderable.add(line);
            outlines.set(meta.part_id, line);
          }
        });
        applyVisibility();
      },
      undefined,
      (err) => console.error('GLB load failed', err),
    );

    const raycaster = new THREE.Raycaster();
    // Line geometry has no surface, so picking needs a world-space threshold. These are meters.
    raycaster.params.Line = { threshold: 3 };
    raycaster.params.Points = { threshold: 3 };
    const pointer = new THREE.Vector2();
    let downAt = { x: 0, y: 0 };

    const onPointerDown = (e: PointerEvent) => {
      downAt = { x: e.clientX, y: e.clientY };
    };
    const onPointerUp = (e: PointerEvent) => {
      if (Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y) > 4) return; // a drag, not a pick
      const rect = renderer.domElement.getBoundingClientRect();
      pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(pointer, camera);
      const candidates = [...partNodes.entries()].filter(([, o]) => o.visible).map(([, o]) => o);
      const hit = raycaster.intersectObjects(candidates, false)[0];
      props.onSelect(hit ? hit.object.name : null);
    };
    renderer.domElement.addEventListener('pointerdown', onPointerDown);
    renderer.domElement.addEventListener('pointerup', onPointerUp);

    function applyVisibility() {
      const s = stateRef.current;
      if (!s) return;
      for (const [id, node] of s.partNodes) {
        const meta = props.partsById.get(id);
        if (!meta) continue;
        node.visible =
          props.visibleSystems.has(meta.system) && props.visibleProvenance.has(meta.provenance);
      }
    }

    const resize = () => {
      const w = mount.clientWidth || 1280;
      const h = mount.clientHeight || 720;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    };
    const ro = new ResizeObserver(resize);
    ro.observe(mount);
    window.addEventListener('resize', resize);

    let raf = 0;
    const tick = () => {
      controls.update();
      renderer.render(scene, camera);
      raf = requestAnimationFrame(tick);
    };
    tick();

    stateRef.current = {
      renderer,
      scene,
      camera,
      controls,
      partNodes,
      outlines,
      baseMaterials,
      dispose: () => {
        cancelAnimationFrame(raf);
        ro.disconnect();
        window.removeEventListener('resize', resize);
        renderer.domElement.removeEventListener('pointerdown', onPointerDown);
        renderer.domElement.removeEventListener('pointerup', onPointerUp);
        controls.dispose();
        renderer.dispose();
        if (renderer.domElement.parentElement === mount) mount.removeChild(renderer.domElement);
      },
    };

    return () => {
      stateRef.current?.dispose();
      stateRef.current = null;
    };
    // The scene is built once; every subsequent change is applied by the effects below.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ---- filters: hide, never fade ---------------------------------------------------
  useEffect(() => {
    const s = stateRef.current;
    if (!s) return;
    for (const [id, node] of s.partNodes) {
      const meta = props.partsById.get(id);
      if (!meta) continue;
      node.visible =
        props.visibleSystems.has(meta.system) && props.visibleProvenance.has(meta.provenance);
    }
  }, [props.visibleSystems, props.visibleProvenance, props.partsById]);

  // ---- outline toggle ---------------------------------------------------------------
  useEffect(() => {
    const s = stateRef.current;
    if (!s) return;
    for (const line of s.outlines.values()) line.visible = props.showOutlines;
  }, [props.showOutlines]);

  // ---- selection highlight ----------------------------------------------------------
  useEffect(() => {
    const s = stateRef.current;
    if (!s) return;
    for (const [id] of s.partNodes) {
      const selected = id === props.selectedId;
      for (const m of s.baseMaterials.get(id) ?? []) {
        const mm = m as THREE.MeshStandardMaterial & { color?: THREE.Color };
        if (mm.emissive) {
          if (!mm.userData.originalEmissive) mm.userData.originalEmissive = mm.emissive.clone();
          mm.emissive.copy(selected ? SELECTED_COLOR : mm.userData.originalEmissive);
        } else if (mm.color) {
          // Line materials have no emissive channel, so selection swaps the base colour instead.
          if (!mm.userData.originalColor) mm.userData.originalColor = mm.color.clone();
          mm.color.copy(selected ? SELECTED_COLOR : mm.userData.originalColor);
        }
      }
    }
  }, [props.selectedId]);

  return <div className="viewport" ref={mountRef} data-testid="viewport" />;
}
