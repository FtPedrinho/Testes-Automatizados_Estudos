import math
from dataclasses import dataclass
from enum import Enum
from typing import List


class Status(Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    MANUAL_REVIEW = "MANUAL_REVIEW"


@dataclass(frozen=True)
class EvaluationResult:
    status: Status
    reasons: List[str]


def evaluate_scholarship(
    age: int,
    gpa: float,
    attendance_rate: float,
    has_required_courses: bool,
    disciplinary_record: bool
) -> EvaluationResult:
    _validate_inputs(
        age=age,
        gpa=gpa,
        attendance_rate=attendance_rate,
        has_required_courses=has_required_courses,
        disciplinary_record=disciplinary_record,
    )

    rejection_reasons = []
    review_reasons = []

    # Rule 1 - Age
    if age < 16:
        rejection_reasons.append("Applicant is younger than the minimum age.")
    elif age <= 17:
        review_reasons.append("Applicant is under 18 and requires manual review.")

    # Rule 2 - GPA
    if gpa < 6.0:
        rejection_reasons.append("GPA is below the minimum required.")
    elif gpa < 7.0:
        review_reasons.append("GPA is in the manual review range.")

    # Rule 3 - Attendance
    if attendance_rate < 75.0:
        rejection_reasons.append("Attendance rate is below the minimum required.")
    elif attendance_rate < 80.0:
        review_reasons.append("Attendance rate is in the manual review range.")

    # Rule 4 - Required courses
    if not has_required_courses:
        rejection_reasons.append("Required courses have not been completed.")

    # Rule 5 - Disciplinary record
    if disciplinary_record:
        rejection_reasons.append("Applicant has a disciplinary record.")

    # Final decision
    if rejection_reasons:
        return EvaluationResult(
            status=Status.REJECTED,
            reasons=rejection_reasons
        )

    if review_reasons:
        return EvaluationResult(
            status=Status.MANUAL_REVIEW,
            reasons=review_reasons
        )

    return EvaluationResult(
        status=Status.APPROVED,
        reasons=["Applicant meets all scholarship requirements."]
    )


def _validate_inputs(
    age: int,
    gpa: float,
    attendance_rate: float,
    has_required_courses: bool,
    disciplinary_record: bool,
) -> None:
    if isinstance(age, bool) or not isinstance(age, int):
        raise ValueError("Age must be an integer.")

    if age < 0:
        raise ValueError("Age must be a non-negative integer.")

    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise ValueError("GPA must be a number between 0 and 10.")

    if not math.isfinite(float(gpa)):
        raise ValueError("GPA must be a finite number.")

    if gpa < 0.0 or gpa > 10.0:
        raise ValueError("GPA must be between 0 and 10.")

    if isinstance(attendance_rate, bool) or not isinstance(attendance_rate, (int, float)):
        raise ValueError("Attendance rate must be a number between 0 and 100.")

    if not math.isfinite(float(attendance_rate)):
        raise ValueError("Attendance rate must be a finite number.")

    if attendance_rate < 0.0 or attendance_rate > 100.0:
        raise ValueError("Attendance rate must be between 0 and 100.")

    if not isinstance(has_required_courses, bool):
        raise ValueError("has_required_courses must be a boolean.")

    if not isinstance(disciplinary_record, bool):
        raise ValueError("disciplinary_record must be a boolean.")


if __name__ == "__main__":
    result = evaluate_scholarship(
        age=18,
        gpa=8.5,
        attendance_rate=92.0,
        has_required_courses=True,
        disciplinary_record=False
    )
    print(result)