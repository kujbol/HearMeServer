import pytest
from flask.json import loads
from mock import patch

from hear_me.models.user import User
from hear_me.views.schemas.next_user import NextUserSchema


@pytest.mark.usefixtures('mongo')
@patch.object(User, 'get_next_user_id', autospec=True)
def test_get_next_user(
        mock_get_next_user_id, fixt_user, app, fixt_service_registry
):
    mock_get_next_user_id.return_value = fixt_user.id
    fixt_user.save()

    response = app.get('v1/next_user', headers={'token': 'fake token'})
    json = loads(response.data)

    expected_result = NextUserSchema().serialize(fixt_user.to_dict())
    assert json == expected_result
    assert response.status_code == 200
