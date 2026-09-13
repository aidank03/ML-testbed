---
title: Multi-Agent Frameworks and Ontologies
subtitle: Architecture map, implementation guide, and project memory
status: Living reference
last_updated: 2026-09-13
---

# Multi-Agent Frameworks and Ontologies

## Purpose of this file

This is a consolidated map and memory file for designing collective agent systems for broad knowledge work. It explains the core concepts, architecture, ontology, memory model, data pipeline, coordination patterns, implementation path, technology landscape, risks, and recommended sequence for bringing a new developer into the space.

The document is intentionally platform-neutral. An agent system may be controlled through a web application, CLI, API, IDE, issue tracker, chat application, notebook, or several of these interfaces at once.

## Quick recall

The core idea is:

> A collective agent system is a workflow system in which some workers use language models, combined with a knowledge system that supplies and preserves their context.

The most important architectural rule is:

> Shared memory lives outside the agents. Each agent receives a bounded, task-specific context packet compiled from a larger, durable knowledge system.

A useful system begins with four operations:

1. Store knowledge.
2. Compile relevant context.
3. Run a bounded task.
4. Validate and commit the result.

Everything else is an extension of these operations for scale, reliability, security, governance, and user experience.

## 1. What an agent is

An agent is a software process that uses a model, instructions, context, and tools in a loop to pursue a goal.

A minimal agent loop is:

1. Receive a task and context.
2. Decide what action to take.
3. Call a model or tool.
4. Observe the result.
5. Continue, stop, or request help.
6. Return a structured output.

An agent is not necessarily:

- A permanent process
- A unique model
- A long conversation
- An autonomous identity
- A separate container or virtual machine

One agent definition can produce thousands of executions. A fleet of 10,000 logical agents might use only 100 active workers and 50 simultaneous model calls.

Always distinguish these quantities:

- Logical agents or tasks
- Active worker processes
- Concurrent model requests
- Workflow steps
- Tool calls per second
- Tokens per minute
- Cost per run
- Human reviews required

## 2. The system mental model

A large collective agent system is closer to a distributed operating system plus a data platform than to a large group chat.

Agents are temporary cognitive workers. The platform owns:

- Goals and task decomposition
- Scheduling and admission control
- Durable workflow state
- Shared knowledge
- Context construction
- Permissions and policies
- Validation and evaluation
- Provenance and audit history
- Budgets and model quotas
- Human approvals

Agents should collaborate through typed tasks and knowledge objects, not unrestricted all-to-all messaging. Ten thousand agents create 49,995,000 possible pairwise connections. A system that permits every agent to communicate with every other agent will spend increasing amounts of time routing, summarizing, reconciling, and repeating information.

The scalable alternatives are:

- Dependency graphs
- Hierarchical supervision
- Shared blackboards
- Publish and subscribe channels
- Typed artifact exchange
- Evidence and claim graphs
- Single-writer or controlled-merge policies

## 3. Architectural planes

| Plane | Responsibility | Typical components |
| --- | --- | --- |
| Experience | Submit work, inspect runs, approve actions | Web console, CLI, API, IDE, Slack, GitHub, notebooks |
| Mission | Define goals, programs, policies, and success criteria | Goal service, policy engine, evaluation registry |
| Coordination | Plan, schedule, budget, retry, cancel, and supervise | Durable workflows, task graph, queues, admission control |
| Execution | Perform cognitive and tool-using work | Agent workers, sandboxes, model gateway, tool gateway |
| Knowledge | Maintain collective understanding and compile context | Ontology service, evidence graph, memory services, retrieval |
| Data | Preserve authoritative state and artifacts | Event log, relational or graph store, object storage, indexes |

### Experience plane

The user interface should be replaceable. A browser control center is usually best for fleet operations, while a CLI and API support automation and development. An IDE can provide repository-aware workflows but should not be responsible for keeping the runtime alive.

A mature interface exposes:

- Goals, programs, and runs
- Task dependency graphs
- Ready, running, blocked, and failed work
- Agent and worker status
- Model usage and cost
- Live events and traces
- Context manifests
- Artifacts and claims
- Evaluations and disagreements
- Retry, pause, cancel, and replay controls
- Human approval queues
- Tool and data permissions

