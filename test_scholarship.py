import math
import runpy
from pathlib import Path

import pytest

from scholarship_system import Status, evaluate_scholarship


# --- TESTES FUNCIONAIS (REQUISITOS) ---

def test_approved_case():
    """Caso de APPROVED: Atende a todos os requisitos mínimos."""
    result = evaluate_scholarship(18, 8.5, 92.0, True, False)
    assert result.status == Status.APPROVED
    assert "Applicant meets all scholarship requirements." in result.reasons


@pytest.mark.parametrize(
    "age, gpa, att, courses, disc, expected_status",
    [
        (17, 8.5, 92.0, True, False, Status.MANUAL_REVIEW),
        (16, 8.5, 92.0, True, False, Status.MANUAL_REVIEW),
        (18, 6.9, 92.0, True, False, Status.MANUAL_REVIEW),
        (18, 7.0, 79.9, True, False, Status.MANUAL_REVIEW),
    ],
)
def test_manual_review_cases(age, gpa, att, courses, disc, expected_status):
    """Casos de MANUAL_REVIEW por idade, GPA ou frequência na faixa de revisão."""
    result = evaluate_scholarship(age, gpa, att, courses, disc)
    assert result.status == expected_status


@pytest.mark.parametrize("age, gpa, att, courses, disc, reason", [
    (15, 8.5, 92.0, True, False, "younger than the minimum"),  # Idade < 16
    (19, 5.0, 92.0, True, False, "GPA is below"),               # GPA < 6.0
    (19, 8.5, 70.0, True, False, "Attendance rate is below"),   # Frequência < 75%
    (19, 8.5, 92.0, False, False, "Required courses have not been completed"),
    (19, 8.5, 92.0, True, True, "Applicant has a disciplinary record"),
])
def test_rejected_reasons(age, gpa, att, courses, disc, reason):
    """Casos de REJECTED por motivos diferentes."""
    result = evaluate_scholarship(age, gpa, att, courses, disc)
    assert result.status == Status.REJECTED
    assert any(reason in r for r in result.reasons)


@pytest.mark.parametrize(
    "age, expected_status",
    [
        (15, Status.REJECTED),
        (16, Status.MANUAL_REVIEW),
        (17, Status.MANUAL_REVIEW),
        (18, Status.APPROVED),
    ],
)
def test_age_boundaries(age, expected_status):
    """Valida os limites de idade da regra de elegibilidade."""
    result = evaluate_scholarship(age, 8.5, 90.0, True, False)
    assert result.status == expected_status


@pytest.mark.parametrize("gpa, expected_status", [
    (5.9, Status.REJECTED),
    (6.0, Status.MANUAL_REVIEW),
    (6.9, Status.MANUAL_REVIEW),
    (7.0, Status.APPROVED),
])
def test_gpa_boundaries(gpa, expected_status):
    """Verifica valores de GPA nos limites exatos da regra de negócio."""
    result = evaluate_scholarship(19, gpa, 90.0, True, False)
    assert result.status == expected_status


@pytest.mark.parametrize("attendance_rate, expected_status", [
    (74.9, Status.REJECTED),
    (75.0, Status.MANUAL_REVIEW),
    (79.9, Status.MANUAL_REVIEW),
    (80.0, Status.APPROVED),
])
def test_attendance_boundaries(attendance_rate, expected_status):
    """Valida os limites de frequência de aprovação e revisão manual."""
    result = evaluate_scholarship(19, 8.5, attendance_rate, True, False)
    assert result.status == expected_status


