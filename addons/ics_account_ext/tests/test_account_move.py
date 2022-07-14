import pytest
from pytest_tr_odoo.fixtures import env
from odoo import fields


@pytest.fixture
def model(env):
    return env['account.move']


@pytest.fixture
def product(env):
    return env['product.product'].create({
        'name': 'Mini Fan'
    })


@pytest.fixture
def account_type(env):
    return env['account.account.type'].create({
        'name': 'Test Type',
        'type': 'other',
        'internal_group': 'income',
    })


@pytest.fixture
def account_id(env, account_type):
    return env['account.account'].create({
        'code': '4001',
        'name': 'Test Account',
        'user_type_id': account_type.id
    })


@pytest.fixture
def account_receivable(env, account_type):
    return env['account.account'].create({
        'code': '1000',
        'name': 'Test Receivable Account',
        'user_type_id': account_type.id
    })


@pytest.fixture
def account_payable(env, account_type):
    return env['account.account'].create({
        'code': '2000',
        'name': 'Test Payable Account',
        'user_type_id': account_type.id
    })


@pytest.fixture
def payment_term(env):
    return env['account.payment.term'].create({
        'name': 'the 15th of the month, min 31 days from now',
        'line_ids': [
                (0, 0, {
                    'value': 'balance',
                    'days': 31,
                    'day_of_the_month': 15,
                    'option': 'day_after_invoice_date',
                }),
        ],
    })


@pytest.fixture
def partner(env, payment_term, account_receivable, account_payable):
    return env['res.partner'].create({
        'name': 'Your Supplier',
        'email': 'supplier@other.company.com',
        'supplier_rank': 10,
        'company_id': 1,
        'property_payment_term_id': payment_term.id,
        'property_account_receivable_id': account_receivable.id,
        'property_account_payable_id': account_payable.id
    })


@pytest.fixture
def invoice(
        model,
        product,
        partner,
        account_id):
    return model.create({
        "partner_id": partner.id,
        "move_type": "out_invoice",
        "invoice_line_ids": [(0, 0, {
            'product_id': product.id,
            'name': product.name,
            'quantity': 10,
            'price_unit': product.lst_price,
            'account_id': product.property_account_income_id.id if
            product.property_account_income_id.id else account_id.id
        })],
    })


@pytest.mark.parametrize('test_input,expected', [
    ({'amount': 100.00},
     {'name': 'One Hundred Dollars'}),
    ({'amount': 100.00,
      'currency_name': 'THB'},
     {'name': 'หนึ่งร้อยบาทถ้วน'}),
])
def test_amount_baht_text(env, model, invoice, test_input, expected):
    if test_input.get('currency_name'):
        invoice.currency_id.name = test_input.get('currency_name')
    res = invoice.amount_baht_text(test_input.get('amount'))
    assert res == expected.get('name')
