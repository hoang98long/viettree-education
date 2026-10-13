from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import UUID

import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.api.routes.learning import accessibility
from app.db import db
from app.fixtures.development import seed
from app.schemas.learning import AccessibilityInput
from app.services.accessibility import merge_text_size, reading_preferences
from tests.test_concurrency import create_student

BASE = "/api/v1"


@pytest.mark.parametrize("options", [None, [], {}, {"text_size": "tiny"}, {"text_size": []}])
def test_old_or_invalid_preferences_have_safe_defaults(options):
    assert reading_preferences(options) == {
        "text_size": "comfortable",
        "text_size_by_device": {},
    }


def test_reading_preferences_ignore_unknown_keys_without_mutating_profile():
    options = {
        "text_size": "compact",
        "text_size_by_device": {
            "phone": "compact",
            "tablet": "large",
            "desktop": [],
            "tv": "large",
        },
        "reduced_motion": True,
    }
    assert reading_preferences(options) == {
        "text_size": "compact",
        "text_size_by_device": {"phone": "compact", "tablet": "large"},
    }
    assert options["text_size_by_device"]["tv"] == "large"
    merged = merge_text_size(options, "comfortable", "desktop")
    assert merged["reduced_motion"]
    assert merged["text_size_by_device"] == {
        "phone": "compact",
        "tablet": "large",
        "desktop": "comfortable",
    }
    assert options["text_size_by_device"]["desktop"] == []


@pytest.mark.parametrize(
    "payload",
    [
        {"text_size": "tiny"},
        {"text_size": "compact", "device_type": "tv"},
        {"text_size": "compact", "student_id": "another-student"},
        {"text_size": "compact", "text_size_by_device": {"phone": "compact"}},
    ],
)
def test_device_preference_input_rejects_unknown_size_device_and_extra_fields(payload):
    with pytest.raises(ValidationError):
        AccessibilityInput.model_validate(payload)


@pytest.mark.integration
def test_device_preferences_persist_independently_and_old_clients_still_work(logged_student, conn):
    client = logged_student
    uid = UUID(client.get(f"{BASE}/auth/me").json()["id"])
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update()
        .where(profiles.c.student_id == uid)
        .values(accessibility_options={"text_size": "large", "reduced_motion": True})
    )
    expected = {}
    for device, size in [("phone", "compact"), ("desktop", "comfortable"), ("tablet", "large")]:
        response = client.put(
            f"{BASE}/students/me/accessibility",
            json={
                "text_size": size,
                "device_type": device,
            },
        )
        assert response.status_code == 200, response.text
        expected[device] = size
        assert response.json() == {"text_size": "large", "text_size_by_device": expected}
    # Login/session and profile responses expose the same persisted preferences.
    for path in ["/auth/me", "/students/me/profile", "/students/me/dashboard"]:
        result = client.get(BASE + path).json()
        if path.endswith("/dashboard"):
            result = result["user"]
        assert result["text_size"] == "large"
        assert result["text_size_by_device"] == expected
    assert client.get(f"{BASE}/students/me/profile").json()["accessibility_options"] == {
        "text_size": "large",
        "text_size_by_device": expected,
        "reduced_motion": True,
    }
    # The legacy API updates the default without removing device overrides.
    response = client.put(f"{BASE}/students/me/accessibility", json={"text_size": "compact"})
    assert response.json() == {"text_size": "compact", "text_size_by_device": expected}
    for payload in [
        {"text_size": "compact", "device_type": "tv"},
        {"text_size": "compact", "device_type": "phone", "is_vip": True},
    ]:
        assert client.put(f"{BASE}/students/me/accessibility", json=payload).status_code == 422
    token = client.headers.pop("X-CSRF-Token")
    assert (
        client.put(
            f"{BASE}/students/me/accessibility",
            json={
                "text_size": "large",
                "device_type": "phone",
            },
        ).status_code
        == 403
    )
    client.headers["X-CSRF-Token"] = token
    assert client.get(f"{BASE}/auth/me").json()["text_size_by_device"]["phone"] == "compact"
    assert client.post(f"{BASE}/auth/logout").status_code == 200
    assert (
        client.put(
            f"{BASE}/students/me/accessibility",
            json={
                "text_size": "large",
                "device_type": "phone",
            },
        ).status_code
        == 401
    )


@pytest.mark.integration
def test_concurrent_device_saves_merge_instead_of_overwriting(test_engine):
    with test_engine.begin() as conn:
        db.load(conn)
        seed(conn)
        user = create_student(conn)
        profiles = db.table("student_profiles")
        conn.execute(
            profiles.update()
            .where(profiles.c.student_id == user["id"])
            .values(accessibility_options={"reduced_motion": True, "text_size": "comfortable"})
        )
    barrier = Barrier(2)

    def save(values):
        barrier.wait(timeout=10)
        with test_engine.begin() as conn:
            return accessibility(AccessibilityInput(**values), user=user, conn=conn)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(
            pool.map(
                save,
                [
                    {"text_size": "compact", "device_type": "phone"},
                    {"text_size": "large", "device_type": "desktop"},
                ],
            )
        )
    assert len(results) == 2
    with test_engine.connect() as conn:
        options = conn.execute(
            select(profiles.c.accessibility_options).where(profiles.c.student_id == user["id"])
        ).scalar_one()
    assert options == {
        "reduced_motion": True,
        "text_size": "comfortable",
        "text_size_by_device": {"phone": "compact", "desktop": "large"},
    }
