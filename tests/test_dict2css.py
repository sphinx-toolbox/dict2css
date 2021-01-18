# stdlib
from typing import Dict, Mapping, MutableMapping

# 3rd party
import css_parser  # type: ignore
import pytest
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.testing import check_file_output, check_file_regression
from domdf_python_tools.words import TAB
from pytest_regressions.data_regression import DataRegressionFixture
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from dict2css import IMPORTANT, CSSSerializer, Style, StyleSheet, dump, dumps, em, load, loads, make_style, px, rem


def test_stylesheet(file_regression: FileRegressionFixture):
	serializer = CSSSerializer(indent="  ", trailing_semicolon=True)

	with serializer.use():
		sheet = StyleSheet()

		# Body width
		sheet.add_style(".wy-nav-content", {"max-width": (px(1200), IMPORTANT)})

		# Spacing between list items
		sheet.add_style("li p:last-child", {"margin-bottom": (px(12), IMPORTANT)})

		# Smooth scrolling between sections
		sheet.add_style("html", {"scroll-behavior": "smooth"})

		stylesheet = sheet.tostring().replace('}', "}\n")

		check_file_regression(stylesheet, file_regression, ".css")


@pytest.mark.parametrize("trailing_semicolon", [True, False])
@pytest.mark.parametrize("indent_closing_brace", [True, False])
@pytest.mark.parametrize("indent", [TAB, "  ", "    "])
def test_dumps(
		file_regression: FileRegressionFixture,
		trailing_semicolon: bool,
		indent_closing_brace: bool,
		indent: str,
		tmp_pathplus: PathPlus
		):
	stylesheet: Dict[str, Style] = {
			".wy-nav-content": {"max-width": (rem(1200), IMPORTANT)},
			"li p:last-child": {
					"margin-bottom": (em(12), IMPORTANT),
					"margin-top": em(6),
					},
			"html": {"scroll-behavior": "smooth"},
			}

	css = dumps(
			stylesheet,
			indent=indent,
			trailing_semicolon=trailing_semicolon,
			indent_closing_brace=indent_closing_brace
			)
	check_file_regression(css, file_regression, ".css")

	output_file = tmp_pathplus / "style.css"

	with output_file.open('w') as fp:
		dump(
				stylesheet,
				fp,
				indent=indent,
				trailing_semicolon=trailing_semicolon,
				indent_closing_brace=indent_closing_brace
				)

	check_file_output(output_file, file_regression)

	dump(
			stylesheet,
			output_file,
			indent=indent,
			trailing_semicolon=trailing_semicolon,
			indent_closing_brace=indent_closing_brace
			)

	check_file_output(output_file, file_regression)


def test_make_style():
	style: css_parser.css.CSSStyleRule = make_style("li p:last-child", {"max-width": (rem(1200), IMPORTANT)})
	assert str(style.selectorText) == "li p:last-child"
	assert StringList(style.cssText) == [
			"li p:last-child {",
			"    max-width: 1200rem !important",
			"    }",
			]

	serializer = CSSSerializer(trailing_semicolon=True)

	with serializer.use():
		assert StringList(style.cssText) == [
				"li p:last-child {",
				"\tmax-width: 1200rem !important;",
				'}',
				]


def test_dump_minify(file_regression: FileRegressionFixture, tmp_pathplus: PathPlus):
	stylesheet: Dict[str, Style] = {
			".wy-nav-content": {"max-width": (rem(1200), IMPORTANT)},
			"li p:last-child": {
					"margin-bottom": (em(12), IMPORTANT),
					"margin-top": em(6),
					},
			"html": {"scroll-behavior": "smooth"},
			}

	css = dumps(stylesheet, minify=True)
	check_file_regression(css, file_regression, ".css")

	output_file = tmp_pathplus / "style.css"

	with output_file.open('w') as fp:
		dump(stylesheet, fp, minify=True)

	check_file_output(output_file, file_regression)

	dump(stylesheet, output_file, minify=True)
	check_file_output(output_file, file_regression)


def test_dumps_media(file_regression: FileRegressionFixture, tmp_pathplus: PathPlus):
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
	check_file_regression(css, file_regression, ".css")

	output_file = tmp_pathplus / "style.css"

	with output_file.open('w') as fp:
		dump(stylesheet, fp, trailing_semicolon=True)

	check_file_output(output_file, file_regression)

	dump(stylesheet, output_file, trailing_semicolon=True)
	check_file_output(output_file, file_regression)


def test_loads(data_regression: DataRegressionFixture, tmp_pathplus: PathPlus):
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

	data_regression.check(loads('\n'.join(style)))

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
