"""Editorial structure and exact numeric answer formats for grade five."""

from decimal import Decimal
from fractions import Fraction

from app.curriculum.builders import blank, choice, lesson

FREE_LESSONS = {"MATH": 18, "VIETNAMESE": 15, "ENGLISH": 13}


def question_count(subject, index):
    return (
        4 if index < 8 else 8 if FREE_LESSONS[subject] <= index < FREE_LESSONS[subject] + 4 else 6
    )


def number_text(value):
    if isinstance(value, Fraction):
        return str(value)
    return (
        format(Decimal(str(value)), "f").rstrip("0").rstrip(".")
        if "." in str(value)
        else str(value)
    )


def numeric(prompt, answer, explanation, position, difficulty=2):
    label = number_text(answer)
    if position % 2:
        return blank(
            prompt + " (Điền số hoặc phân số tối giản, không ghi đơn vị.)",
            list(dict.fromkeys([label, label.replace(".", ",")])),
            explanation,
            difficulty,
        )
    wrong = [number_text(answer + 1), number_text(answer + 2)]
    options = [label.replace(".", ","), *[value.replace(".", ",") for value in wrong]]
    correct = position % 3
    options = options[-correct:] + options[:-correct] if correct else options
    return choice(prompt, options, correct, explanation, difficulty)


def text_questions(rows, context):
    """Rows contain prompt/correct/two distinct distractors/reason; rotate positions."""
    result = []
    for position, row in enumerate(rows):
        prompt, answer, wrong1, wrong2, explanation = row
        correct = position % 3
        options = [answer, wrong1, wrong2]
        options = options[-correct:] + options[:-correct] if correct else options
        result.append(
            choice("Ngữ liệu của bài:\n" + context + "\n\n" + prompt, options, correct, explanation)
        )
    return result


def language_unit(
    subject, index, topic, code, title, teaching, example, remember, hints, rows, *, reflection=None
):
    parsed = [tuple(field.strip() for field in row.split("|")) for row in rows.strip().splitlines()]
    if any(len(row) != 5 for row in parsed):
        raise ValueError(f"{code}: mỗi câu cần câu hỏi, đáp án, hai lựa chọn khác và giải thích")
    questions = text_questions(parsed, example)
    return unit(
        subject,
        index,
        topic,
        code,
        title,
        teaching,
        example,
        remember,
        hints,
        questions,
        reflection=reflection,
        illustration=dict(
            kind="reading", caption="Đọc ngữ liệu, tìm chi tiết và tự giải thích lựa chọn."
        ),
    )


def unit(
    subject,
    index,
    topic,
    code,
    title,
    teaching,
    example,
    remember,
    hints,
    questions,
    *,
    illustration=None,
    reflection=None,
):
    vip = index >= FREE_LESSONS[subject]
    if len(questions) != question_count(subject, index):
        raise ValueError(f"{code}: số câu không đúng cấu trúc biên soạn")
    item = lesson(title, teaching, example, remember)
    item["estimated_minutes"] = 15 if vip else 12
    item["content"].update(
        category="thinking" if vip else "core",
        goals=[
            "Thực hành: " + title,
            "Giải thích lựa chọn bằng phép tính hoặc chi tiết trong ngữ liệu.",
        ],
        hints=hints,
        free_hint_count=1,
        reflection=reflection
        or ["Em hãy giải thích một đáp án bằng dữ kiện của bài, rồi tự kiểm tra."],
        illustration=illustration,
    )
    return dict(
        topic=topic,
        code="g5-" + code,
        title=title,
        lesson=item,
        questions=questions,
        minimum_plan_code="vip" if vip else "free",
        learning_level="advanced" if vip else "basic",
        sort_order=30 + index,
    )
