import pytest
from pytest_tr_odoo.fixtures import env
from odoo import fields


@pytest.fixture
def model(env):
    return env['sale.report']


@pytest.fixture
def crm(env):
    return env['crm.team'].create({'name': 'Test Crm'})


@pytest.fixture
def sale_office(env):
    return env['sale.office'].create({'name': 'Test Office'})


@pytest.fixture
def distribution(env):
    return env['distribution'].create({'name': 'Test Distribution'})


@pytest.fixture
def partner_industry(env):
    return env['res.partner.industry'].create(
        {
            'name': 'Test industry',
            'full_name': 'Test industry',
            'active': True,
        }
    )


@pytest.fixture
def partner2(env):
    return env.ref('base.res_partner_2')


@pytest.fixture
def partner4(env):
    return env.ref('base.res_partner_4')


@pytest.fixture
def sale_order1(env):
    return env.ref('sale.sale_order_1')


@pytest.mark.parametrize('test_input,expected', [
    ({'fields': None},
     {'fields': 'sale_office_id'}),
    ({'fields': {'sale_office_id': 'sale_office_id'}},
     {'name': 'sale_office_id'}),
])
def test__select_sale(model, test_input, expected):
    res = model._select_sale(fields=test_input.get('fields'))
    assert 'sale_office_id' in res


def test_from_sale(env, model):
    res = model._from_sale(from_clause='')
    assert 'distribution' in res


def test__group_by_sale(model):
    res = model._group_by_sale(groupby='')
    assert 's.sale_office_id' in res


@pytest.mark.parametrize('test_input,expected', [
    ({'fields': None},
     {'fields': 'sale_office_id'}),
    ({'fields': {'sale_office_id': 'sale_office_id'}},
     {'name': 'sale_office_id'}),
])
def test__select_pos(model, test_input, expected):
    res = model._select_pos(fields=test_input.get('fields'))
    assert 'sale_office_id' in res
