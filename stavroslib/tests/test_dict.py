from stavroslib.dict import merge_dicts


def test_merge_dicts():
    d1 = {"name": "Stavros"}
    d2 = {"last": "Pitoglou"}
    assert merge_dicts(d1, d2) == {"name": "Stavros", "last": "Pitoglou"}


def test_merge_dicts_empty_first():
    d1 = {}
    d2 = {"key": "value"}
    assert merge_dicts(d1, d2) == {"key": "value"}


def test_merge_dicts_empty_second():
    d1 = {"key": "value"}
    d2 = {}
    assert merge_dicts(d1, d2) == {"key": "value"}


def test_merge_dicts_both_empty():
    assert merge_dicts({}, {}) == {}


def test_merge_dicts_overlapping_keys():
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}
    result = merge_dicts(d1, d2)
    assert result == {"a": 1, "b": 3, "c": 4}  # d2 overwrites d1