### Mission plane

The mission plane defines why work exists. A goal should include:

- Desired outcome
- Owner
- Scope
- Constraints
- Deadline
- Success criteria
- Allowed risk and cost
- Required human authority

The mission plane is where open-ended intent becomes a controlled program of work.

### Coordination plane

The coordination plane maintains the task graph and determines what may run. It contains two distinct functions:

- The planner proposes tasks and dependencies.
- The scheduler decides when and whether tasks are allowed to run.

This separation prevents an agent from creating unlimited recursive work.

### Execution plane

The execution plane contains stateless or lightly stateful workers. Workers claim tasks, obtain a context packet, perform work, and return structured results. Execution environments may be local processes, serverless functions, containers, virtual machines, microVM sandboxes, or distributed compute jobs.

### Knowledge plane

The knowledge plane turns data into addressable organizational understanding. It manages concepts, entities, claims, relationships, provenance, conflicts, validity, and context compilation.

### Data plane

The data plane preserves authoritative records. Current state can be stored directly or derived from an append-only event history. Large artifacts should generally be stored outside the workflow payload.

## 4. The core execution lifecycle

A work item normally follows this lifecycle:

`planned -> ready -> leased -> running -> review -> accepted`

Additional states include:

- `blocked`
- `failed`
- `cancelled`
- `expired`
- `rejected`
- `superseded`

A complete task execution works as follows:

1. A goal is decomposed into typed work items.
2. Dependencies determine which tasks are ready.
3. Admission control checks priority, permissions, quotas, and budgets.
4. A worker leases the task for a limited time.
5. The context compiler constructs an immutable context manifest.
6. The agent executes using only approved tools and data.
7. The agent returns typed results, evidence, uncertainties, and proposed follow-up work.
8. Validators check the result.
9. Accepted outputs are committed as artifacts, claims, decisions, or events.
10. Dependent tasks become ready.

Leases, idempotency keys, and conditional writes are important because distributed task delivery can occur more than once.

## 5. The minimum core components

### 5.1 Task ledger

The task ledger is the authoritative record of work. Build it before building an elaborate supervisor agent.

Each work item should contain:

- Stable task ID
- Goal and parent task
- Task type
- Objective
- Dependencies
- Required capabilities
- Input references
- Expected output schema
- Owner or cohort
- Priority
- Status
- Lease owner and expiration
- Attempt count
- Token, time, and cost budgets
- Allowed tools and data scopes
- Created, started, completed, and reviewed times
- Error and retry information

The conversation transcript is supporting evidence. It is not the task ledger.

### 5.2 Ontology and schema registry

The ontology defines what important things mean and how they relate. The schema registry defines their machine-readable shapes and versions.

The ontology can begin as code:

- Pydantic models
- JSON Schema
- Enumerated entity types
- Enumerated relationship types
- Validation rules
- Examples and tests

It does not require an RDF store or graph database at the beginning.

### 5.3 Knowledge repository

The repository stores typed entities, claims, relationships, decisions, policies, and evaluations. It should preserve version history and provenance.

### 5.4 Artifact store

The artifact store holds documents, datasets, images, model outputs, reports, code, and other large objects. The knowledge repository points to these artifacts and describes their meaning.

### 5.5 Context compiler

The context compiler retrieves relevant knowledge and produces a bounded, reproducible context packet for an agent execution.

### 5.6 Agent runner

The runner implements the inner model and tool loop. It enforces limits and produces structured results.

### 5.7 Validator and curator

Validators assess schema compliance, evidence, calculations, safety, and quality. Curators decide what becomes accepted knowledge.

### 5.8 Orchestrator and scheduler

The orchestrator manages durable workflow progress. The scheduler controls dispatch, concurrency, priority, and resource use.

### 5.9 Model and tool gateways

Gateways centralize:

- Authentication
- Provider routing
- Rate limits
- Token accounting
- Caching
- Retries
- Tool permissions
- Network policy
- Audit logging

### 5.10 Observability and evaluation

