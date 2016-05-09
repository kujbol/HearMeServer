from flask.json import loads, dumps

import pytest

from hear_me.views.schemas.settings import SettingsSchema


@pytest.mark.usefixtures('mongo')
def test_get_settings(fixt_user, app, fixt_service_registry):
    fixt_user.save()

    response = app.get('v1/settings', headers={'token': 'fake token'})
    json = loads(response.data)

    expected_result = SettingsSchema().serialize(fixt_user.to_dict())

    assert response.status_code == 200
    assert json['search_settings'] == expected_result['search_settings']
    assert json['search_preferences'] == expected_result['search_preferences']


@pytest.mark.usefixtures('mongo')
def test_post_settings(fixt_user, app, fixt_service_registry):
    fixt_user.save()

    json = {
        "search_preferences": {
            "age_range_low": 1,
            "age_range_top": 99,
            "genders": [
              "male",
              "female"
            ],
            "is_in_same_country": True,
            "languages": [
              "english",
              "germany",
            ]
        },
        "search_settings": {
            "gender": "male",
            "languages": [
              "english",
            ]
        }
    }

    response = app.post(
        'v1/settings', headers={'token': 'fake token'},
        data=dumps(json), content_type='application/json'
    )
    fixt_user.reload()
    assert response.status_code == 200

    expected_result = SettingsSchema().serialize(fixt_user.to_dict())

    assert response.status_code == 200
    assert json['search_settings'] == expected_result['search_settings']
    assert json['search_preferences'] == expected_result['search_preferences']


@pytest.mark.usefixtures('mongo')
@pytest.mark.parametrize('param_json, result', [
    (
        {}, {
            'schema_error': {
                'search_preferences': 'Required',
                'search_settings': 'Required'}
        }
    ),
])
def test_exception_post_settings(
        app, fixt_service_registry, param_json, result, fixt_user
):
    fixt_user.save()
    response = app.post(
        'v1/settings', headers={'token': 'fake token'},
        data=dumps(param_json), content_type='application/json'
    )
    json = loads(response.data)

    assert response.status_code == 400
    assert json == result
