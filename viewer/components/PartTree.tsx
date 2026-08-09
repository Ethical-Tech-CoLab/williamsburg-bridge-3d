import type { ModelConfig, PartMeta, Provenance } from '../src/model';

// Two letters, not one: a single "D" would be indistinguishable from source confidence grade D
// sitting next to it, which is exactly the axis-merging CONFIDENCE-MODEL.md section 1 warns about.
const PROVENANCE_TAG: Record<Provenance, string> = {
  MEASURED: 'MS',
  DOCUMENTED: 'DC',
  INFERRED: 'IN',
  ASSUMED: 'AS',
};

/** Component tree explorer, grouped by system. */
export function PartTree(props: {
  config: ModelConfig;
  parts: PartMeta[];
  visibleSystems: Set<string>;
  selectedId: string | null;
  onSelect: (id: string) => void;
}) {
  const bySystem = new Map<string, PartMeta[]>();
  for (const p of props.parts) {
    if (!bySystem.has(p.system)) bySystem.set(p.system, []);
    bySystem.get(p.system)!.push(p);
  }

  return (
    <div className="part-tree">
      <h3>Components</h3>
      {[...bySystem.entries()].map(([system, parts]) => (
        <details key={system} open={system !== 'reference'}>
          <summary>
            {system.replace(/_/g, ' ')}
            <span className="count">{parts.length}</span>
            {!props.visibleSystems.has(system) && <span className="muted"> hidden</span>}
          </summary>
          <ul>
            {parts.map((p) => (
              <li key={p.part_id}>
                <button
                  type="button"
                  className={p.part_id === props.selectedId ? 'part on' : 'part'}
                  onClick={() => props.onSelect(p.part_id)}
                >
                  <span
                    className="dot"
                    style={{ background: props.config.confidence[p.confidence].color }}
                    aria-hidden="true"
                  />
                  <span className="part-name">{p.part_id}</span>
                  <span className={`prov-tag prov-${p.provenance.toLowerCase()}`}>
                    {PROVENANCE_TAG[p.provenance]}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </details>
      ))}
    </div>
  );
}
