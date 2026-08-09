import type { Confidence, ModelConfig, PartMeta, Provenance } from '../src/model';
import { CONFIDENCE_ORDER, PROVENANCE_ORDER } from '../src/model';

/**
 * The standing tally. CONFIDENCE-MODEL.md section 4 requires it permanently on screen rather than
 * below the fold of a scrolling list, because a buried tally is a hidden tally.
 */
export function ConfidenceLegend(props: {
  config: ModelConfig;
  parts: PartMeta[];
  provenanceCensus: Record<Provenance, number>;
  confidenceCensus: Record<Confidence, number>;
}) {
  const total = props.parts.length;
  return (
    <div className="legend" role="status" aria-label="Provenance and confidence tally">
      <div className="legend-block">
        <h3>Geometry provenance</h3>
        <ul>
          {PROVENANCE_ORDER.map((p) => {
            const n = props.provenanceCensus[p] ?? 0;
            return (
              <li key={p} className={n === 0 ? 'zero' : undefined}>
                <span className={`swatch prov-${p.toLowerCase()}`} aria-hidden="true" />
                <span className="legend-label">{props.config.provenance[p].label}</span>
                <span className="legend-count">{n}</span>
              </li>
            );
          })}
        </ul>
      </div>
      <div className="legend-block">
        <h3>Source confidence</h3>
        <ul>
          {CONFIDENCE_ORDER.map((c) => {
            const n = props.confidenceCensus[c] ?? 0;
            return (
              <li key={c} className={n === 0 ? 'zero' : undefined}>
                <span
                  className="swatch"
                  style={{ background: props.config.confidence[c].color }}
                  aria-hidden="true"
                />
                <span className="legend-label">{props.config.confidence[c].label}</span>
                <span className="legend-count">{n}</span>
              </li>
            );
          })}
        </ul>
      </div>
      <p className="legend-total">
        {total} parts. Nothing in this model is measured, and no dimension is annotated on geometry
        whose position is not documented.
      </p>
    </div>
  );
}