Observability records what happened. Evaluation determines whether the result was good.

Both are required. A successful HTTP response does not mean an agent produced a useful answer.

## 6. Memory architecture

Memory should be divided by function.

| Memory type | Contains | Lifetime |
| --- | --- | --- |
| Working memory | Current instructions, observations, scratch state | One task or turn |
| Run memory | Task graph, status, dependencies, intermediate decisions | One program or run |
| Semantic memory | Concepts, entities, claims, definitions, relationships | Long-lived and versioned |
| Episodic memory | Events, traces, attempts, outcomes | Append-only history |
| Artifact memory | Documents, datasets, reports, code, calculations | Durable object storage |
| Procedural memory | Skills, tools, prompts, playbooks, evaluation methods | Versioned reusable assets |
| Governance memory | Policies, permissions, budgets, retention rules | Authoritative and audited |

The shared knowledge system is the memory. A model context window is a temporary projection of that memory.

### Why raw conversation history is insufficient

Conversation histories contain duplicated facts, obsolete conclusions, unsupported statements, and large amounts of task-specific detail. They are difficult to query and expensive to place into future prompts.

Important information should be promoted from conversation into typed objects:

- A result becomes an `Artifact`.
- A proposition becomes a `Claim`.
- A selected course becomes a `Decision`.
- A change becomes an `Event`.
- A reusable method becomes a `Procedure` or `Skill`.
- A restriction becomes a `Policy`.

## 7. Ontology design

### What an ontology is

An ontology defines:

- Types of things
- Meanings of those types
- Allowed relationships
- Constraints on those relationships
- Identity and equivalence rules
- Version and validity rules
- How domain concepts connect to work and evidence

An ontology is more than a taxonomy. A taxonomy primarily classifies. An ontology also expresses meaning and relationships.

An ontology is also different from a knowledge graph. The ontology is the model. The knowledge graph is data instantiated using that model.

### Three connected ontology layers

1. **Domain ontology:** concepts specific to the field in which work occurs.
2. **Work ontology:** goals, tasks, agents, tools, runs, artifacts, decisions, and evaluations.
3. **Provenance ontology:** sources, activities, derivations, authorship, timestamps, and responsibility.

### General core entities

- **Goal:** desired outcome, scope, constraints, owner, and success criteria.
- **Program:** coordinated collection of goals and work streams.
- **WorkItem:** schedulable unit of work.
- **Agent:** versioned capability and policy profile.
- **Human:** person with responsibility or decision authority.
- **Tool:** callable capability with permissions and contracts.
- **Source:** original evidence or data origin.
- **Artifact:** durable work product.
- **Claim:** atomic proposition with evidence and validity.
- **Concept:** canonical domain entity or category.
- **Observation:** recorded measurement or finding.
- **Decision:** selected action with supporting rationale.
- **Event:** immutable record of something that happened.
- **Policy:** rule governing agents, tools, data, or actions.
- **Evaluation:** assessment of a run, output, claim, or agent version.
- **ContextManifest:** exact inputs assembled for an execution.
- **Procedure:** reusable method or playbook.

### General core relationships

| Subject | Relationship | Object |
| --- | --- | --- |
| Goal | decomposesInto | WorkItem |
| WorkItem | dependsOn | WorkItem |
| Agent | executes | WorkItem |
| Agent | uses | Tool |
| WorkItem | consumes | Artifact or Claim |
| WorkItem | produces | Artifact or Claim |
| Artifact | derivedFrom | Source or Artifact |
| Claim | about | Concept |
| Claim | supportedBy | Source, Observation, Artifact, or Claim |
| Claim | refutedBy | Source, Observation, Artifact, or Claim |
| Claim | contradicts | Claim |
| Decision | basedOn | Claim or Evaluation |
| Decision | selects | Alternative |
| Policy | governs | Agent, WorkItem, Tool, Data, or Action |
| Evaluation | scores | Run, Artifact, Claim, or Agent version |
| Event | changes | Entity or relationship |
| ContextManifest | includes | Versioned entity or artifact |
| Procedure | appliesTo | WorkItem type |

### Required metadata envelope

