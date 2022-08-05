from . import HttpField
from ._test import FieldTest
from ..note import Note, categories, levels
from ..syntax import rfc7231
from ..type import AddNoteMethodType


class content_encoding(HttpField):
    canonical_name = "Content-Encoding"
    description = """\
The `Content-Encoding` header's value indicates what additional content codings have
been applied to the body, and thus what decoding mechanisms must be applied in order to obtain the
media-type referenced by the Content-Type header field.

Content-Encoding is primarily used to allow a document to be compressed without losing the identity
of its underlying media type; e.g., `gzip` and `deflate`."""
    reference = f"{rfc7231.SPEC_URL}#header.content_encoding"
    syntax = rfc7231.Content_Encoding
    list_header = True
    deprecated = False
    valid_in_requests = True
    valid_in_responses = True

    def parse(self, field_value: str, add_note: AddNoteMethodType) -> str:
        # check to see if there are any non-gzip encodings, because
        # that's the only one we ask for.
        if field_value.lower() != "gzip":
            add_note(ENCODING_UNWANTED, unwanted_codings=field_value)
        return field_value.lower()


class ENCODING_UNWANTED(Note):
    category = categories.CONNEG
    level = levels.WARN
    summary = "%(response)s contained unwanted content-codings."
    text = """\
%(response)s's `Content-Encoding` header indicates it has content-codings applied
(`%(unwanted_codings)s`) that REDbot didn't ask for.

Normally, clients ask for the encodings they want in the `Accept-Encoding` request header. Using
encodings that the client doesn't explicitly request can lead to interoperability problems."""


class ContentEncodingTest(FieldTest):
    name = "Content-Encoding"
    inputs = [b"gzip"]
    expected_out = ["gzip"]


class ContentEncodingCaseTest(FieldTest):
    name = "Content-Encoding"
    inputs = [b"GZip"]
    expected_out = ["gzip"]


class UnwantedContentEncodingTest(FieldTest):
    name = "Content-Encoding"
    inputs = [b"gzip", b"foo"]
    expected_out = ["gzip", "foo"]
    expected_err = [ENCODING_UNWANTED]
