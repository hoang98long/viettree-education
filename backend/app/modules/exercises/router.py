from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.exercise import AttemptStatus, AnswerSubmission, Exercise, ExerciseAttempt, Question, QuestionOption
from app.models.learning import Student
from app.models.user import User
from app.modules.auth.router import get_current_user
from app.modules.exercises.schemas import ExerciseOut, ExerciseResult, ExerciseSummary, QuestionResult, SubmitExerciseRequest

router = APIRouter(prefix="/exercises", tags=["Bài tập"])


def _get_student(user: User, db: Session) -> Student:
    student = db.scalar(select(Student).where(Student.user_id == user.id))
    if not student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tài khoản chưa có hồ sơ học sinh")
    return student


def _exercise_payload(exercise: Exercise, db: Session) -> ExerciseOut:
    questions = db.scalars(
        select(Question).where(Question.exercise_id == exercise.id).order_by(Question.display_order)
    ).all()
    result_questions = []
    for question in questions:
        options = db.scalars(
            select(QuestionOption)
            .where(QuestionOption.question_id == question.id)
            .order_by(QuestionOption.display_order)
        ).all()
        result_questions.append({
            "id": question.id,
            "question_type": question.question_type.value,
            "question_text": question.question_text,
            "hint": question.hint,
            "difficulty": question.difficulty.value,
            "points": question.points,
            "display_order": question.display_order,
            "options": options,
        })
    return ExerciseOut(
        id=exercise.id,
        lesson_id=exercise.lesson_id,
        title=exercise.title,
        description=exercise.description,
        difficulty=exercise.difficulty.value,
        points=exercise.points,
        questions=result_questions,
    )


@router.get("/{exercise_id}", response_model=ExerciseOut)
def get_exercise(exercise_id: UUID, db: Session = Depends(get_db)):
    exercise = db.scalar(select(Exercise).where(Exercise.id == exercise_id, Exercise.is_active.is_(True)))
    if not exercise:
        raise HTTPException(status_code=404, detail="Bài tập không tồn tại")
    return _exercise_payload(exercise, db)


@router.get("", response_model=list[ExerciseSummary])
def list_exercises(lesson_id: UUID, db: Session = Depends(get_db)):
    exercises = db.scalars(
        select(Exercise)
        .where(Exercise.lesson_id == lesson_id, Exercise.is_active.is_(True))
        .order_by(Exercise.display_order, Exercise.title)
    ).all()
    return exercises


@router.post("/{exercise_id}/submit", response_model=ExerciseResult)
def submit_exercise(
    exercise_id: UUID,
    data: SubmitExerciseRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = _get_student(user, db)
    exercise = db.scalar(select(Exercise).where(Exercise.id == exercise_id, Exercise.is_active.is_(True)))
    if not exercise:
        raise HTTPException(status_code=404, detail="Bài tập không tồn tại")

    questions = db.scalars(select(Question).where(Question.exercise_id == exercise.id)).all()
    question_map = {question.id: question for question in questions}
    answer_map = {answer.question_id: answer for answer in data.answers}
    attempt = ExerciseAttempt(
        id=uuid4(),
        student_id=student.id,
        exercise_id=exercise.id,
        status=AttemptStatus.COMPLETED,
        max_score=sum(question.points for question in questions),
    )
    db.add(attempt)
    db.flush()

    results = []
    score = 0.0
    correct_count = 0
    for question in questions:
        answer = answer_map.get(question.id)
        selected = set(answer.selected_option_ids if answer else [])
        correct_options = set(db.scalars(
            select(QuestionOption.id).where(
                QuestionOption.question_id == question.id,
                QuestionOption.is_correct.is_(True),
            )
        ).all())
        is_correct = bool(answer) and selected == correct_options
        question_score = float(question.points if is_correct else 0)
        score += question_score
        correct_count += int(is_correct)
        db.add(AnswerSubmission(
            attempt_id=attempt.id,
            question_id=question.id,
            answer_text=answer.answer_text if answer else None,
            selected_option_ids=list(selected) if selected else None,
            is_correct=is_correct,
            score=question_score,
        ))
        results.append(QuestionResult(
            question_id=question.id,
            is_correct=is_correct,
            score=question_score,
            max_score=question.points,
            explanation=question.explanation if is_correct else question.hint,
        ))

    attempt.score = score
    db.commit()
    return ExerciseResult(
        attempt_id=attempt.id,
        score=score,
        max_score=float(attempt.max_score or 0),
        correct_count=correct_count,
        total_questions=len(questions),
        results=results,
    )
