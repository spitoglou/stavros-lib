from stavroslib.dict import merge_dicts


def test_merge_dicts():
    d1 = {'name': 'Stavros'}
    d2 = {'last': 'Pitogloy'}
    assert merge_dicts(d1, d2) == {'name': 'Stavros', 'last': 'Pitogloy'}
