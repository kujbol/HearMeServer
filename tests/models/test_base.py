import pytest
from mongoengine import StringField

from hear_me.models.base import BaseDocument


class TestBase(BaseDocument):
    id = StringField(primary_key=True)
    text = StringField()


@pytest.fixture
def fixt_base_document():
    return TestBase(id='1', text='test text')


def test_to_dict(fixt_base_document):
    assert fixt_base_document.to_dict() == {
        '_id': '1',
        'text': 'test text',
    }


@pytest.mark.usefixtures('mongo')
def test_get_by_id(fixt_base_document):
    fixt_base_document.save()
    result = TestBase.get_by_id('1')
    assert result == fixt_base_document
