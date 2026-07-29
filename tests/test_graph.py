"""End-to-end graph smoke tests."""
from pathlib import Path

from main_system import run_system


def test_full_pipeline_twenty_reviews():
    state = run_system(target_reviewers=20, max_rounds=5)
    assert state.terminated is True
    assert state.partial_output is False
    assert state.is_validated is True
    assert len(state.reviews) == 20
    reviews_dir = Path(__file__).resolve().parents[1] / "outputs" / "reviews"
    for i in range(1, 21):
        assert (reviews_dir / f"reviewer_{i:02d}.md").exists()
    assert (Path(__file__).resolve().parents[1] / "outputs" / "meta_analysis.md").exists()
    assert (Path(__file__).resolve().parents[1] / "outputs" / "final_report.md").exists()


def test_reviews_are_isolated_ids():
    state = run_system(target_reviewers=3, max_rounds=5)
    ids = [r["reviewer_id"] for r in state.reviews]
    assert ids == [1, 2, 3]
