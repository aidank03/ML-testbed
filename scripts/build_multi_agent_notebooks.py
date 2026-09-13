"""Build the dependency-light Factor multi-agent and ontology teaching notebooks."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


def lines(text: str) -> list[str]:
    return dedent(text).strip("\n").splitlines(keepends=True)


def markdown(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": lines(text)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines(text),
    }


def notebook(lesson: str, cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python (Factor AI)",
                "language": "python",
                "name": "factor-ai",
            },
            "language_info": {
                "name": "python",
                "version": "3.12",
                "mimetype": "text/x-python",
                "codemirror_mode": {"name": "ipython", "version": 3},
                "pygments_lexer": "ipython3",
                "nbconvert_exporter": "python",
                "file_extension": ".py",
            },
            "ml_testbed": {
                "course_version": "0.2.0",
                "lesson": lesson,
                "evaluation": "public development",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


coordination = notebook("15", [
    markdown("""
    # ML-testbed 15 — coordinate a bounded agent fleet

    Lesson 14 assembled one closed-loop synthetic experiment. This lesson turns that loop into **typed work that multiple temporary agents could execute safely**. It models logical work items, a bounded scheduler, creator–validator stages, idempotent delivery, and a controlled knowledge commit.

    It does **not** launch LLMs, background workers, or a distributed service. The goal is to inspect the coordination semantics before adding infrastructure.
    """),
    markdown("""
    ## How to use this lesson

    Run from the top after the earlier ML-testbed lessons, or independently with Python 3.10 or later. No API calls, downloads, model server, PyTorch, or distributed runtime are required.

    **Skills:** task graphs, bounded concurrency, typed agent contracts, validation, idempotency, controlled knowledge commits

    **Evidence contract:** every result is a deterministic teaching simulation. It demonstrates software invariants; it does not establish multi-agent scale, reliability, cost, or scientific performance in production.
    """),
    markdown("""
    ## The architecture under test

    ```mermaid
    flowchart LR
      G[Goal] --> L[Typed task ledger]
      L --> S[Bounded scheduler]
      S --> W[Temporary workers]
      K[Versioned knowledge] --> C[Context compiler]
      C --> W
      W --> V[Validator]
      V -->|accepted| K
      V -->|provisional or rejected| R[Review queue]
      W --> E[Append-only events]
      V --> E
    ```

    The planner proposes dependencies. The scheduler owns admission and concurrency. Workers never write canonical knowledge directly.
    """),
    code("""
    from dataclasses import dataclass, field
    from collections import defaultdict
    from typing import Callable
    import hashlib
    import json

    @dataclass
    class WorkItem:
        task_id: str
        role: str
        objective: str
        depends_on: tuple[str, ...] = ()
        expected_type: str = "Artifact"
        status: str = "planned"
        attempts: int = 0

    def canonical(value):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))

    def stable_id(prefix, value):
        digest = hashlib.sha256(canonical(value).encode()).hexdigest()[:12]
        return f"{prefix}:{digest}"
    """),
    markdown("""
    ## 1. Define a typed evidence-to-decision graph

    These are six logical tasks, not six simultaneous model calls. Dependencies determine which work is ready.
    """),
    code("""
    tasks = {
        item.task_id: item for item in [
            WorkItem("task:source-a", "researcher", "Inspect calibration source A"),
            WorkItem("task:source-b", "researcher", "Inspect diagnostic source B"),
            WorkItem("task:claim", "analyst", "Propose an atomic drift claim",
                     ("task:source-a", "task:source-b"), "Claim"),
            WorkItem("task:calculation", "calculator", "Check the bounded interval",
                     ("task:source-a",), "Artifact"),
            WorkItem("task:validate", "validator", "Validate evidence and calculation",
                     ("task:claim", "task:calculation"), "Evaluation"),
            WorkItem("task:decision", "curator", "Commit or withhold the decision",
                     ("task:validate",), "Decision"),
        ]
    }

    def ready_items(ledger):
        complete = {task_id for task_id, item in ledger.items() if item.status == "accepted"}
        return [item for item in ledger.values()
                if item.status == "planned" and set(item.depends_on) <= complete]

    for item in tasks.values():
        deps = ", ".join(item.depends_on) or "—"
        print(f"{item.task_id:<18} {item.role:<11} depends on: {deps}")
    """),
    markdown("""
    ## 2. Run bounded scheduling waves

    Change `MAX_CONCURRENCY` and rerun. The result remains dependency-correct; only the number of admitted tasks per wave changes.
    """),
    code("""
    MAX_CONCURRENCY = 2
    events = []
    wave = 0

    while any(item.status == "planned" for item in tasks.values()):
        ready = ready_items(tasks)
        if not ready:
            raise RuntimeError("No ready work: the graph is cyclic or a dependency failed")
        admitted = ready[:MAX_CONCURRENCY]
        wave += 1
        print(f"wave {wave}: " + ", ".join(item.task_id for item in admitted))
        for item in admitted:
            item.status = "running"
            item.attempts += 1
            events.append({"event": "leased", "task_id": item.task_id, "attempt": item.attempts})
        for item in admitted:
            item.status = "accepted"
            events.append({"event": "accepted", "task_id": item.task_id, "attempt": item.attempts})

    print()
    print(f"{len(tasks)} tasks completed in {wave} waves; peak concurrency was bounded at {MAX_CONCURRENCY}.")
    """),
    markdown("""
    ## 3. Why dependency graphs replace all-to-all chat

    An unrestricted group of `n` agents has `n(n-1)/2` possible pairwise channels. Typed task graphs grow with actual dependencies instead.
    """),
    code("""
    dependency_edges = sum(len(item.depends_on) for item in tasks.values())
    print("agents/tasks | pairwise channels | this task graph")
    print("-------------|-------------------|----------------")
    for n in (10, 100, 1_000, 10_000):
        pairwise = n * (n - 1) // 2
        print(f"{n:>12,} | {pairwise:>17,} | {dependency_edges:>15}")
    """),
    markdown("""
    ## 4. Validate before committing knowledge

    A worker produces a proposal. A deterministic gate checks its shape and evidence references. The curator—not the worker—owns the canonical write.
    """),
    code("""
    artifacts = {
        "artifact:calibration-a": {"kind": "Source", "verified": True},
        "artifact:diagnostic-b": {"kind": "Observation", "verified": True},
    }
    proposal = {
        "object_type": "Claim",
        "statement": "Optical-path drift can mimic apparent motion in the synthetic model.",
        "evidence_ids": ["artifact:calibration-a", "artifact:diagnostic-b"],
        "scope": "synthetic-development-only",
        "verification_status": "provisional",
    }

    def validate_claim(claim, artifact_store):
        errors = []
        required = {"object_type", "statement", "evidence_ids", "scope", "verification_status"}
        if set(claim) != required:
            errors.append("claim shape does not match the contract")
        missing = [ref for ref in claim.get("evidence_ids", []) if ref not in artifact_store]
        if missing:
            errors.append(f"missing evidence: {missing}")
        if claim.get("scope") != "synthetic-development-only":
            errors.append("claim exceeds the evaluated scientific scope")
        return errors

    errors = validate_claim(proposal, artifacts)
    knowledge = {}
    if not errors:
        claim_id = stable_id("claim", proposal)
        knowledge[claim_id] = {**proposal, "verification_status": "accepted"}
        print("controlled commit:", claim_id)
    else:
        print("withheld from canonical knowledge:", errors)
    """),
    markdown("""
    ## 5. Duplicate delivery must be harmless

    Distributed queues may deliver the same task more than once. An idempotency key makes the second commit a replay rather than a second fact.
    """),
    code("""
    commit_log = {}

    def commit_once(idempotency_key, value):
        if idempotency_key in commit_log:
            return "replayed", commit_log[idempotency_key]
        object_id = stable_id("artifact", value)
        commit_log[idempotency_key] = object_id
        return "created", object_id

    payload = {"task_id": "task:claim", "attempt": 1, "result": proposal}
    print(commit_once("task:claim/attempt:1", payload))
    print(commit_once("task:claim/attempt:1", payload))
    print("canonical records:", len(commit_log))
    """),
    markdown("""
    ## What this lab establishes

    - Logical task count is separate from model-call concurrency.
    - Dependencies make coordination inspectable and prevent premature work.
    - Schema and evidence checks occur before knowledge commit.
    - Idempotency makes duplicate delivery recoverable.
    - The event log preserves attempts; accepted state is a governed projection.

    **Try next:** introduce a failed validation, a missing dependency, or a concurrency limit of one. Then decide which events a real Factor runtime must preserve for replay.
    """),
])


ontology = notebook("16", [
    markdown("""
    # ML-testbed 16 — build shared ontology and provenance

    Lesson 15 coordinated bounded work. This lesson builds the durable shared memory those workers need. It explores why organized data affects LLM retrieval, training, and evaluation by loading Factor's ontology kernel, constructing typed knowledge records, comparing retrieval policies, compiling a reproducible context manifest, and filtering a training set by provenance.

    No model is called. The lab isolates the **data-selection mechanism** so it can later be compared with identical models and token budgets.
    """),
    markdown("""
    ## How to use this lesson

    Run from the Factor repository root or `notebooks/` with Python 3.10 or later. No API calls, downloads, model server, or graph database are required.

    **Skills:** ontology envelopes, tags, provenance, governed retrieval, immutable context manifests, training-data lineage

    **Evidence contract:** the retrieval collection and relevance labels are an exposed teaching example. The comparison explains a mechanism; it is not a measured claim that an ontology improves LLM accuracy on independent tasks.
    """),
    markdown("""
    ## The knowledge pipeline

    ```mermaid
    flowchart LR
      R[Raw documents] --> N[Normalize and hash]
      N --> T[Type and tag]
      T --> P[Attach provenance]
      P --> V[Validate]
      V --> K[Versioned knowledge]
      K --> C[Compile authorized context]
      C --> A[LLM or deterministic worker]
      A --> E[Evaluate]
      E -->|governed update| K
    ```

    The context window is a temporary projection. The versioned knowledge system is the durable memory.
    """),
    code("""
    from pathlib import Path
    from datetime import datetime, timezone
    import hashlib
    import json

    candidates = [Path.cwd(), Path.cwd().parent]
    ROOT = next((path for path in candidates
                 if (path / "docs/ontology/factor-core.schema.json").is_file()), None)
    if ROOT is None:
        raise FileNotFoundError("Run this notebook from factor/ or factor/notebooks/")

    ontology_schema = json.loads((ROOT / "docs/ontology/factor-core.schema.json").read_text())
    example_claim = json.loads((ROOT / "docs/ontology/example-claim.json").read_text())
    print("ontology:", example_claim["ontology_version"])
    print("object type:", example_claim["object_type"])
    print("tags:", ", ".join(example_claim["tags"]))
    print("status:", example_claim["verification_status"])
    """),
    markdown("""
    ## 1. Inspect the common metadata envelope

    This lightweight check explains the fields used below. It is **not** a replacement for a JSON Schema 2020-12 validator.
    """),
    code("""
    required = set(ontology_schema["$defs"]["envelope"]["required"])
    missing = required - set(example_claim)
    assert not missing, f"missing required fields: {sorted(missing)}"
    assert 0 <= example_claim["confidence"] <= 1
    assert len(set(example_claim["tags"])) == len(example_claim["tags"])

    print(f"required envelope fields present: {len(required)}")
    for name in sorted(required):
        print(f"  {name:<24} {example_claim[name]}")
    """),
    markdown("""
    ## 2. Build a tiny governed document collection

    `relevant` is evaluator truth for this teaching example. A production benchmark would keep it separate from the retrieval code.
    """),
    code("""
    documents = [
        {"id": "source:calibration-note", "text": "Optical drift calibration and motion ambiguity.",
         "type": "Source", "tags": ["domain/pdv", "topic/optical-drift"],
         "status": "accepted", "security": "project", "relevant": True},
        {"id": "artifact:synthetic-drift-run", "text": "Synthetic optical drift reproduces apparent motion.",
         "type": "Artifact", "tags": ["domain/pdv", "topic/optical-drift", "evidence/synthetic"],
         "status": "accepted", "security": "project", "relevant": True},
        {"id": "claim:bounded-inference", "text": "Motion remains ambiguous without a defensible drift bound.",
         "type": "Claim", "tags": ["domain/pdv", "topic/optical-drift"],
         "status": "provisional", "security": "project", "relevant": True},
        {"id": "source:obsolete-note", "text": "Optical drift never affects motion inference.",
         "type": "Source", "tags": ["domain/pdv", "topic/optical-drift"],
         "status": "superseded", "security": "project", "relevant": False},
        {"id": "artifact:generated-summary", "text": "A model says optical drift proves material motion.",
         "type": "Artifact", "tags": ["domain/pdv", "origin/model-generated"],
         "status": "unreviewed", "security": "project", "relevant": False},
        {"id": "source:restricted-shot", "text": "Restricted optical drift and motion record.",
         "type": "Source", "tags": ["domain/pdv", "topic/optical-drift"],
         "status": "accepted", "security": "restricted", "relevant": False},
        {"id": "source:robotics", "text": "Optical flow estimates robot motion.",
         "type": "Source", "tags": ["domain/robotics"],
         "status": "accepted", "security": "public", "relevant": False},
        {"id": "policy:review", "text": "Claims need evidence and review before acceptance.",
         "type": "Policy", "tags": ["governance/claims"],
         "status": "accepted", "security": "project", "relevant": False},
    ]

    for doc in documents:
        doc["sha256"] = hashlib.sha256(doc["text"].encode()).hexdigest()
    print(f"collection contains {len(documents)} versionable objects")
    """),
    markdown("""
    ## 3. Compare unstructured and governed retrieval

    The unstructured baseline sees words only. The governed strategy combines lexical matching with type, tag, verification, and authorization filters.
    """),
    code("""
    query_terms = {"optical", "drift", "motion"}

    def lexical_score(doc):
        words = set(doc["text"].lower().replace(".", "").split())
        return len(query_terms & words)

    unstructured = sorted(
        (doc for doc in documents if lexical_score(doc) > 0),
        key=lambda doc: (-lexical_score(doc), doc["id"]),
    )[:5]

    governed = [doc for doc in unstructured
                if "domain/pdv" in doc["tags"]
                and doc["status"] in {"accepted", "provisional"}
                and doc["security"] in {"public", "project"}]

    def metrics(results):
        selected = {doc["id"] for doc in results}
        truth = {doc["id"] for doc in documents if doc["relevant"]}
        hits = len(selected & truth)
        return {
            "selected": len(selected),
            "precision": hits / len(selected) if selected else 0,
            "recall": hits / len(truth) if truth else 0,
        }

    for label, results in [("unstructured", unstructured), ("governed", governed)]:
        score = metrics(results)
        print(f"{label:<13} selected={score['selected']}  precision={score['precision']:.2f}  recall={score['recall']:.2f}")
        for doc in results:
            print("  ", doc["id"])
    """),
    markdown("""
    This toy result is explanatory, not an empirical LLM-performance claim. A real Factor evaluation must freeze tasks and truth, use identical models and token budgets, and measure citation validity, unsupported claims, accuracy, calibration, latency, and cost.
    """),
    markdown("""
    ## 4. Compile an immutable context manifest

    The manifest records the exact object IDs, hashes, and selection policy. A changed source creates a different manifest rather than silently altering an old attempt.
    """),
    code("""
    manifest_payload = {
        "ontology_version": "factor-ontology/0.1",
        "objective": "Assess whether optical drift can mimic apparent motion",
        "selection_policy": {
            "domain_tag": "domain/pdv",
            "allowed_status": ["accepted", "provisional"],
            "allowed_security": ["public", "project"],
        },
        "items": [{"id": doc["id"], "sha256": doc["sha256"]} for doc in governed],
    }
    manifest_hash = hashlib.sha256(
        json.dumps(manifest_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    context_manifest = {
        "id": f"context:{manifest_hash[:16]}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        **manifest_payload,
    }

    print(context_manifest["id"])
    print(json.dumps(context_manifest["items"], indent=2))
    """),
    markdown("""
    ## 5. Trace provenance instead of trusting fluent text

    Claims and artifacts remain separate. Typed relationships let a reviewer walk from a claim to its evidence and original source.
    """),
    code("""
    relationships = [
        ("claim:bounded-inference", "supportedBy", "artifact:synthetic-drift-run"),
        ("artifact:synthetic-drift-run", "derivedFrom", "source:calibration-note"),
    ]

    def provenance_path(start):
        path, frontier, seen = [], [start], set()
        while frontier:
            current = frontier.pop(0)
            if current in seen:
                continue
            seen.add(current)
            for subject, predicate, obj in relationships:
                if subject == current:
                    path.append((subject, predicate, obj))
                    frontier.append(obj)
        return path

    for subject, predicate, obj in provenance_path("claim:bounded-inference"):
        print(f"{subject} --{predicate}--> {obj}")
    """),
    markdown("""
    ## 6. Use provenance to protect a training split

    Hashes expose duplicate content. Origin tags and review status let a dataset builder exclude unreviewed model output instead of training on it as if it were independent evidence.
    """),
    code("""
    candidates = documents + [{**documents[0], "id": "source:calibration-note-copy"}]
    accepted_examples, excluded, seen_hashes = [], [], set()

    for doc in candidates:
        reasons = []
        if doc["sha256"] in seen_hashes:
            reasons.append("duplicate-content")
        if "origin/model-generated" in doc["tags"] and doc["status"] != "accepted":
            reasons.append("unreviewed-model-origin")
        if doc["status"] in {"rejected", "superseded", "unreviewed"}:
            reasons.append(f"status/{doc['status']}")
        if doc["security"] == "restricted":
            reasons.append("not-authorized-for-training")
        if reasons:
            excluded.append((doc["id"], reasons))
        else:
            accepted_examples.append(doc["id"])
            seen_hashes.add(doc["sha256"])

    print("accepted training examples:", len(accepted_examples))
    print("excluded:")
    for object_id, reasons in excluded:
        print(f"  {object_id:<34} {', '.join(reasons)}")
    """),
    markdown("""
    ## What this lab establishes

    - Types and tags make retrieval policy explicit.
    - Provenance distinguishes source evidence from generated interpretation.
    - Verification and security filters prevent known-bad or unauthorized context.
    - Content hashes help detect duplicates and freeze datasets.
    - Context manifests make model-visible inputs replayable.

    **Try next:** change a status, tag, or authorization level and observe the manifest ID and retrieval metrics. Then add temporal validity or a contradictory claim without deleting either interpretation.
    """),
])


def main() -> None:
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    outputs = {
        "15_multi_agent_coordination_lab.ipynb": coordination,
        "16_data_ontology_and_provenance_lab.ipynb": ontology,
    }
    for name, payload in outputs.items():
        path = NOTEBOOKS / name
        path.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
