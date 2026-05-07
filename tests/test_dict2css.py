# stdlib
from typing import Dict, Mapping, MutableMapping

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture, AdvancedFileRegressionFixture
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.words import TAB

# this package
from dict2css import IMPORTANT, Style, dump, dumps, load, loads
from dict2css.helpers import em, rem


@pytest.mark.parametrize("trailing_semicolon", [True, False])
@pytest.mark.parametrize("indent_closing_brace", [True, False])
@pytest.mark.parametrize("indent", [TAB, "  ", "    "])
def test_dumps(
		advanced_file_regression: AdvancedFileRegressionFixture,
		trailing_semicolon: bool,
		indent_closing_brace: bool,
		indent: str,
		tmp_pathplus: PathPlus,
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
			indent_closing_brace=indent_closing_brace,
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
