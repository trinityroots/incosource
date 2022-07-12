import pytest
from pytest_tr_odoo.fixtures import env
from odoo import fields


@pytest.fixture
def model(env):
    return env['res.config.settings']


@pytest.fixture
def company(env):
    company = env.company
    company .write({'authorized_signature': '1234'})
    return company


@pytest.fixture
def config(model):
    return model.create({})


def test_set_values(config):
    config.write({
        'authorized_signature': '1234'
    })

    config.set_values()
    assert config.authorized_signature.decode('ascii') == '1234'


@pytest.fixture
def config_param(env):
    return env['ir.config_parameter']


def test_get_values(config, config_param):
    config_param.set_param(
        'ics_account_ext.authorized_signature', '1234'
    )
    res = config.get_values()
    assert res['authorized_signature'] == '1234'
