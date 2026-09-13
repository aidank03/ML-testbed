# Focused roadmap

## Complete in version 0.2

- Package, CLI, local Git repository, install/build configuration and CI definition.
- Reproducible synthetic experiment-to-evaluation workflow.
- Numerical diagnostic scorecards and uncertainty/abstention reporting.
- Analytic physics checks and candidate-measurement ranking.
- Local evidence retrieval and optional structured LLM integration.
- Separate public AI candidate runner and answer grader.

## Next: one real shot

1. Attach and review the original project folder.
2. Freeze the exact observable, clock relation, field of view and calibration contract.
3. Implement a reader for the real PDV/radiographic formats and test it with representative data.
4. Produce one reproducible evaluation card with independently reviewed labels.

## After that

- Connect a verified one-dimensional material/current-diffusion solver and compare motion across EOS/conductivity choices.
- Implement raw PDV and energy-dependent radiographic forward/reduction pipelines.
- Add spatial-growth and phase-inference tasks with censoring and clock covariance.
- Test a controlled seed contrast, then one informative intervention.
- Run a live model baseline, retrieval-only baseline and retrieval-plus-calculation baseline on genuinely held-out tasks.
- Transfer the validated observables to an imploding-liner benchmark.

## Multi-agent and governed-data track

The architecture, ontology vocabulary and staged gates are defined in [Multi-agent systems and data ontology](MULTI_AGENT_AND_DATA_ONTOLOGY.md).

1. Validate the ontology kernel and add typed Python models for sources, artifacts, claims, relationships, evaluations and context manifests.
2. Compile replayable context from explicit versioned object references.
3. Add a durable work-item ledger and a bounded creator-validator workflow with one controlled knowledge-commit path.
4. Compare unstructured, tagged and provenance-aware retrieval using the same model, task set and token budget.
5. Scale logical work only after correctness, contradiction handling, recovery, cost and authorization gates pass.

Large-fleet operation is not an implemented capability or current performance claim.

No calendar promise is made for facility work or solver access. A model or diagnostic should advance only when its defined evaluation gate is met.
