"""Verify Qdrant 1.7.3 768-dim Cosine batch upsert and semantic retrieval."""

from backend.core.stores import QDRANT_STORE, deterministic_embed_768


def test_qdrant_768d_batch_upsert_and_cosine_search() -> None:
    vec = deterministic_embed_768("Mach effect piezoelectric propulsion")
    assert len(vec) == 768

    docs = QDRANT_STORE.upsert_batch(
        [
            ("engineering", "Woodward Piezo Stack Test", "36.4 kHz PZT-8 resonator thrust telemetry", "test://1"),
            ("legal", "Bilateral Treaty Lien", "OpenTimestamps anchored sovereign gazette filing", "test://2"),
        ]
    )
    assert len(docs) == 2
    assert all(d.vector_dim == 768 for d in docs)

    hits = QDRANT_STORE.search("36.4 kHz PZT-8 resonator thrust", tab="engineering", limit=3)
    assert len(hits) >= 1
    assert hits[0].cosine_score > 0.2
