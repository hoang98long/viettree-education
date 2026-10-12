"""Editorial helpers for original grade-three lessons, not generated textbook copies."""

from app.curriculum import blank, choice, lesson, multiple, ordering


def unit(
    topic,
    code,
    title,
    teaching,
    example,
    remember,
    hints,
    rows,
    *,
    vip=False,
    thinking=False,
    numeric=False,
    illustration=None,
):
    questions = []
    for position, row in enumerate(rows.strip().splitlines()):
        fields = [value.strip() for value in row.split("|")]
        if fields[0] == "ORDER":
            _, prompt, parts, order, explanation = fields
            question = ordering(
                prompt, parts.split("~"), [int(i) for i in order.split("~")], explanation
            )
        elif fields[0] == "MULTI":
            _, prompt, parts, correct, explanation = fields
            question = multiple(
                prompt, parts.split("~"), [int(i) for i in correct.split("~")], explanation
            )
        elif numeric:
            prompt, answer, explanation = fields
            value = int(answer)
            if position % 2:
                options = [str(value + 1), answer, str(value + 10)]
                question = choice(prompt, options, 1, explanation, 3 if vip else 2)
            else:
                question = blank(prompt + " (Chỉ điền số.)", [answer], explanation, 3 if vip else 2)
        else:
            prompt, answer, wrong1, wrong2, explanation = fields
            # Rotate correct positions; text answers occur only when a unique word is requested.
            if prompt.startswith("Điền từ:"):
                question = blank(prompt, [answer], explanation, 3 if vip else 2)
            else:
                options = [answer, wrong1, wrong2]
                correct = position % 3
                options = options[-correct:] + options[:-correct] if correct else options
                question = choice(prompt, options, correct, explanation, 3 if vip else 2)
        if not numeric:
            question["content"]["prompt"] = (
                "Ngữ liệu của bài:\n" + example + "\n\n" + question["content"]["prompt"]
            )
        questions.append(question)
    item = lesson(title, teaching, example, remember)
    item["content"].update(
        category="thinking" if thinking else "core",
        goals=["Hiểu và thực hành: " + title, "Giải thích cách làm bằng một ví dụ của em."],
        hints=hints.split("|"),
        free_hint_count=1,
        reflection=["Em hãy kể một tình huống có thể dùng điều vừa học và giải thích cách làm."],
        illustration=illustration,
    )
    return {
        "topic": topic,
        "code": "g3-" + code,
        "title": title,
        "lesson": item,
        "questions": questions,
        "minimum_plan_code": "vip" if vip else "free",
        "learning_level": "advanced" if vip else "basic",
        "sort_order": 30,
    }
