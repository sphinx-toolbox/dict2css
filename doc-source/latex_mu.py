# 3rd party
from sphinx.application import Sphinx
from sphinx_toolbox.latex import replace_unknown_unicode


def setup(app: Sphinx):
	app.connect("build-finished", replace_unknown_unicode)
