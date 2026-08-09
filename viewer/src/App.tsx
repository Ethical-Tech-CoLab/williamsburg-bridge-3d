import { useEffect, useMemo, useState } from 'react';
import { BridgeViewer } from './BridgeViewer';
import { ConfidenceLegend } from '../components/ConfidenceLegend';
import { MetadataPanel, type ControlRow } from '../components/MetadataPanel';
import { PartTree } from '../components/PartTree';
import { Toolbar } from '../components/Toolbar';
import {
  CONFIDENCE_ORDER,
  PROVENANCE_ORDER,
  census,
  loadModel,
  type Confidence,
  type ModelConfig,
  type PartMeta,
  type PartsDoc,
  type Provenance,
} from './model';

interface Loaded {
  config: ModelConfig;
  parts: PartsDoc;
  assetUrl: string;
}

export function App() {
  const [loaded, setLoaded] = useState<Loaded | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [visibleSystems, setVisibleSystems] = useState<Set<string>>(new Set());
  const [visibleProvenance, setVisibleProvenance] = useState<Set<Provenance>>(
    new Set(PROVENANCE_ORDER),
  );
  const [showOutlines, setShowOutlines] = useState(true);
  const [showHo, setShowHo] = useState(false);

  useEffect(() => {
    loadModel()
      .then((m) => {
        setLoaded(m);
        setVisibleSystems(new Set(m.parts.parts.map((p) => p.system)));
      })
      .catch((e: unknown) => setError(e instanceof Error ? e.message : String(e)));
  }, []);

  const partsById = useMemo(() => {
    const map = new Map<string, PartMeta>();
    for (const p of loaded?.parts.parts ?? []) map.set(p.part_id, p);
    return map;
  }, [loaded]);

  const controlsById = useMemo(() => {
    const map = new Map<string, ControlRow>();
    for (const c of (loaded?.parts as unknown as { controls?: ControlRow[] })?.controls ?? []) {
      map.set(c.control_id, c);
    }
    return map;
  }, [loaded]);

  const systems = useMemo(
    () => [...new Set((loaded?.parts.parts ?? []).map((p) => p.system))],
    [loaded],
  );

  const provenanceCensus = useMemo(() => {
    const base = Object.fromEntries(PROVENANCE_ORDER.map((p) => [p, 0])) as Record<Provenance, number>;
    return { ...base, ...census(loaded?.parts.parts ?? [], (p) => p.provenance) };
  }, [loaded]);

  const confidenceCensus = useMemo(() => {
    const base = Object.fromEntries(CONFIDENCE_ORDER.map((c) => [c, 0])) as Record<Confidence, number>;
    return { ...base, ...census(loaded?.parts.parts ?? [], (p) => p.confidence) };
  }, [loaded]);

  if (error) {
    return (
      <div className="fatal">
        <h1>Could not load the model</h1>
        <p>{error}</p>
        <p className="subtle">
          Run <code>python scripts/build_control_skeleton.py</code> from the repository root, then
          reload.
        </p>
      </div>
    );
  }
  if (!loaded) return <div className="fatal">Loading…</div>;

  const { config, parts } = loaded;
  const visibleCount = parts.parts.filter(
    (p) => visibleSystems.has(p.system) && visibleProvenance.has(p.provenance),
  ).length;

  return (
    <div className="app">
      <header>
        <div>
          <h1>{config.title}</h1>
          <p className="subtitle">
            {config.subtitle} · {parts.parts.length} parts · units {config.units}, datum{' '}
            {config.verticalDatum}
          </p>
        </div>
        <div className="build-id" title="The control document this model was built from">
          <span>{config.documents.control}</span>
          <code>{parts.control_document_sha256.slice(0, 12)}</code>
        </div>
      </header>

      <aside className="left">
        <Toolbar
          config={config}
          systems={systems}
          visibleSystems={visibleSystems}
          onToggleSystem={(s) =>
            setVisibleSystems((prev) => {
              const next = new Set(prev);
              if (next.has(s)) next.delete(s);
              else next.add(s);
              return next;
            })
          }
          visibleProvenance={visibleProvenance}
          onToggleProvenance={(p) =>
            setVisibleProvenance((prev) => {
              const next = new Set(prev);
              if (next.has(p)) next.delete(p);
              else next.add(p);
              return next;
            })
          }
          showOutlines={showOutlines}
          onToggleOutlines={() => setShowOutlines((v) => !v)}
          showHo={showHo}
          onToggleHo={() => setShowHo((v) => !v)}
          provenanceCensus={provenanceCensus}
        />
        <PartTree
          config={config}
          parts={parts.parts}
          visibleSystems={visibleSystems}
          selectedId={selectedId}
          onSelect={setSelectedId}
        />
      </aside>

      <main>
        <BridgeViewer
          config={config}
          assetUrl={loaded.assetUrl}
          partsById={partsById}
          visibleSystems={visibleSystems}
          visibleProvenance={visibleProvenance}
          selectedId={selectedId}
          onSelect={setSelectedId}
          showOutlines={showOutlines}
        />
        {visibleCount === 0 && (
          <div className="empty-frame">
            <p>
              Nothing is visible. That is not a bug: with these filters, this model has nothing to
              show you. The frame is empty because the evidence is.
            </p>
          </div>
        )}
        <ConfidenceLegend
          config={config}
          parts={parts.parts}
          provenanceCensus={provenanceCensus}
          confidenceCensus={confidenceCensus}
        />
      </main>

      <aside className="right">
        <MetadataPanel
          config={config}
          part={selectedId ? (partsById.get(selectedId) ?? null) : null}
          controls={controlsById}
          hoScale={showHo}
        />
      </aside>
    </div>
  );
}
