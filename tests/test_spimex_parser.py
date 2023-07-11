from webapp.spimex.spimex_parser import (convert_empty_strings, 
                                         get_url_to_spimex_data,
                                         download_file_from_spimex,
                                         delete_all_emty_values_from_raw_data,
                                         get_indexes_for_search_value,
                                         extract_value_from_string,
                                         make_strings_from_all_values
                                         )
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
def test__get_url_to_spimex_data__success(date, expected):
    assert get_url_to_spimex_data(date) == expected


def test__download_file_from_spimex__success(make_request_response):
    value = 'some value'
    with patch('webapp.spimex.spimex_parser.requests.get') as requests_get_mock:
        requests_get_mock.return_value = make_request_response(value)
        assert download_file_from_spimex('some_url') == b'some value'

# TODO написать тесты на обработку ошибок

# TODO написать тесты на возвращение объекта sheet.Sheet из байтов и конвертиртацию Sheet.sheet. в строку


@pytest.mark.parametrize(('raw_data, expected'),
                         [
                             (['', 'first_word', '', 'second_word', ''], ['first_word', 'second_word']),
                             (['one', 'two'], ['one', 'two'])
]
)
def test__delete_all_emty_values_from_raw_data__success(raw_data, expected):
    assert delete_all_emty_values_from_raw_data(raw_data) == expected


@pytest.mark.parametrize(('all_values, search_value, expected'),
                         [
                             (['one', 'two', 'tree', 'four', 'tree'], 'tree', [2, 4]),
                             (['1', '2', '3', '4', '5'], '6', [])
])
def test__get_indexes_for_search_value__success(all_values, search_value, expected):
    assert get_indexes_for_search_value(all_values, search_value) == expected


@pytest.mark.parametrize(('raw_string, prefix, expected'),
                         [
                             ('prepword', 'prep', 'word'),
                             ('somesimbol', 'other', 'somesimbol')
])
def test__extract_value_from_string__succes(raw_string, prefix, expected):
    assert extract_value_from_string(raw_string, prefix) == expected


@pytest.mark.parametrize(('all_values, search_value, prefix, expected'),
                         [
                             (['prepone', 'two', 'tree', 'preptwo', 'tree'], 'prep', 'prep', ['one', 'two']),
                             (['1', '2', '3', '4', '5'], '6', '6', [])
])
def test__make_strings_from_all_values__success(all_values, search_value, prefix, expected):
    assert make_strings_from_all_values(all_values, search_value, prefix) == expected


