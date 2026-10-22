from baselines import run


def test_table_has_a_row_per_system_between_the_markers():
    fake = {"score": 2.5, "delivered": 0.9, "last": 11.75, "half": 10.5, "by14": 0.9, "vehicles": 2, "driver_hours": 0.0}
    text = run.table([[fake] * len(run.SYSTEMS)] * 3, workers=4, minutes=2.5)
    assert text.startswith(run.START) and text.endswith(run.END)
    rows = [line for line in text.splitlines() if line.startswith("| ") and "system" not in line]
    assert len(rows) == len(run.SYSTEMS)
    assert "| 2.50 h | 90% | 11:45 | 10:30 | 90% | 2.0 " in rows[0]
    assert "2.5 minutes on 4 workers" in text
