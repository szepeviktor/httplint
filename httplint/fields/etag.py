from typing import Tuple

from . import HttpField, FieldTest
from ..syntax import rfc7232
from ..type import AddNoteMethodType
from ._utils import unquote_string
from ._notes import BAD_SYNTAX


class etag(HttpField):
    canonical_name = "ETag"
    description = """\
The `ETag` header provides an opaque identifier for the representation."""
    reference = f"{rfc7232.SPEC_URL}#header.etag"
    syntax = rfc7232.ETag
    list_header = False
    deprecated = False
    valid_in_requests = True
    valid_in_responses = True

    def parse(self, field_value: str, add_note: AddNoteMethodType) -> Tuple[bool, str]:
        if field_value[:2] == "W/":
            return (True, unquote_string(field_value[2:]))
        return (False, unquote_string(field_value))


class ETagTest(FieldTest):
    name = "ETag"
    inputs = [b'"foo"']
    expected_out = (False, "foo")


class WeakETagTest(FieldTest):
    name = "ETag"
    inputs = [b'W/"foo"']
    expected_out = (True, "foo")


class UnquotedETagTest(FieldTest):
    name = "ETag"
    inputs = [b"foo"]
    expected_out = (False, "foo")
    expected_err = [BAD_SYNTAX]
