#!/usr/bin/env python3
#
#  serializer.py
"""
Serializer for cascading style sheets.

.. versionadded:: 0.2.0
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Adapted from https://github.com/austinyu/ujson5
#  Copyright (c) 2025 Sir Austin
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import re
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterable, Iterator, Mapping, Optional, Union

# 3rd party
from domdf_python_tools.words import TAB

__all__ = ["CSSSerializer"]

#: Python objects that can be serialized to CSS
Serializable = Union[dict, list, tuple, int, float, str, bool, None]

#: A callable that takes in an object that is not serializable and returns a serializable object
DefaultInterface = Union[
	Callable[[Any], dict],
	Callable[[Any], list],
	Callable[[Any], tuple],
	Callable[[Any], int],
	Callable[[Any], float],
	Callable[[Any], str],
	Callable[[Any], bool],
	Callable[[Any], Serializable]
	]

ESCAPE = re.compile(r'[\x00-\x1f\\"\b\f\n\r\t]')
ESCAPE_DCT = {
		'\\': "\\\\",
		'"': '\\"',
		'\x08': "\\b",
		'\x0c': "\\f",
		'\n': "\\n",
		'\r': "\\r",
		'\t': "\\t",
		}
for i in range(0x20):
	ESCAPE_DCT.setdefault(chr(i), f"\\u{i:04x}")


class CSSSerializer:
	r"""
	Serializes a dictionary to CSS.

	This controls the formatting of the style sheet.

	:param indent: The indent to use, such as a tab (``\t``), two spaces or four spaces.
	:param trailing_semicolon:  Whether to add a semicolon to the end of the final property.
	:param indent_closing_brace:
	:param minify: Minify the CSS. Overrides all other options.
	:param sort_keys: Sort dictionary keys alphabetically.
	:param check_circular: Check for circular references.

	.. versionchanged:: 0.5.0  New implementation. Output may differ slightly from previous css-parser based one.

	.. autosummary-widths:: 1/4
	"""

	def __init__(
			self,
			*,
			indent: str = TAB,
			trailing_semicolon: Optional[bool] = None,
			indent_closing_brace: bool = False,
			minify: bool = False,
			sort_keys: bool = False,
			check_circular: bool = True,  # default: Optional[DefaultInterface] = None,
			) -> None:
		self._set_options(
				indent=indent,
				trailing_semicolon=trailing_semicolon,
				indent_closing_brace=indent_closing_brace,
				minify=minify,
				sort_keys=sort_keys,
				)

		if check_circular:
			self._markers: Optional[Dict[int, Any]] = {}
		else:
			self._markers = None

		# TODO self._default: Optional[DefaultInterface] = default
		self._default: Optional[DefaultInterface] = None

	def _set_options(
			self,
			indent: str = TAB,
			trailing_semicolon: Optional[bool] = None,
			indent_closing_brace: bool = False,
			minify: bool = False,
			sort_keys: bool = False,
			) -> None:

		self._sort_keys: bool = sort_keys
		self._indent_str: str = (None if minify else indent) or ''

		if minify:
			self._key_separator: str = ':'
		else:
			self._key_separator = ": "

		if not indent and not minify:
			self._item_separator: str = "; "
		else:
			self._item_separator = ';'

		if minify:
			self._trailing_semicolon = False
		elif trailing_semicolon is None:
			self._trailing_semicolon = bool(self._indent_str)
		else:
			self._trailing_semicolon = trailing_semicolon

		if indent_closing_brace and indent is not None:
			self._indent_closing_brace = True
		else:
			self._indent_closing_brace = False

		self._minify = minify

	# TODO: deprecate
	def reset_style(self) -> None:  # pragma: no cover
		"""
		Reset the serializer to its default style.
		"""

		self._set_options()

	def encode(self, obj: Mapping) -> str:
		"""
		Return a CSS representation of a Python dictionary.

		:param obj: The Python dictionary to be serialized

		:returns: The CSS string representation of the Python dictionary
		"""

		return ''.join(self.iterencode(obj))

	def iterencode(self, obj: Mapping) -> Iterable[str]:
		"""
		Encode the given dictionary and yield each part of the CSS string representation.

		:param obj: The Python dictionary to be serialized

		:returns: An iterable of strings representing the CSS serialization of the Python dictionary.
		"""

		if not isinstance(obj, Mapping):
			raise TypeError(f"Cannot convert {type(obj)} to CSS")

		return self._iterencode_dict(obj, indent_level=-1)

	def default(self, obj: Any) -> Serializable:
		"""
		Override this method in a subclass to implement custom serialization for objects that are not serializable by default.

		This method should return a serializable object.
		If this method is not overridden, the encoder will raise a :exc:`ValueError` when trying to encode an unsupported object.

		:param obj: The object to be serialized that is not supported by default.

		:returns: A serializable object

		:raises: ValueError: If the object cannot be serialized
		"""

		if self._default is not None:  # pragma no cover  # TODO
			return self._default(obj)

		raise ValueError(f"Object of type {obj.__class__.__name__} cannot be represented in CSS")

	def _encode_float(self, obj: float) -> str:
		if obj != obj or obj == float("inf") or obj == float("-inf"):
			raise ValueError(f"Out of range float values are not allowed: {repr(obj)}")
		else:
			return repr(obj)

	def _encode_str(self, obj: str) -> str:

		def replace_unicode(match: re.Match) -> str:  # pragma: no cover  # TODO
			return ESCAPE_DCT[match.group(0)]

		return ESCAPE.sub(replace_unicode, obj)

	def _iterencode(self, obj: Any, indent_level: int) -> Iterable[str]:
		if isinstance(obj, str):
			yield self._encode_str(obj)
		elif obj is True:
			yield "true"
		elif obj is False:
			yield "false"
		elif obj is None:
			yield "none"
		elif isinstance(obj, int):
			yield repr(obj)
		elif isinstance(obj, float):
			yield self._encode_float(obj)
		elif isinstance(obj, (list, tuple)):  # pragma: no cover  # TODO (needs default exposed)
			yield from self._iterencode_list(obj, indent_level)
		elif isinstance(obj, dict):  # pragma: no cover  # TODO (needs default exposed)
			yield from self._iterencode_dict(obj, indent_level)
		else:
			if self._markers is not None:
				marker_id: Optional[int] = id(obj)
				if marker_id in self._markers:  # pragma: no cover  # TODO (super edge case)
					raise ValueError("Circular reference detected")
				assert marker_id is not None
				self._markers[marker_id] = obj
			else:
				marker_id = None

			obj_user = self.default(obj)
			yield from self._iterencode(obj_user, indent_level)  # pragma: no cover  # TODO (needs default exposed)

			if self._markers is not None and marker_id is not None:  # pragma: no cover  # TODO (needs default exposed)
				del self._markers[marker_id]

	def _iterencode_list(
			self,
			obj: Union[list, tuple, None],
			indent_level: int,
			) -> Iterable[str]:

		# this package
		from dict2css import IMPORTANT

		if not obj:
			raise ValueError("Property cannot be empty")

		if self._markers is not None:
			marker_id: Optional[int] = id(obj)
			if marker_id in self._markers:  # pragma: no cover  # TODO (super edge case)
				raise ValueError("Circular reference detected")
			assert marker_id is not None
			self._markers[marker_id] = obj
		else:
			marker_id = None

		first: bool = True
		for value in obj:
			if first:
				yield ''
				first = False
			else:
				yield ' '

			if value == IMPORTANT:
				yield "!important"
			else:
				yield from self._iterencode(value, indent_level)

		if self._markers is not None and marker_id is not None:
			del self._markers[marker_id]

	def _iterencode_dict(
			self,
			obj: Mapping[str, Any],
			indent_level: int,
			) -> Iterable[str]:
		if not obj:
			if indent_level >= 0:
				yield "{}"

			return

		if self._markers is not None:
			marker_id: Optional[int] = id(obj)
			if marker_id in self._markers:
				raise ValueError("Circular reference detected")
			assert marker_id is not None
			self._markers[marker_id] = obj
		else:
			marker_id = None

		if indent_level >= 0:
			yield '{'

		minify_indent = False
		if self._minify or not self._indent_str:
			# No indent
			newline_indent: Optional[str] = None

			if indent_level == -1:
				indent_level += 1
				minify_indent = True

		else:
			indent_level += 1
			newline_indent = '\n' + self._indent_str * indent_level
			assert newline_indent is not None

			if indent_level > 0:
				yield newline_indent

		first = True
		if self._sort_keys:
			items: Any = sorted(obj.items())
		else:
			items = obj.items()

		total_items: int = len(items)
		for idx, (key, value) in enumerate(items):
			if not isinstance(key, str):
				raise TypeError(f"keys must be strings, not {key.__class__.__name__}")

			if first:
				first = False
			elif newline_indent is not None:
				yield newline_indent  # we do not need to yield anything if indent == 0
			yield self._encode_str(key)

			if isinstance(value, dict):
				if not self._minify:
					yield ' '

				yield from self._iterencode_dict(value, indent_level)
			else:
				yield self._key_separator

				if isinstance(value, (list, tuple)):
					yield from self._iterencode_list(value, indent_level)
				else:
					yield from self._iterencode(value, indent_level)

				if idx != total_items - 1 or self._trailing_semicolon:
					yield self._item_separator

		if self._indent_str:
			indent_level -= 1
			yield '\n' + self._indent_str * indent_level
		elif minify_indent:
			indent_level -= 1

		if indent_level >= 0:
			if self._indent_closing_brace:
				yield self._indent_str

			yield '}'

			if not self._minify:
				yield '\n'

		if self._markers is not None and marker_id is not None:
			del self._markers[marker_id]

	# TODO: deprecate
	@contextmanager
	def use(self) -> Iterator:  # pragma: no cover
		"""
		No-op. Deprecated.
		"""

		yield
