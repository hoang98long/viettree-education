"""Authoring helpers for the independently versioned applied-2026-01 pack."""

from app.curriculum.builders import choice


def unit(
    grade,
    topic,
    code,
    title,
    teaching,
    example,
    remember,
    hints,
    figure,
    rows,
    *,
    vip=False,
    context="",
):
    questions = []
    for index, (prompt, answer, distractors, explanation) in enumerate(rows):
        options = [answer, *distractors]
        offset = (grade + index) % len(options)
        options = options[offset:] + options[:offset]
        questions.append(
            choice(
                (context + "\n\n" if context else "") + prompt,
                options,
                options.index(answer),
                explanation,
                difficulty=3 if vip else 1,
            )
        )
    return {
        "topic": topic,
        "code": "applied-2026-01-" + code,
        "title": title,
        "minimum_plan_code": "vip" if vip else "free",
        "learning_level": "advanced" if vip else "reinforcement",
        "sort_order": 200 if not vip else 201,
        "lesson": {
            "title": title,
            "estimated_minutes": (7 if vip else 5) if grade <= 2 else (10 if vip else 7),
            "content": {
                "category": "thinking" if vip else "core",
                "goals": [title, "Chọn câu trả lời và thử nói vì sao."],
                "blocks": [
                    {"type": "text", "title": "Cùng khám phá", "text": teaching},
                    {"type": "example", "title": "Xem một ví dụ", "text": example},
                    {"type": "remember", "title": "Mẹo của em", "text": remember},
                ],
                "hints": hints,
                "free_hint_count": 1,
                "reflection": ["Em thử kể một ví dụ tương tự ở nhà hoặc ở lớp nhé."],
                "illustration": figure,
            },
        },
        "questions": questions,
    }


def cards(*labels):
    return {
        "kind": "cards",
        "labels": list(labels),
        "caption": "Nhìn các thẻ để nhớ những ý chính của bài.",
    }
