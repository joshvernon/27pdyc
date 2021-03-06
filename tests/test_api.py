import pytest
import api as service

@pytest.fixture
def api():
    return service.api

### Testing "/years"

def test_2037_is_in_years_collection(api):
    r = api.requests.get('/years?payday=2018-01-11')
    assert 2037 in r.json()['paydayLeapYears']

def test_non_default_count(api):
    r = api.requests.get('/years?payday=2018-01-11&count=10')
    assert len(r.json()['paydayLeapYears']) == 10

def test_non_default_start_year(api):
    r = api.requests.get('/years?payday=2018-01-11&startYear=1992')
    assert 2004 in r.json()['paydayLeapYears']

### Testing "/years/{year}"

def test_thursday_2015_biweekly_is_true(api):
    r = api.requests.get('/years/2015?payday=2018-01-11')
    assert r.json()['isPaydayLeapYear'] is True

def test_thursday_2020_weekly(api):
    r = api.requests.get('/years/2020?payday=2018-01-11&frequency=weekly')
    assert r.json()['isPaydayLeapYear'] is True

def test_default_parameters(api):
    r = api.requests.get('/years/2018')
    assert r.status_code == 200

def test_valid_request_has_no_error_returned(api):
    r = api.requests.get('/years/2015?payday=2018-01-11')
    with pytest.raises(KeyError):
        r.json()['error']

def test_extraneous_query_params_have_no_effect(api):
    r = api.requests.get('/years/2015?payday=2018-01-11&foo=bar&baz=hello')
    assert r.json()['isPaydayLeapYear'] is True

### Exception tests

def test_invalid_year_returns_400(api):
    r = api.requests.get('/years/foo')
    assert r.status_code == 400

def test_invalid_year_error_message(api):
    r = api.requests.get('/years/foo')
    assert r.json()['error'] == 'Invalid parameter value'

def test_invalid_payday_format_returns_400(api):
    r = api.requests.get('/years/2015?payday=01/11/2018')
    assert r.status_code == 400

def test_invalid_payday_format_years_resource(api):
    r = api.requests.get('/years?payday=01/11/2018')
    assert r.status_code == 400

def test_post_year_resource_returns_405(api):
    r = api.requests.post('/years/2020?payday=2018-01-11&frequency=weekly')
    assert r.status_code == 405
