import type { ModelConfig, Provenance } from '../src/model';
import { PROVENANCE_ORDER } from '../src/model';

/**
 * System and provenance filters.
 *
 * The provenance switches HIDE geometry, they do not fade it. Turning INFERRED and ASSUMED off on
 * this model leaves the reference frame, the towers and the station markers, and that emptiness is
 * the honest picture rather than a bug.
 */
export function Toolbar(props: {
  config: ModelConfig;
  systems: string[];
  visibleSystems: Set<string>;
  onToggleSystem: (system: string) => void;
  visibleProvenance: Set<Provenance>;
  onToggleProvenance: (p: Provenance) => void;
  showOutlines: boolean;
  onToggleOutlines: () => void;
  showHo: boolean;
  onToggleHo: () => void;
  isFullscreen: boolean;
  onToggleFullscreen: () => void;
  provenanceCensus: Record<Provenance, number>;
}) {
  return (
    <div className="toolbar">
      <section>
        <h3>Systems</h3>
        <div className="chips">
          {props.systems.map((s) => (
            <button
              key={s}
              type="button"
              className={props.visibleSystems.has(s) ? 'chip on' : 'chip'}
              onClick={() => props.onToggleSystem(s)}
              aria-pressed={props.visibleSystems.has(s)}
            >
              {s.replace(/_/g, ' ')}
            </button>
          ))}
        </div>
      </section>

      <section>
        <h3>Provenance filter</h3>
        <p className="hint">These hide geometry. They do not fade it.</p>
        <div className="chips">
          {PROVENANCE_ORDER.map((p) => (
            <button
              key={p}
              type="button"
              className={props.visibleProvenance.has(p) ? `chip on prov-${p.toLowerCase()}` : 'chip'}
              onClick={() => props.onToggleProvenance(p)}
              aria-pressed={props.visibleProvenance.has(p)}
              disabled={(props.provenanceCensus[p] ?? 0) === 0}
              title={
                (props.provenanceCensus[p] ?? 0) === 0
                  ? `No ${props.config.provenance[p].label.toLowerCase()} geometry exists in this model`
                  : undefined
              }
            >
              {props.config.provenance[p].label}
              <span className="chip-count">{props.provenanceCensus[p] ?? 0}</span>
            </button>
          ))}
        </div>
      </section>

      <section>
        <h3>Display</h3>
        <div className="chips">
          <button
            type="button"
            className={props.showOutlines ? 'chip on' : 'chip'}
            onClick={props.onToggleOutlines}
            aria-pressed={props.showOutlines}
          >
            Provenance outlines
          </button>
          <button
            type="button"
            className={props.showHo ? 'chip on' : 'chip'}
            onClick={props.onToggleHo}
            aria-pressed={props.showHo}
          >
            HO 1:{props.config.hoScaleDenominator}
          </button>
          <button
            type="button"
            className={props.isFullscreen ? 'chip on' : 'chip'}
            onClick={props.onToggleFullscreen}
            aria-pressed={props.isFullscreen}
            title="Fullscreen (F). Press Escape to leave."
          >
            {props.isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}
          </button>
        </div>
      </section>
    </div>
  );
}
