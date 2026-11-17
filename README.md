# tdd-ping-pong: Roommate Expense Splitter

You're asked to build a tiny Splitwise. The core functionality is pretty simple:
people record who paid for what, and we tell them how they owe their roommate. 

## Setup

```bash
git clone https://github.com/Algo-Group-UChicago/tdd-ping-pong.git
cd tdd-ping-pong
git switch -c pair/alice-bob # use your actual name
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
```

You should see **7 passed**. If you don't, ask for help before you start.

When you write tests, **always** inject `FakeClock` and `InMemoryStorage`. See
`test_an_added_expense_is_stored_with_the_clocks_current_time` in `tests/test_ledger.py`

## The activity: TDD ping-pong

1. **A** writes **one** small failing test. Run `pytest` and confirm it fails *for the
   reason you expect* (not an `ImportError` or a typo).
2. **B** writes the **simplest** code that makes it pass. Run `pytest`, and make sure everything is green.
3. Commit: `git add -A && git commit -m "<message>"`.
4. Push: `git push -u origin pair/<personA>-<personB>`
5. **B** now writes the next failing test, and **A** makes it pass. Keep swapping.

Add as many features as you can. What those features actually do is up to you, but all behavior should support the intended use case above. Each test should then check **one** behavior.

## Suggested Features

1. **Balances.** `ledger.balances()` returns each person's net position in cents, as a
   `dict[str, int]`. Positive means they are owed money, negative means they owe.
   - Alice pays 3000 for alice and bob. Then alice is +1500 and bob is -1500.
   - The payer doesn't have to be a participant.
   - Several expenses add together.
2. **Expenses since a time.** `ledger.expenses_since(dt)` returns expenses whose timestamp is
   at or after `dt`.
3. **Saving.** Every `add_expense` saves the whole ledger through `storage.save(...)`.
   - `Ledger` converts each `Expense` to a dict. Hint: JSON has no `datetime`, so look at
     `datetime.isoformat()` and `datetime.fromisoformat()`.
   - `InMemoryStorage.save_calls` lets you assert that a save happened.
   - What should happen when `storage` is `None`? You decide.
4. **Loading.** A new `Ledger` built with storage that already has records starts with
   those expenses.
5. **Settle up** `ledger.settle_up()` returns a list of `(from, to, cents)`
   payments that bring every balance to 0.

## Running tests

```bash
pytest                    # everything
pytest -x                 # stop at the first failure
pytest -k balances        # only tests whose name contains "balances"
pytest tests/test_ledger.py::test_expenses_are_returned_in_insertion_order
```
