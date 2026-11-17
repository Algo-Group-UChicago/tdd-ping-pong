from splitter.storage import JsonFileStorage


def test_json_file_storage_round_trips_records(tmp_path):
    # Arrange
    storage = JsonFileStorage(tmp_path / "ledger.json")
    records = [
        {"payer": "alice", "amount_cents": 4500, "participants": ["alice", "bob"]},
        {"payer": "bob", "amount_cents": 1200, "participants": ["bob"]},
    ]

    # Act
    storage.save(records)
    loaded = storage.load()

    # Assert
    assert loaded == records


def test_load_on_a_file_that_does_not_exist_yet_returns_an_empty_list(tmp_path):
    # Arrange
    storage = JsonFileStorage(tmp_path / "does-not-exist.json")

    # Act
    loaded = storage.load()

    # Assert
    assert loaded == []
