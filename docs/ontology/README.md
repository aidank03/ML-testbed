# Factor ontology kernel

This directory contains the first machine-readable vocabulary for Factor's proposed multi-agent and governed-data extension.

- `factor-core.schema.json` validates one durable ontology object or relationship.
- `example-claim.json` demonstrates an atomic scientific claim with tags, verification state, and explicit evidence links.

The kernel is deliberately small and storage-neutral. It uses JSON Schema so it can be validated before a database or graph service is selected. Version `factor-ontology/0.1` is a design contract, not a migration of existing run folders.

## Validation

With a JSON Schema 2020-12 validator installed:

```sh
check-jsonschema --schemafile docs/ontology/factor-core.schema.json \
  docs/ontology/example-claim.json
```

At minimum, Python can verify that both files are valid JSON:

```sh
python -m json.tool docs/ontology/factor-core.schema.json >/dev/null
python -m json.tool docs/ontology/example-claim.json >/dev/null
```

## Evolution rules

- Add domain terms as separate versioned modules after competency questions require them.
- Do not reuse an identifier for a different meaning.
- Additive optional fields may remain within a compatible version; changed meaning or validation requires a new ontology version.
- Keep claims separate from their supporting artifacts and from decisions.
- Preserve superseded objects and relationships so prior contexts remain replayable.
