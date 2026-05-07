# stdlib
from ipaddress import IPv4Address
from typing import Dict, Mapping, MutableMapping

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture, AdvancedFileRegressionFixture
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.words import TAB

# this package
from dict2css import IMPORTANT, Style, dump, dumps, load, loads
from dict2css.helpers import em, px, rem


def boolean_option(name: str, id: str):  # noqa: A002,MAN002  # pylint: disable=redefined-builtin
	return pytest.mark.parametrize(
			name,
			[
					pytest.param(True, id=id),
					pytest.param(False, id=f"not {id}"),
					],
			)


def test_dumps_not_mapping():
	with pytest.raises(TypeError, match="Cannot convert .* to CSS"):
		dumps([1, 2, 3])

	with pytest.raises(TypeError, match="Cannot convert .* to CSS"):
		dumps((1, 2, 3))

	with pytest.raises(TypeError, match="Cannot convert .* to CSS"):
		dumps("ABC")

	with pytest.raises(TypeError, match="Cannot convert .* to CSS"):
		dumps(123)

	with pytest.raises(TypeError, match="Cannot convert .* to CSS"):
		dumps(123.456)

	with pytest.raises(TypeError, match="Cannot convert .* to CSS"):
		dumps(True)

	with pytest.raises(TypeError, match="Cannot convert .* to CSS"):
		dumps(None)


@boolean_option("check_circular", "check_circular")
def test_dumps_unknown_type(check_circular: bool):
	with pytest.raises(ValueError, match="Object of type .* cannot be represented in CSS"):
		dumps({"the_key": None}, check_circular=check_circular)

	with pytest.raises(ValueError, match="Object of type .* cannot be represented in CSS"):
		dumps({"the_key": IPv4Address("127.0.0.1")}, check_circular=check_circular)


def test_dumps_bad_floats():
	with pytest.raises(ValueError, match="Out of range float values are not allowed:"):
		dumps({"the_key": float("inf")})

	with pytest.raises(ValueError, match="Out of range float values are not allowed:"):
		dumps({"the_key": float("-inf")})

	with pytest.raises(ValueError, match="Out of range float values are not allowed:"):
		dumps({"the_key": float("nan")})


@boolean_option("check_circular", "check_circular")
@boolean_option("sort_keys", "sort_keys")
@boolean_option("trailing_semicolon", "trailing_semicolon")
@boolean_option("indent_closing_brace", "indent_closing_brace")
@pytest.mark.parametrize(
		"indent",
		[
				pytest.param(TAB, id="tab"),
				pytest.param("  ", id='2'),
				pytest.param("    ", id='4'),
				pytest.param('', id='0'),
				],
		)
def test_dumps(
		advanced_file_regression: AdvancedFileRegressionFixture,
		trailing_semicolon: bool,
		indent_closing_brace: bool,
		indent: str,
		check_circular: bool,
		sort_keys: bool,
		tmp_pathplus: PathPlus,
		):
	stylesheet: Dict[str, Style] = {
			".wy-nav-content": {"max-width": (rem(1200), IMPORTANT), "z-index": 999},
			"li p:last-child": {
					"margin-bottom": (em(12), IMPORTANT),
					"margin-top": em(6),
					"font-size": px(14),
					"line-height": 1.5,
					"font-weight": (800, IMPORTANT),
					},
			"html": {"scroll-behavior": "smooth"},
			}

	# TODO
	sort_keys = False

	css = dumps(
			stylesheet,
			indent=indent,
			trailing_semicolon=trailing_semicolon,
			indent_closing_brace=indent_closing_brace,
			check_circular=check_circular,
			sort_keys=sort_keys,
			)
	advanced_file_regression.check(css, extension=".css")

	output_file = tmp_pathplus / "style.css"

	with output_file.open('w') as fp:
		dump(
				stylesheet,
				fp,
				indent=indent,
				trailing_semicolon=trailing_semicolon,
				indent_closing_brace=indent_closing_brace,
				)

	advanced_file_regression.check_file(output_file)

	dump(
			stylesheet,
			output_file,
			indent=indent,
			trailing_semicolon=trailing_semicolon,
			indent_closing_brace=indent_closing_brace,
			)

	advanced_file_regression.check_file(output_file)


