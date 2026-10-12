"""Original short lessons for beginning readers; every exercise has an explicit answer."""

from app.curriculum import blank, choice, lesson, ordering

EXPECTED = {
    "MATH": {"topics": 8, "lessons": 25, "questions": 142, "assessments": 21},
    "VIETNAMESE": {"topics": 6, "lessons": 23, "questions": 130, "assessments": 19},
    "ENGLISH": {"topics": 7, "lessons": 20, "questions": 112, "assessments": 16},
}
FREE_LESSONS = {"MATH": 18, "VIETNAMESE": 15, "ENGLISH": 13}


def cards(labels, caption):
    return {"kind": "cards", "labels": labels, "caption": caption}


def counters(count):
    return {
        "kind": "counters",
        "count": count,
        "caption": f"Có {count} chấm tròn; chạm hoặc chỉ vào từng chấm để đếm.",
    }


def build(
    grade,
    subject,
    index,
    topic,
    code,
    title,
    teaching,
    example,
    remember,
    hints,
    rows,
    *,
    illustration=None,
    thinking=False,
):
    vip = index >= FREE_LESSONS[subject]
    needed = 4 if index < 8 else (8 if vip and index < FREE_LESSONS[subject] + 4 else 6)
    questions, answers = [], []
    for position, row in enumerate(rows):
        if row[0] == "ORDER":
            _, prompt, parts, order, explanation = row
            question = ordering(prompt, parts, order, explanation, 2)
            answer = {"ordered_ids": [chr(97 + i) for i in order]}
        else:
            prompt, correct, wrong, explanation = row
            correct = str(correct)
            # Two choices for the first foundation lessons; three after guided practice.
            distractors = [str(v) for v in wrong][: 1 if grade == 1 and index < 8 else 2]
            assert correct not in distractors and len(set(distractors)) == len(distractors)
            if subject == "MATH" and grade == 2 and position % 3 == 2 and correct.isdigit():
                question = blank(prompt + " (Điền số.)", [correct], explanation, 2 if vip else 1)
                answer = {"text": correct}
            else:
                options = [correct, *distractors]
                slot = position % len(options)
                options = options[-slot:] + options[:-slot] if slot else options
                question = choice(prompt, options, slot, explanation, 2 if vip else 1)
                answer = {"option_id": chr(97 + slot)}
            if subject != "MATH":
                question["content"]["prompt"] = example + "\n\n" + prompt
        questions.append(question)
        answers.append(answer)
    assert len(questions) == needed, (grade, subject, code, len(questions), needed)
    item = lesson(title, teaching, example, remember)
    item["estimated_minutes"] = 6 if grade == 1 else 8
    item["content"].update(
        category="thinking" if thinking else "core",
        goals=[title, "Chọn hoặc chỉ vào câu trả lời; nói một ý ngắn nếu em sẵn sàng."],
        hints=hints.split("|"),
        free_hint_count=1,
        reflection=["Em thử một lần với đồ vật thật hoặc nói cùng người thân."],
        illustration=illustration,
    )
    item["content"]["blocks"][-1]["text"] = (
        "Mỗi lần em làm 2–3 câu, rồi nghỉ nếu mỏi. Người lớn có thể đọc câu lệnh và giúp thao tác. Em được lưu bài để làm tiếp; không cần làm nhanh."
    )
    return dict(
        topic=topic,
        code=f"g{grade}-" + code,
        title=title,
        lesson=item,
        questions=questions,
        answer_examples=answers,
        minimum_plan_code="vip" if vip else "free",
        learning_level="reinforcement" if vip else "basic",
        sort_order=30 + index,
    )


def numeric(prompt, answer, explanation, maximum):
    nearby = [
        v
        for v in [answer + 1, answer - 1, answer + 2, answer - 2]
        if 0 <= v <= maximum and v != answer
    ]
    return prompt, answer, nearby[:2], explanation


def assemble(units, topics):
    core, extension = {}, {}
    for subject, items in units.items():
        core[subject] = []
        for index in range(0, 8, 2):
            first, second = items[index : index + 2]
            assert first["topic"] == second["topic"]
            core[subject].append(
                dict(
                    code=first["topic"],
                    title=topics[subject][first["topic"]],
                    lessons=[first["lesson"], second["lesson"]],
                    questions=first["questions"] + second["questions"],
                )
            )
        extension[subject] = items[8:]
    return core, extension