Every important object should include:

- Stable identifier
- Object type
- Schema and ontology version
- Tenant, project, and security classification
- Creator: human, agent, or system
- Created and observed times
- Valid-from and valid-to times where relevant
- Source and derivation chain
- Confidence or verification status where relevant
- Content hash
- Version number
- Supersedes and superseded-by relationships
- Ownership or stewardship

### Build the ontology from questions

Do not begin by trying to list everything in a domain. Begin with competency questions the system must answer.

Examples:

- Which sources support this claim?
- Which claims disagree about this concept?
- Which tasks and decisions depend on this assumption?
- Which artifacts were generated using this model version?
- Which observations validate this prediction?
- What must be reconsidered if this claim is refuted?
- Who has authority to approve this action?
- Which knowledge was available when this decision was made?

For each question:

1. Identify the entities involved.
2. Identify the necessary relationships.
3. Identify required metadata and provenance.
4. Create valid and invalid examples.
5. Define validation rules.
6. Test whether real queries can answer the question.

Start with a small stable kernel. Extend it using versioned domain modules.

## 8. Context compilation

The context compiler is the bridge between the knowledge system and the agent.

### Inputs

- Work item
- Goal and success criteria
- Agent role and capabilities
- Dependency outputs
- Policies and permissions
- Token, time, and cost budgets
- Candidate knowledge and memories

### Retrieval methods

- Stable identifiers
- Metadata filters
- Relational queries
- Graph traversal
- Lexical search
- Vector similarity
- Recency and temporal validity
- Provenance and authority ranking
- Prior evaluation performance

### Compilation operations

The compiler should:

- Deduplicate information
- Prefer current valid versions
- Preserve unresolved disagreements
- Distinguish evidence from generated interpretation
- Exclude unauthorized data
- Fit the token budget
- Retain source links
- Record every included object version

### Context packet

A useful context packet contains:

- Objective
- Success criteria
- Relevant definitions
- Known claims with citations
- Open questions and disagreements
- Dependency outputs
- Applicable policies
- Allowed tools
- Required output schema
- Token, time, and cost budget
- Context manifest ID

The context packet should be immutable for an individual attempt. If context changes, create a new manifest and attempt.

### Important principle

Vector search is one retrieval technique. It is not the complete memory architecture. Tasks, authority, decisions, provenance, validity, and relationships require structured representation.

## 9. Agent contracts

Every agent invocation should use a typed input contract and typed output contract.

### Example input

```json
{
  "task_id": "task-204",
  "objective": "Assess the evidence supporting assumption A",
  "context_manifest_id": "context-881",
  "allowed_tools": ["literature_search", "data_catalog"],
  "output_schema": "EvidenceAssessmentV2",
  "budget": {
    "max_tokens": 50000,
    "max_cost_usd": 10,
    "deadline_seconds": 900
  }
}
```

### Example output

```json
{
  "status": "completed",
  "claims": [],
  "artifacts": [],
  "evidence_links": [],
  "uncertainties": [],
  "proposed_tasks": [],
  "summary": ""
}
```

The output should separate:

- Observations
- Claims
- Evidence
- Inferences
- Decisions
- Uncertainties
- Proposed work

This separation makes validation and reuse possible.

## 10. Validation and knowledge commit

Agent output should not automatically become accepted knowledge.

Validation may include:

- JSON or schema validation
- Citation existence
- Source quality checks
- Numerical and unit consistency
- Reproduction of calculations
- Contradiction detection
- Policy checks
- Independent agent review
- Human review
- Domain-specific tests

The curator or commit service decides whether to:

- Accept a claim
- Reject it
- Mark it provisional
- Preserve it as a competing interpretation
- Supersede an older version
- Request additional evidence

Maintain these distinctions:

- An **artifact** is something produced.
- A **claim** is something asserted.
- An **accepted claim** is something that passed the required governance process.
- A **decision** is an authorized selection, not merely a plausible recommendation.

Canonical facts should not be silently overwritten. New evidence should create a new claim or version. A materialized view can determine the current accepted state.

## 11. Coordination patterns

Different forms of work need different patterns.

