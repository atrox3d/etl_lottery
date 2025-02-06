from dbhelpers import querybuilder as qb


BIND_PARAM = '?'


def test_simple_select_no_params():
    query = 'select * from table'
    sql, params = qb.query_builder(
        query,
    )
    print(f'{sql = }')
    print(f'{params = }')
    assert query == sql
    assert params == {}


def test_simple_select_one_param():
    query = 'select * from table'
    sql, params = qb.query_builder(
        query,
        name='bob'
    )
    print(f'{sql = }')
    print(f'{params = }')
    assert sql == f'{query} WHERE name = :name'
    assert params == {'name': 'bob'}


def test_simple_select_two_params():
    query = 'select * from table'
    sql, params = qb.query_builder(
        query,
        name='bob',
        age=10
    )
    print(f'{sql = }')
    print(f'{params = }')
    assert sql == f'{query} WHERE name = :name AND age = :age'
    assert params == {'name': 'bob', 'age': 10}


def test_simple_select_with_one_param_like():
    query = 'select * from table'
    sql, params = qb.query_builder(
        query,
        name__like='bob',
    )
    print(f'{sql = }')
    print(f'{params = }')
    assert sql == f'{query} WHERE name like :name'
    assert params == {'name': '%bob%'}


def test_simple_select_with_one_param_and_one_like():
    query = 'select * from table'
    sql, params = qb.query_builder(
        query,
        name__like='bob',
        age=10
    )
    print(f'{sql = }')
    print(f'{params = }')
    assert sql == f'{query} WHERE name like :name AND age = :age'
    assert params == {'name': '%bob%', 'age': 10}
