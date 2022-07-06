import pytest
from pytest_tr_odoo.fixtures import env
from odoo import fields


@pytest.fixture
def model(env):
    return env['res.company']


@pytest.mark.parametrize('test_input,expected', [
    ({'name': 'Test Company 1'},
     {'name': 'Test Company 1'}),
])
def test_write(env, model, test_input, expected):
    res = model.create({
        'name': test_input.get('name'),
        'currency_id': env.ref('base.USD').id
    })
    assert res.name == expected.get('name')
