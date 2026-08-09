import type { ModelConfig, PartMeta } from '../src/model';
import { isDimensionable } from '../src/model';

export interface ControlRow {
  control_id: string;
  key: string;
  value: number;
  unit: string;
  source_ids: string[];
  confidence: string;
  notes: string;
}

/**
 * Locus on selection: what this part's geometry rests on, or a plain statement that there is
 * nothing. CONFIDENCE-MODEL.md section 4.
 */
export function MetadataPanel(props: {
  config: ModelConfig;
  part: PartMeta | null;
  controls: Map<string, ControlRow>;
  hoScale: boolean;
}) {
  if (!props.part) {
    return (
      <div className="metadata empty">
        <h3>No part selected</h3>
        <p>
          Select a component in the model or in the tree to see the controls its geometry rests on,
          the sources behind them, and the questions still open against it.
        </p>
      </div>
    );
  }

  const p = props.part;
  const dimensionable = isDimensionable(props.config, p);
  const refs = p.control_refs.map((id) => props.controls.get(id)).filter(Boolean) as ControlRow[];

  return (
    <div className="metadata">
      <h3>{p.part_id}</h3>
      <p className="subtle">{p.system.replace(/_/g, ' ')}</p>

      <dl className="kv">
        <dt>Source confidence</dt>
        <dd>
          <span className="dot" style={{ background: props.config.confidence[p.confidence].color }} />
          {props.config.confidence[p.confidence].label}
        </dd>
        <dt>Geometry provenance</dt>
        <dd className={`prov-${p.provenance.toLowerCase()}`}>
          {props.config.provenance[p.provenance].label}
        </dd>
        <dt>Material</dt>
        <dd>
          {p.material.replace(/_/g, ' ')} <span className="subtle">({p.material_id}, grade {p.material_confidence})</span>
        </dd>
        <dt>Basis</dt>
        <dd>{p.source_basis.join(', ')}</dd>
        <dt>Review</dt>
        <dd>
          {p.review_status.replace(/_/g, ' ')} <span className="subtle">by {p.last_modified_by_agent}</span>
        </dd>
      </dl>

      {p.notes && <p className="notes">{p.notes}</p>}

      <h4>Controls this geometry rests on</h4>
      {refs.length === 0 ? (
        <p className="warn">
          This part cites no control. Its position rests on nothing in GEOMETRY-CONTROL.md.
        </p>
      ) : (
        <table className="controls">
          <thead>
            <tr>
              <th>Control</th>
              <th>Value</th>
              {props.hoScale && <th>HO</th>}
              <th>Grade</th>
              <th>Sources</th>
            </tr>
          </thead>
          <tbody>
            {refs.map((c) => (
              <tr key={c.control_id} className={c.confidence === 'D' ? 'placeholder' : undefined}>
                <td>
                  <code>{c.control_id}</code>
                  <div className="subtle">{c.key.replace(/_/g, ' ')}</div>
                </td>
                <td className="num">
                  {dimensionable ? (
                    <>
                      {c.value} {c.unit}
                    </>
                  ) : (
                    <span className="withheld" title="No dimension is annotated on geometry whose position is not documented">
                      withheld
                    </span>
                  )}
                </td>
                {props.hoScale && (
                  <td className="num">
                    {dimensionable && c.unit !== 'count' && c.unit !== 'ratio'
                      ? `${hoMm(c, props.config.hoScaleDenominator).toFixed(1)} mm`
                      : '—'}
                  </td>
                )}
                <td>{c.confidence}</td>
                <td className="subtle">{c.source_ids.join(', ') || 'none'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!dimensionable && (
        <p className="warn">
          Dimensions are withheld for this part. Its provenance is{' '}
          {props.config.provenance[p.provenance].label.toLowerCase()}: if we do not know where it is,
          we do not get to say how big it is.
        </p>
      )}

      <h4>Open questions</h4>
      {p.open_questions.length === 0 ? (
        <p className="subtle">None recorded against this part.</p>
      ) : (
        <ul className="oq">
          {p.open_questions.map((q) => (
            <li key={q}>
              <code>{q}</code>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

const FT_TO_M = 0.3048;
const IN_TO_M = 0.0254;

function hoMm(c: ControlRow, denominator: number): number {
  const metres =
    c.unit === 'ft' ? c.value * FT_TO_M : c.unit === 'in' ? c.value * IN_TO_M : c.unit === 'mm' ? c.value / 1000 : c.value;
  return (metres / denominator) * 1000;
}
