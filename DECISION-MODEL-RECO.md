# Decision-model recommendation: prioritize unreviewed evidence

Date: 2026-10-11. Public-source proposal.
Reviewed [README](https://github.com/Ethical-Tech-CoLab/williamsburg-bridge-3d/blob/b3e77588a7e72e05e3ccd7b7d2e9c12117ad882d/README.md).
Assessment is documentation-led, not a geometry or image-validation audit.

## Bounded use

Suggest which public source/caption records a curator should inspect for a
specific component question. Use a relevance rubric and unknown, retaining
the original review status and source. This prioritizes work, not truth.

The reviewed README explicitly reports an auto-screened photo corpus. Do not
convert model review into "reviewed by a person". HAER reference photos without
known camera pose must not become dimension evidence. Unsourced dimensions
remain grade-D placeholders linked to open questions.

## Comparison and evaluation

Compare manual/lexical discovery and a local cross-encoder with Jev's
[reranking recipe](https://docs.typesafe.ai/cookbooks/rerank_typesafe.md),
Microsoft-Decision-1 and Sage on public metadata and source passages.
Split by source/part family; include wrong bridges, similar trusses, conflicting
dimensions and images without usable pose/scale.

Measure candidate recall, relevant-item recall at review budget, false support,
calibration, reviewer time and total cost. Do not infer accuracy from provider
benchmarks on unrelated tasks.

## Gate

No geometry, source-grade, human-review-status or shared-viewer change.
Preserve the traceability test that rejects improper photographic dimension
citations. Start offline with derived suggestions and reversible logging.
Exact proprietary checkpoints are not local models; local alternatives need
their own evaluation. No saving is claimed.
