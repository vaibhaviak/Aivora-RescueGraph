from rescuegraph import Household, Shock, simulate, detect_first_domino, compare_interventions

def household(**kwargs):
    data = dict(monthly_income=60000, starting_savings=90000,
                essential_expenses=30000, debt_payment=12000,
                discretionary_expenses=5000, salary_delay_months=1,
                horizon_months=3)
    data.update(kwargs)
    return Household(**data)

def test_salary_delay_and_shock():
    h = household()
    result = simulate(h, [Shock(amount=40000, month=1)])
    assert result["months"][0]["ending_balance"] == 3000
    assert result["months"][1]["ending_balance"] == 16000
    assert result["first_negative_month"] is None

def test_first_negative_month():
    h = household(starting_savings=10000, monthly_income=0,
                  essential_expenses=8000, debt_payment=5000,
                  discretionary_expenses=0, salary_delay_months=3)
    result = simulate(h)
    domino = detect_first_domino(result)
    assert domino["month"] == 1
    assert result["first_negative_month"] == 1

def test_intervention_comparison_has_four_scenarios():
    h = household()
    rows = compare_interventions(h, [Shock(amount=40000, month=1)],
                                 discretionary_reduction=2000, one_time_support=10000)
    assert len(rows) == 4
    assert rows[0]["scenario"] == "Selected stress scenario"