### Map-reduce

Many workers independently process items. A reducer aggregates results. Good for literature review, classification, extraction, evaluation, and dataset processing.

### Planner-worker

A planner creates tasks and dependencies. Workers execute them. The scheduler limits what actually runs.

### Creator-validator

One agent produces an output. Other agents or deterministic checks challenge it before acceptance.

### Debate with adjudication

Multiple agents develop different interpretations. An adjudicator evaluates evidence and either selects an answer or records unresolved disagreement.

### Blackboard

Agents publish typed claims, requests, and artifacts to a shared knowledge space. Other agents subscribe to relevant changes rather than conversing with every participant.

### Deterministic pipeline

Fixed stages combine ordinary code with model judgment. This is often more reliable than allowing an agent to invent the workflow dynamically.

### Hierarchical cohorts

Workers are organized into cohorts, perhaps 10 to 50 agents, with a supervisor responsible for a bounded subproblem. Program orchestrators coordinate supervisors.

### Market or auction

Workers bid based on capability, confidence, availability, and expected cost. Useful when capabilities vary, but usually unnecessary in an initial system.

### Single-writer rule

Multiple agents may research, propose, critique, and validate in parallel. Shared canonical state should be committed by one authorized service or controlled merge process.

## 12. Data and knowledge pipeline

The pipeline transforms raw material into governed knowledge and then supplies new work.

1. **Ingest:** capture documents, databases, APIs, user input, and agent outputs.
2. **Normalize:** parse formats, identify language, attach source metadata, and hash content.
3. **Classify:** assign ontology types, domains, sensitivity, and retention rules.
4. **Extract:** identify entities, concepts, events, claims, relationships, and candidate tasks.
5. **Resolve:** deduplicate identities, reconcile aliases, and connect versions.
6. **Validate:** check schemas, provenance, permissions, evidence, and contradictions.
7. **Commit:** append immutable events and update accepted projections.
8. **Index:** update relational, graph, lexical, and vector indexes.
9. **Compile:** construct context packets for authorized tasks.
10. **Execute:** run agents and tools.
11. **Evaluate:** score outputs and system behavior.
12. **Learn:** feed accepted improvements back through the governed pipeline.

The ontology governs meaning across this pipeline. The event log preserves what happened. The repository holds accepted and provisional knowledge. Indexes are replaceable projections optimized for retrieval.

## 13. Storage model

A practical first implementation can use PostgreSQL and object storage.

### Minimum tables

- `goals`
- `work_items`
- `work_item_dependencies`
- `agent_definitions`
- `agent_executions`
- `entities`
- `entity_versions`
- `relations`
- `claims`
- `artifacts`
- `events`
- `context_manifests`
- `context_manifest_items`
- `policies`
- `evaluations`

JSONB is useful for evolving domain-specific payloads while stable identifiers, types, status, timestamps, and relationships remain relational.

Add other systems only when justified:

- Object storage for large artifacts
- Vector index for semantic retrieval
- Search engine for advanced lexical search
- Graph database for traversal workloads that become difficult in SQL
- Redis for temporary caching, leases, or rate-limit counters
- Kafka for high-volume event streaming and multiple independent consumers

Do not make the vector database the system of record.

## 14. Orchestration and execution infrastructure

### Agent behavior frameworks

Frameworks implement the inner agent loop:

- OpenAI Agents SDK
- Google Agent Development Kit
- LangGraph
- Microsoft AutoGen
- CrewAI
- PydanticAI
- Semantic Kernel

They provide combinations of tools, handoffs, sessions, graph nodes, structured results, tracing, and local state. They do not automatically provide the entire fleet platform.

### Durable workflow systems

Durable workflow systems manage the outer lifecycle:

- Temporal
- Restate
- DBOS
- AWS Step Functions

Use them when runs must survive crashes, deployments, long waits, retries, or human approvals.

### Queues

- Amazon SQS
- Kafka
- Redis Streams
- RabbitMQ

Queues provide buffering and backpressure. Choose the simplest queue that satisfies delivery, ordering, throughput, and operational requirements.

### Worker runtimes

