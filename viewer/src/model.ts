/**
 * Types and loading for a source-governed model.
 *
 * The viewer compiles in nothing about any particular bridge. It reads model.config.json for how to
 * render provenance and confidence, and parts.json for what every part rests on.
 */

export type Provenance = 'MEASURED' | 'DOCUMENTED' | 'INFERRED' | 'ASSUMED';
export type Confidence = 'A' | 'B' | 'C' | 'D';

export interface PartMeta {
  part_id: string;
  system: string;
  source_basis: string[];
  control_refs: string[];
  source_ids: string[];
  open_questions: string[];
  confidence: Confidence;
  provenance: Provenance;
  material: string;
  material_id: string;
  material_confidence: Confidence;
  prototype_units: string;
  ho_scale_units: string;
  last_modified_by_agent: string;
  review_status: string;
  notes: string;
}

export interface PartsDoc {
  schema_version: string;
  model: string;
  milestone: number;
  bridge: string;
  control_document: string;
  control_document_sha256: string;
  units: string;
  vertical_datum: string;
  ho_scale_denominator: number;
  taxonomy: string[];
  parts: PartMeta[];
}

export interface ProvenanceStyle {
  label: string;
  opacity: number;
  outline: 'solid' | 'dashed' | 'dotted';
  dimensionable: boolean;
}

export interface ModelConfig {
  modelId: string;
  title: string;
  subtitle: string;
  asset: string;
  parts: string;
  units: string;
  verticalDatum: string;
  hoScaleDenominator: number;
  upAxis: string;
  camera: { position: [number, number, number]; target: [number, number, number]; near: number; far: number };
  provenance: Record<Provenance, ProvenanceStyle>;
  confidence: Record<Confidence, { label: string; color: string }>;
  documents: Record<string, string>;
}

export const PROVENANCE_ORDER: Provenance[] = ['MEASURED', 'DOCUMENTED', 'INFERRED', 'ASSUMED'];
export const CONFIDENCE_ORDER: Confidence[] = ['A', 'B', 'C', 'D'];

/** Resolve a config-relative URL against the config's own location, so one build works both
 *  standalone and co-served under a district site root. */
function resolveAgainst(base: string, target: string): string {
  return new URL(target, new URL(base, window.location.href)).toString();
}

export async function loadModel(configUrl = './model.config.json'): Promise<{
  config: ModelConfig;
  parts: PartsDoc;
  assetUrl: string;
}> {
  const configRes = await fetch(configUrl);
  if (!configRes.ok) throw new Error(`could not load ${configUrl}: ${configRes.status}`);
  const config = (await configRes.json()) as ModelConfig;

  const partsUrl = resolveAgainst(configUrl, config.parts);
  const partsRes = await fetch(partsUrl);
  if (!partsRes.ok) throw new Error(`could not load ${partsUrl}: ${partsRes.status}`);
  const parts = (await partsRes.json()) as PartsDoc;

  return { config, parts, assetUrl: resolveAgainst(configUrl, config.asset) };
}

export function census<T extends string>(parts: PartMeta[], key: (p: PartMeta) => T): Record<T, number> {
  const out = {} as Record<T, number>;
  for (const p of parts) {
    const k = key(p);
    out[k] = (out[k] ?? 0) + 1;
  }
  return out;
}

/** A part may only carry a dimension callout if its provenance permits it.
 *  CONFIDENCE-MODEL.md section 4: if we do not know where it is, we do not get to say how big it is. */
export function isDimensionable(config: ModelConfig, part: PartMeta): boolean {
  return config.provenance[part.provenance]?.dimensionable ?? false;
}

export function hoMillimetres(prototypeMetres: number, denominator: number): number {
  return (prototypeMetres / denominator) * 1000;
}