@pytest.mark.parametrize(
    "age, gpa, attendance_rate, courses, disc, expected_reasons",
    [
        (
            15,
            5.8,
            60.0,
            False,
            True,
            [
                "Applicant is younger than the minimum age.",
                "GPA is below the minimum required.",
                "Attendance rate is below the minimum required.",
                "Required courses have not been completed.",
                "Applicant has a disciplinary record.",
            ],
        ),
        (
            16,
            6.4,
            78.0,
            True,
            False,
            [
                "Applicant is under 18 and requires manual review.",
                "GPA is in the manual review range.",
                "Attendance rate is in the manual review range.",
            ],
        ),
    ],
)
def test_multiple_reasons_are_reported(age, gpa, attendance_rate, courses, disc, expected_reasons):
    """Assegura que múltiplos motivos são retornados sem perder ordem nem critério."""
    result = evaluate_scholarship(age, gpa, attendance_rate, courses, disc)
    assert result.reasons == expected_reasons


# --- ENTRADAS INVÁLIDAS ---

@pytest.mark.parametrize(
    "age, gpa, attendance_rate, courses, disc, expected_message",
    [
        (-1, 8.5, 90.0, True, False, "Age must be a non-negative integer."),
        (18, -1.0, 90.0, True, False, "GPA must be between 0 and 10."),
        (18, 8.5, -1.0, True, False, "Attendance rate must be between 0 and 100."),
        (18, 8.5, 90.0, "yes", False, "has_required_courses must be a boolean."),
        (18, 8.5, 90.0, True, "False", "disciplinary_record must be a boolean."),
        ("18", 8.5, 90.0, True, False, "Age must be an integer."),
        (18, float("nan"), 90.0, True, False, "GPA must be a finite number."),
        (18, 8.5, float("inf"), True, False, "Attendance rate must be a finite number."),
    ],
)
def test_invalid_inputs(age, gpa, attendance_rate, courses, disc, expected_message):
    """As entradas inválidas devem ser rejeitadas com mensagens claras e consistentes."""
    with pytest.raises(ValueError, match=expected_message):
        evaluate_scholarship(age, gpa, attendance_rate, courses, disc)


def test_invalid_gpa_upper_bound():
    with pytest.raises(ValueError, match="GPA must be between 0 and 10"):
        evaluate_scholarship(20, 11.0, 90.0, True, False)


def test_invalid_attendance_upper_bound():
    with pytest.raises(ValueError, match="Attendance rate must be between 0 and 100"):
        evaluate_scholarship(20, 8.5, 110.0, True, False)


@pytest.mark.parametrize(
    "gpa, attendance_rate, expected_message",
    [
        (True, 90.0, "GPA must be a number between 0 and 10."),
        (8.5, True, "Attendance rate must be a number between 0 and 100."),
    ],
)
def test_numeric_types_must_be_numbers_not_bool(gpa, attendance_rate, expected_message):
    """Valores booleanos não devem ser aceitos como número em parâmetros numéricos."""
    with pytest.raises(ValueError, match=expected_message):
        evaluate_scholarship(18, gpa, attendance_rate, True, False)


@pytest.mark.parametrize(
    "value",
    [True, False, 0, 1, "yes", None],
)
def test_boolean_flags_are_strictly_validated(value):
    """Garantia adicional da robustez: flags booleanas devem obedecer ao tipo esperado."""
    if value is True or value is False:
        result = evaluate_scholarship(18, 8.5, 90.0, value, False)
        assert result.status in {Status.APPROVED, Status.REJECTED}
    else:
        with pytest.raises(ValueError, match="has_required_courses must be a boolean"):
            evaluate_scholarship(18, 8.5, 90.0, value, False)


def test_nan_and_inf_values_are_rejected():
    assert math.isnan(float("nan"))
    with pytest.raises(ValueError, match="GPA must be a finite number"):
        evaluate_scholarship(18, float("nan"), 90.0, True, False)
    with pytest.raises(ValueError, match="Attendance rate must be a finite number"):
        evaluate_scholarship(18, 8.5, float("inf"), True, False)


def test_main_entrypoint_runs_demo_evaluation():
    """Executa o script em modo __main__ para cobrir o bloco de execução demo."""
    namespace = runpy.run_path(str(Path(__file__).with_name("scholarship_system.py")), run_name="__main__")
    assert namespace["result"].status.value == "APPROVED"
    assert "Applicant meets all scholarship requirements." in namespace["result"].reasons