- Local Python processes
- Serverless functions
- Managed containers
- Kubernetes jobs
- Ray workers
- Dedicated virtual machines

### Sandboxes

Agents that execute code, control browsers, or access sensitive tools need isolation. Options include:

- E2B
- Modal
- Daytona
- Container sandboxes
- Firecracker or other microVM systems
- Isolated Kubernetes jobs

### Managed agent platforms

- Amazon Bedrock AgentCore
- Microsoft Foundry Agent Service
- Google Gemini Enterprise Agent Platform

These platforms can provide managed runtime, memory, identity, gateway, governance, or observability components. Application-level ontology, task semantics, evaluation, and knowledge quality remain the developer's responsibility.

## 15. Existing multi-agent products

Software-development products provide useful examples of agent control surfaces and operational patterns:

- Cognition Devin and Fusion
- Factory Droids and Missions
- Cursor Cloud Agents
- GitHub Copilot coding agents and agent control surfaces
- OpenHands Agent Canvas, Agent Server, and Sandbox Server

These products demonstrate:

- Isolated execution environments
- Background agents
- Task decomposition
- Worktree or branch isolation
- Human approval
- Validation and review
- Cost and usage control
- Control-center interfaces

They are narrower than a general collective knowledge-work platform.

An important practical lesson from current systems is that parallel agents work best on independently writable tasks. Multiple agents can contribute intelligence while writes to shared state remain controlled.

## 16. Observability and evaluation

### Observability

Record:

- Workflow and task IDs
- Agent definition and version
- Model and prompt versions
- Context manifest
- Model calls
- Tool calls
- Latency
- Token usage
- Cost
- Retries and errors
- Artifact and claim IDs
- Validation outcomes

OpenTelemetry provides a common tracing foundation. Agent-oriented platforms include LangSmith, Arize Phoenix, Braintrust, and Weights & Biases Weave.

### Evaluation

Evaluate at several levels:

- **Step:** Was this tool call correct?
- **Task:** Did the agent satisfy the output contract?
- **Claim:** Is the proposition supported?
- **Workflow:** Did the overall process reach the desired result?
- **System:** Is the platform reliable, affordable, secure, and useful?

Use deterministic tests wherever possible. Use model-based judges for dimensions that require judgment, and calibrate them against human review.

Maintain offline evaluation datasets for regression testing and sample production runs for ongoing quality monitoring.

## 17. Security and governance

Every agent should have an execution identity and explicit authority.

Control:

- Data it may read
- Tools it may call
- Networks it may access
- Artifacts it may create
- State it may modify
- Money it may spend
- Tasks it may delegate
- Actions requiring human approval

Important controls include:

- Least-privilege credentials
- Short-lived tokens
- Tool allowlists
- Network egress rules
- Data classification
- Prompt-injection defenses
- Secret isolation
- Audit logs
- Approval gates
- Delegation-depth limits
- Per-run and per-tenant budgets
- Emergency cancellation

Treat retrieved content as untrusted data, not executable instructions.

## 18. Scaling model

### Approximately 10 agents

Use one process or a small durable workflow. Focus on typed tasks, structured outputs, evidence, validation, and context manifests.

### Approximately 100 agents

Add a durable task ledger, queue, bounded worker pool, explicit budgets, evaluation, and basic ontology governance.

### Approximately 1,000 agents

Add hierarchical supervision, partitioned queues, capability routing, admission control, policy enforcement, artifact storage, distributed tracing, and conflict-resolution workflows.

### Approximately 10,000 agents

Treat the platform as a multi-tenant distributed system. Add:

- Sharding
- Fair scheduling
- Blast-radius isolation
- Regional worker pools
- Replay and recovery
- Schema migration
- Ontology stewardship
- Model and tool quota allocation
- Human kill switches
- Aggressive backpressure

Ten thousand logical tasks should not produce 10,000 simultaneous model calls. Most work will be queued, blocked on dependencies, awaiting review, or complete.

## 19. Failure model

Design explicitly for:

