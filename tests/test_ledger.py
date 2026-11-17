from datetime import datetime, timedelta

import pytest

from splitter.ledger import Ledger
from tests.fakes import FakeClock


def test_an_added_expense_is_stored_with_the_clocks_current_time():
    # Arrange
    clock = FakeClock(datetime(2026, 9, 1, 18, 30))
    ledger = Ledger(clock=clock)

    # Act
    expense = ledger.add_expense(
        payer="alice",
        amount_cents=4500,
        participants=["alice", "bob", "carol"],
        description="pizza",
    )

    # Assert
    assert expense.timestamp == datetime(2026, 9, 1, 18, 30)
    assert ledger.expenses == [expense]


def test_expenses_are_returned_in_insertion_order():
    # Arrange
    clock = FakeClock(datetime(2026, 9, 1, 9, 0))
    ledger = Ledger(clock=clock)

    # Act
    ledger.add_expense("alice", 1200, ["alice", "bob"], "groceries")
    clock.advance(timedelta(hours=1))
    ledger.add_expense("bob", 3000, ["alice", "bob"], "internet")
    clock.advance(timedelta(hours=1))
    ledger.add_expense("alice", 800, ["alice", "bob"], "dish soap")

    # Assert
    descriptions = [e.description for e in ledger.expenses]
    assert descriptions == ["groceries", "internet", "dish soap"]


def test_add_expense_rejects_an_empty_participants_list():
    # Arrange
    ledger = Ledger(clock=FakeClock(datetime(2026, 9, 1)))

    # Act / Assert
    with pytest.raises(ValueError):
        ledger.add_expense("alice", 1000, [], "mystery charge")


@pytest.mark.parametrize("amount_cents", [0, -500])
def test_add_expense_rejects_a_non_positive_amount(amount_cents):
    # Arrange
    ledger = Ledger(clock=FakeClock(datetime(2026, 9, 1)))

    # Act / Assert
    with pytest.raises(ValueError):
        ledger.add_expense("alice", amount_cents, ["alice", "bob"], "refund?")
