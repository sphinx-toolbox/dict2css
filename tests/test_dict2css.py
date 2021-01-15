# stdlib
from typing import Dict

# 3rd party
import css_parser  # type: ignore
import pytest
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.testing import check_file_output, check_file_regression
from domdf_python_tools.words import TAB

# this package
from dict2css import IMPORTANT, CSSSerializer, Style, StyleSheet, dump, dumps, em, make_style, px, rem


def test_stylesheet(file_regression):
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
def test_dumps(file_regression, trailing_semicolon, indent_closing_brace, indent, tmp_pathplus):
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


def test_dump_minify(file_regression, tmp_pathplus):
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
		dump(
				stylesheet,
				fp,
				minify=True,
				)

	check_file_output(output_file, file_regression)