- Duplicate task delivery
- Worker crashes
- Lost heartbeats
- Partial tool execution
- Model throttling
- Invalid structured output
- Context retrieval failure
- Stale knowledge
- Conflicting claims
- Poisoned sources
- Recursive delegation
- Cost exhaustion
- Human approval timeout
- Deployment during active runs
- Ontology and schema changes

Important mechanisms include:

- Idempotency keys
- Leases and heartbeats
- Bounded retries
- Dead-letter queues
- Checkpoints
- Immutable events
- Versioned contexts
- Compensating actions
- Failure thresholds
- Circuit breakers
- Replay tools

## 20. Common anti-patterns

- Treating every model call as a unique autonomous agent
- Allowing every agent to message every other agent
- Using conversation history as the only memory
- Storing every output as accepted truth
- Treating embeddings as the ontology
- Beginning with a universal ontology
- Giving agents unrestricted write access
- Letting planners create unlimited tasks
- Using one supervisor as a global bottleneck
- Introducing Kubernetes before defining task contracts
- Introducing Kafka before basic queue semantics are understood
- Measuring throughput without measuring correctness
- Ignoring model and tool quotas
- Allowing generated content to cite other generated content as independent evidence
- Failing to distinguish recommendations from authorized decisions

## 21. Recommended starting stack

For a new implementation:

- Python
- Pydantic or JSON Schema
- PostgreSQL
- Local filesystem or S3-compatible object storage
- One model provider
- One agent SDK
- Pytest
- Structured JSON logging
- CLI or small API

Add later:

- Temporal, Restate, or Step Functions
- SQS, Redis Streams, or another queue
- Sandboxed workers
- OpenTelemetry
- A web control center
- Dedicated search or graph infrastructure

The system of record should remain independent of any one model provider or agent framework.

## 22. Suggested repository structure

```text
collective-system/
  ontology/
    entities.py
    relationships.py
    validation.py
    versions.py
  tasks/
    models.py
    ledger.py
    scheduler.py
    leases.py
  knowledge/
    repository.py
    claims.py
    retrieval.py
    context_compiler.py
  agents/
    runner.py
    researcher.py
    analyst.py
    validator.py
    curator.py
  workflows/
    evidence_assessment.py
  gateways/
    models.py
    tools.py
    policies.py
  evaluations/
    schema_checks.py
    citation_checks.py
    quality_tests.py
  observability/
    tracing.py
    metrics.py
  api/
    routes.py
  cli.py
```

## 23. New developer onboarding

### Stage 1: One reliable agent

Teach the developer to:

- Define a typed task
- Give an agent limited tools
- Require structured output
- Record model and tool activity
- Capture artifacts
- Test timeouts and failures

Success means the same input can be replayed and inspected.

### Stage 2: External memory

Add:

- Sources
- Artifacts
- Claims
- Concepts
- Relationships
- Provenance
- Context manifests
- Hybrid retrieval

Success means the agent can answer using the repository without receiving every document.

### Stage 3: Ten coordinated agents

Add:

- Task dependencies
- Worker pool
- Bounded concurrency
- Validator agents
- Retry and cancellation
- Single controlled commit path

Success means agents coordinate through the task ledger and knowledge system rather than direct chat.

### Stage 4: Durable execution

Add:

- Durable workflow engine
- Queue
- Sandboxed workers where needed
- Model and tool gateways
- OpenTelemetry
- Cost and quota enforcement
- Human approval
- Replay and recovery

Success means work survives worker crashes and deployments.

### Stage 5: Scale testing

Run 100, 1,000, and 10,000 logical tasks using fake or inexpensive models before increasing real inference concurrency.

Test:

- Duplicates
- Failures
- Throttling
- Cancellation
- Queue backlog
- Schema migration
- Conflicting claims
- Budget exhaustion
- Recovery time

## 24. First reference project

The best first project is a narrow evidence-to-decision workflow.

Example goal:

> Assess the evidence supporting a technical assumption and identify which models, predictions, observations, and decisions depend on it.

Possible task graph:

1. Identify relevant sources.
2. Extract atomic claims and evidence.
3. Identify relevant models and prior analyses.
4. Map predictions to observable outcomes.
5. Identify constraints, disagreements, and missing evidence.
6. Validate claims and citations.
7. Produce a synthesis with explicit uncertainty.

