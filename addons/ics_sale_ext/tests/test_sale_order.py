import pytest
from pytest_tr_odoo.fixtures import env
from odoo import fields


@pytest.fixture
def model(env):
    return env['sale.order']


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


def test_onchange_partner(
        env,
        sale_order1,
        sale_office,
        distribution,
        partner_industry,
        crm,
        partner4):
    partner4.write({
        'industry_id': partner_industry.id,
        'team_id': crm.id,
        'distribution_id': distribution.id,
        'sale_office_id': sale_office.id
    })
    sale_order1.partner_id = partner4.id
    sale_order1._onchange_partner()

    assert sale_order1.shop_type_id.id == partner_industry.id
    assert sale_order1.team_id.id == crm.id
    assert sale_order1.distribution_id.id == distribution.id
    assert sale_order1.sale_office_id.id == sale_office.id
