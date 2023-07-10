from webapp.spimex.spimex_parser import convert_empty_strings, get_url_to_spimex_data, download_file_from_spimex
import pytest
from unittest.mock import patch


def test__convert_empty_strings__success_return_none_for_value_is_dash():
    assert convert_empty_strings('-') is None


def test__convert_empty_strings__return_string_when_value_is_not_dash():
    assert convert_empty_strings('abc') == 'abc'


@pytest.mark.parametrize(
    ('date, expected'),
    [
        ('20230707', 'https://spimex.com/upload/reports/oil_xls/oil_xls_20230707162000.xls'),
        ('20230705', 'https://spimex.com/upload/reports/oil_xls/oil_xls_20230705162000.xls')
    ]
)
def test__get_url_to_spimex_data(date, expected):
    assert get_url_to_spimex_data(date) == expected


def test__download_file_from_spimex__success(make_request_response):
    value = 'some value'
    with patch('webapp.spimex.spimex_parser.requests.get') as requests_get_mock:
        requests_get_mock.return_value = make_request_response(value)
        assert download_file_from_spimex('some_url') == b'some value'


# TODO написать тест на возвращение объекта sheet.Sheet из байтов
def test__read_spimex_file__():
    pass

