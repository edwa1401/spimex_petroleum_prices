from webapp.spimex.spimex_parser import convert_empty_strings


def test__convert_empty_strings__success_return_none_for_value_is_dash():
    assert convert_empty_strings('-') is None


def test__convert_empty_strings__return_string_when_value_is_not_dash():
    assert convert_empty_strings('abc') == 'abc'
