"""Mô phỏng nearest-neighbour: không gọi mô hình bên ngoài."""

from collections import Counter

from app.academy.media import OBJECTS

DATASET = [
    dict(
        id=f"sample-{i}",
        asset=f"card-{kind}-{i % 3}",
        label=label,
        features=[
            {"cat": 4, "dog": 4, "rabbit": 4, "bird": 2, "turtle": 4, "butterfly": 6, "cow": 4}.get(
                kind, 0
            ),
            int(kind in {"apple", "orange", "grape", "ball", "clock"}),
            int(
                kind
                in {
                    "apple",
                    "banana",
                    "orange",
                    "pear",
                    "grape",
                    "watermelon",
                    "pineapple",
                    "strawberry",
                }
            ),
            int(kind in {"bag", "cup", "scissors", "pencil"}),
            i % 3,
        ],
    )
    for i, (kind, name, label) in enumerate(OBJECTS)
]


def predict(training_ids, test_ids, features=(0, 1, 2, 3)):
    by_id = {row["id"]: row for row in DATASET}
    if (
        not training_ids
        or len(set(training_ids)) != len(training_ids)
        or set(training_ids) & set(test_ids)
    ):
        raise ValueError("Cần tập học khác tập thử, không trùng mẫu")
    if (
        not set(training_ids + test_ids) <= set(by_id)
        or not set(features) <= {0, 1, 2, 3, 4}
        or not features
    ):
        raise ValueError("Mẫu hoặc đặc điểm không hợp lệ")
    output = []
    for identifier in test_ids:
        target = by_id[identifier]
        distances = [
            (sum(abs(target["features"][f] - by_id[t]["features"][f]) for f in features), t)
            for t in training_ids
        ]
        distance = min(d for d, _ in distances)
        nearby = [by_id[t]["label"] for d, t in distances if d == distance]
        predicted = Counter(nearby).most_common(1)[0][0]
        output.append(
            dict(
                id=identifier,
                predicted=predicted,
                actual=target["label"],
                correct=predicted == target["label"],
                distance=distance,
                explanation="So đặc điểm với các ví dụ gần nhất. Thiếu nhóm hoặc chỉ dùng màu có thể gây nhầm; đây là thuật toán mô phỏng.",
            )
        )
    return output
