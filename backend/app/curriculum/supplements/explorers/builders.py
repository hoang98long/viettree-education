"""Small age-aware lessons, explicit teaching goals and self-contained exercises."""

from copy import deepcopy

from app.curriculum.builders import choice


def pick(prompt, correct, wrong, explanation):
    options = [correct, *wrong]
    offset = sum(map(ord, prompt)) % len(options)
    options = options[offset:] + options[:offset]
    return choice(prompt, options, options.index(correct), explanation, difficulty=2)


def cards(*labels):
    return {
        "kind": "cards",
        "labels": list(labels),
        "caption": "Nhìn thẻ tranh rồi đọc từng ý ngắn cùng người hướng dẫn.",
    }


def unit(
    grade,
    topic,
    code,
    title,
    goal,
    teaching,
    example,
    remember,
    hints,
    figure,
    questions,
    *,
    vip=False,
    context="",
):
    questions = deepcopy(questions)
    if context:
        for question in questions:
            question["content"]["prompt"] = context + "\n\n" + question["content"]["prompt"]
    return {
        "topic": topic,
        "code": "explorers-2026-01-" + code,
        "title": title,
        "minimum_plan_code": "vip" if vip else "free",
        "learning_level": "advanced" if vip else "reinforcement",
        "sort_order": 220,
        "lesson": {
            "title": title,
            "estimated_minutes": 6 if grade <= 2 else 8,
            "content": {
                "category": "thinking" if vip else "core",
                "goals": [goal],
                "blocks": [
                    {"type": "text", "title": "Cùng khám phá", "text": teaching},
                    {"type": "example", "title": "Thử một ví dụ", "text": example},
                    {"type": "remember", "title": "Mẹo của em", "text": remember},
                ],
                "hints": hints,
                "free_hint_count": 1,
                "reflection": ["Em thử nói một điều vừa khám phá nhé."],
                "illustration": figure,
            },
        },
        "questions": questions,
    }
