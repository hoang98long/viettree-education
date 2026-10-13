"""Question and lesson primitives shared by all grades."""


def choice(prompt, options, correct, explanation, difficulty=2):
    return dict(
        question_type="single_choice",
        difficulty=difficulty,
        content={
            "prompt": prompt,
            "options": [{"id": chr(97 + i), "text": text} for i, text in enumerate(options)],
        },
        grading={"correct_option_id": chr(97 + correct)},
        explanation={"text": explanation},
    )


def multiple(prompt, options, correct, explanation, difficulty=3):
    result = choice(prompt, options, 0, explanation, difficulty)
    result.update(
        question_type="multiple_choice",
        grading={"correct_option_ids": [chr(97 + i) for i in correct]},
    )
    return result


def blank(prompt, accepted, explanation, difficulty=2):
    return dict(
        question_type="fill_blank",
        difficulty=difficulty,
        content={"prompt": prompt},
        grading={"accepted_answers": accepted},
        explanation={"text": explanation},
    )


def ordering(prompt, parts, order, explanation, difficulty=3):
    result = choice(prompt, parts, 0, explanation, difficulty)
    result.update(question_type="ordering", grading={"ordered_ids": [chr(97 + i) for i in order]})
    return result


def lesson(title, teaching, example, remember):
    return dict(
        title=title,
        content={
            "blocks": [
                {"type": "text", "title": "Cùng khám phá", "text": teaching},
                {"type": "example", "title": "Thử với ví dụ", "text": example},
                {"type": "remember", "title": "Em ghi nhớ", "text": remember},
                {
                    "type": "practice",
                    "title": "Tự luyện tập",
                    "text": "Hãy giải thích lại ví dụ bằng lời của em, rồi chọn bài luyện tập bên dưới. Đọc kỹ yêu cầu trước khi trả lời; em có thể lưu bài và quay lại.",
                },
            ]
        },
    )