The first demonstration should include:

- One goal
- Five to ten typed tasks
- Three agent roles
- One context compiler
- One validator
- Twenty-five documents
- A task and knowledge ledger
- A reproducible final artifact

## 25. Build sequence

1. Define five competency questions.
2. Define the ontology kernel and metadata envelope.
3. Implement entity, claim, relation, and task schemas.
4. Build the task and knowledge ledger.
5. Implement the context compiler and manifest format.
6. Run one agent with structured input and output.
7. Add provenance and deterministic validation.
8. Add a small worker pool and task dependencies.
9. Add independent evaluation and controlled commits.
10. Add durable execution, queues, and recovery.
11. Add a control interface.
12. Load-test logical tasks before scaling model traffic.
13. Add hierarchical coordination only when needed.
14. Establish ontology and policy stewardship.

## 26. Design decisions to preserve

- Agents are workers, not the system of record.
- Context is compiled, not accumulated indefinitely.
- The ontology begins small and grows from useful questions.
- Claims are stored separately from documents.
- Evidence is stored separately from interpretation.
- Current accepted state is derived from versioned knowledge.
- Planner authority is separated from scheduler authority.
- Agent output is validated before becoming accepted knowledge.
- Shared writes use a controlled commit path.
- Model and tool concurrency is bounded.
- Every consequential action has provenance and authority.
- Infrastructure is added in response to measured needs.

## 27. Open design questions

These choices depend on the target domain and should be revisited as the system develops:

- Which first competency questions create enough value to justify the system?
- Which knowledge requires formal human approval?
- What confidence model should claims use?
- How should disagreements and contradictory evidence be represented?
- Which relationships require temporal validity?
- Which data is too sensitive for model context?
- When should an agent propose versus execute follow-up work?
- Which work should be deterministic rather than agentic?
- What is the correct unit of a cohort?
- When does a graph database become necessary?
- Which evaluations predict real user value?
- Who owns ontology changes?
- How will old schemas and contexts be replayed?
- What are acceptable cost, latency, and failure thresholds?

## 28. Standards and references

### Agent frameworks and platforms

- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- Google Agent Development Kit: https://google.github.io/adk-docs/
- LangGraph: https://docs.langchain.com/oss/python/langgraph/
- Microsoft AutoGen: https://microsoft.github.io/autogen/
- PydanticAI: https://ai.pydantic.dev/
- OpenHands: https://docs.openhands.dev/
- Factory Missions: https://docs.factory.ai/missions/overview
- Cognition, "Multi-Agents: What's Actually Working": https://cognition.com/blog/multi-agents-working

### Orchestration and infrastructure

- Temporal: https://docs.temporal.io/
- AWS Step Functions Distributed Map: https://docs.aws.amazon.com/step-functions/latest/dg/state-map-distributed.html
- AWS SQS at-least-once delivery: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html
- Amazon Bedrock quotas: https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html
- E2B sandboxes: https://e2b.dev/

### Knowledge, ontology, and lineage

- W3C PROV-O provenance ontology: https://www.w3.org/TR/prov-o/
- W3C SHACL graph validation: https://www.w3.org/TR/shacl/
- CloudEvents: https://cloudevents.io/
- OpenLineage: https://openlineage.io/docs/

### Observability and evaluation

- OpenTelemetry: https://opentelemetry.io/docs/
- LangSmith observability: https://docs.langchain.com/langsmith/observability
- Arize Phoenix: https://phoenix.arize.com/
- Braintrust: https://www.braintrust.dev/

## Final summary

The scalable unit is not an agent conversation. It is a typed work item executed against a reproducible context and committed through a governed knowledge pipeline.

The ontology gives the system a shared language. The task ledger gives it coordination. The knowledge repository gives it memory. The context compiler gives each agent the right bounded view. Validation gives the system trust. Durable workflows, queues, workers, gateways, and observability allow the same design to grow without changing its core model.

The first serious implementation should optimize for correctness, provenance, inspectability, and useful knowledge reuse. Scale becomes valuable only after those properties exist.
