import pytest
from pytest_tr_odoo.fixtures import env
from odoo import fields


@pytest.fixture
def model(env):
    return env['res.partner']


@pytest.mark.parametrize('test_input,expected', [
    ({'name': 'customer 1', 'customer_reference': 'customer 2'},
     {'name': 'customer 1', 'customer_reference': 'customer 2'}),
])
def test_create(model, test_input, expected):
    res = model.create({
        'name': test_input.get('name'),
        'customer_reference': test_input.get('customer_reference')
    })

    assert res.name == expected.get('name')
    assert res.customer_reference == expected.get('customer_reference')
