import pytest
from mixer.backend.django import mixer
from myapp.models import Transaction
@pytest.mark.django_db
class TestModels:

    def test_credit_amount_transaction(self):
        product=mixer.blend('myapp.Transaction',credit_amount=1)
        assert product.is_credit_amount==True