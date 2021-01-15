# 3rd party
import css_parser
from css_parser.css import CSSMediaRule

# this package
from dict2css import IMPORTANT, make_style, rem


def test_media():
	# 	print(MediaList("screen"))
	# 	media = MediaList("screen and (min-width: 870px)")
	# 	style: css_parser.css.CSSStyleRule = make_style("li p:last-child", {"max-width": (rem(1200), IMPORTANT)})
	#
	# 	print(media)
	# 	sheet =css_parser.css.CSSStyleSheet(media=media)
	# 	sheet.add(style)
	# 	print(sheet)
	# 	print(print(sheet.cssText))

	media = CSSMediaRule("screen and (min-width: 870px)")
	style: css_parser.css.CSSStyleRule = make_style("li p:last-child", {"max-width": (rem(1200), IMPORTANT)})

	media.add(style)
	print(media)
	sheet = css_parser.css.CSSStyleSheet()
	sheet.add(media)
	print(sheet)
	print(sheet.cssText)
