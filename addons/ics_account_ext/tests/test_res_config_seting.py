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


def test_set_values(config, company):
    assert config.authorized_signature == company.authorized_signature
