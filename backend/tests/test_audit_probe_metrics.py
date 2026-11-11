from uuid import uuid4

from scripts.load_probe import endpoint_label, endpoint_summary, percentile


def test_probe_metrics_keep_operation_but_remove_ids_and_query():
    first, second = uuid4(), uuid4()
    label = endpoint_label("put", f"/attempts/{first}/answers/{second}?token=private")
    assert label == "PUT /attempts/{id}/answers/{id}"
    assert str(first) not in label and "private" not in label
    assert endpoint_label("GET", "/students/me/skills") == "GET /students/me/skills"


def test_nearest_rank_percentile_retains_tail_in_small_samples():
    assert percentile([], 0.95) is None
    assert percentile([20, 10], 0.95) == 20
    assert percentile([5, 1, 2, 3, 4], 0.5) == 3
    assert percentile([5, 1, 2, 3, 4], 0.99) == 5


def test_endpoint_summary_counts_errors_without_merging_actions():
    rows = [
        ("GET /attempts/{id}", 10, 200),
        ("GET /attempts/{id}", 20, 503),
        ("POST /attempts/{id}/submit", 50, 200),
    ]
    result = endpoint_summary(rows)
    assert sum(row["requests"] for row in result.values()) == 3
    assert result["GET /attempts/{id}"]["status_counts"] == {200: 1, 503: 1}
    assert result["POST /attempts/{id}/submit"]["p95_ms"] == 50