def test_dump_minify(advanced_file_regression: AdvancedFileRegressionFixture, tmp_pathplus: PathPlus):
	stylesheet: Dict[str, Style] = {
			".wy-nav-content": {"max-width": (rem(1200), IMPORTANT)},
			"li p:last-child": {
					"margin-bottom": (em(12), IMPORTANT),
					"margin-top": em(6),
					},
			"html": {"scroll-behavior": "smooth"},
			}

	css = dumps(stylesheet, minify=True)
	advanced_file_regression.check(css, extension=".css")

	output_file = tmp_pathplus / "style.css"

	with output_file.open('w') as fp:
		dump(stylesheet, fp, minify=True)

	advanced_file_regression.check_file(output_file)

	dump(stylesheet, output_file, minify=True)
	advanced_file_regression.check_file(output_file)


def test_dumps_media(advanced_file_regression: AdvancedFileRegressionFixture, tmp_pathplus: PathPlus):
	stylesheet: Dict[str, MutableMapping] = {
			".wy-nav-content": {"max-width": (rem(1200), IMPORTANT)},
			"li p:last-child": {
					"margin-bottom": (em(12), IMPORTANT),
					"margin-top": em(6),
					},
			"html": {"scroll-behavior": "smooth"},
			"@media screen and (min-width: 870px)": {"li p:last-child": {"max-width": (rem(1200), IMPORTANT)}},
			}

	css = dumps(stylesheet, trailing_semicolon=True)
	advanced_file_regression.check(css, extension=".css")

	output_file = tmp_pathplus / "style.css"

	with output_file.open('w') as fp:
		dump(stylesheet, fp, trailing_semicolon=True)

	advanced_file_regression.check_file(output_file)

	dump(stylesheet, output_file, trailing_semicolon=True)
	advanced_file_regression.check_file(output_file)


def test_loads(advanced_data_regression: AdvancedDataRegressionFixture, tmp_pathplus: PathPlus):
	style = [
			".wy-nav-content {",
			"    max-width: 1200rem !important;",
			"    }",
			'',
			"li p:last-child {",
			"    margin-bottom: 12em !important;",
			"    margin-top: 6em;",
			"    }",
			'',
			"@media screen {",
			"    html {",
			"        scroll-behavior: smooth;",
			"        }",
			'}',
			]

	advanced_data_regression.check(loads('\n'.join(style)))

	stylesheet: Mapping[str, Mapping] = {
			".wy-nav-content": {"max-width": (rem(1200), IMPORTANT)},
			"li p:last-child": {
					"margin-bottom": (em(12), IMPORTANT),
					"margin-top": em(6),
					},
			"html": {"scroll-behavior": "smooth"},
			"@media screen and (min-width: 870px)": {"li p:last-child": {"max-width": (rem(1200), IMPORTANT)}},
			}

	assert loads(dumps(stylesheet)) == stylesheet

	style_file = tmp_pathplus / "style.css"
	dump(stylesheet, style_file)
	assert load(style_file) == stylesheet

	with style_file.open() as fp:
		assert load(fp) == stylesheet


def test_loads_bad_syntax():
	style = [
			".wy-nav-content {",
			"    max-width",
			"    }",
			]

	with pytest.raises(ValueError, match="<ParseError invalid>"):
		loads('\n'.join(style))


def test_circular_references():
	css = {
			'a': {'b': 'c'},
			}
	css['d'] = css

	with pytest.raises(ValueError, match="Circular reference detected"):
		dumps(css)


def test_edge_cases():
	with pytest.raises(TypeError, match="keys must be strings, not"):
		dumps({1234: {'a': 'b'}})
	with pytest.raises(ValueError, match="Property cannot be empty"):
		dumps({'a': {'b': ()}})

	assert dumps({}) == ''
	assert dumps({'a': {}}) == "a {}\n"
	assert dumps({'a': {'b': True}}, indent='') == "a {b: true; }\n"
	assert dumps({'a': {'b': False}}, indent='') == "a {b: false; }\n"

	assert dumps({'a': {'b': ('c', ('d', ))}}) == 'a {\n\tb: c d;\n}\n'
