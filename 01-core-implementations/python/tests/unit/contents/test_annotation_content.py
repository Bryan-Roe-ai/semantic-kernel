# Copyright (c) Microsoft. All rights reserved.

from xml.etree.ElementTree import Element

import pytest

from semantic_kernel.contents.annotation_content import AnnotationContent, CitationType

test_cases = [
    pytest.param(AnnotationContent(file_id="12345"), id="file_id"),
    pytest.param(AnnotationContent(quote="This is a quote."), id="quote"),
    pytest.param(AnnotationContent(start_index=5, end_index=20), id="indices"),
    pytest.param(
        AnnotationContent(
            file_id="12345", quote="This is a quote.", start_index=5, end_index=20
        ),
        id="all_fields",
    ),
    pytest.param(
        AnnotationContent(
            file_id="abc",
            type=CitationType.URL_CITATION.value,
            url="http://example.com",
            quote="q",
            start_index=0,
            end_index=2,
        ),
        id="citation_type_and_url",
    ),
]


def test_create_empty():
    annotation = AnnotationContent()
    assert annotation.file_id is None
    assert annotation.quote is None
    assert annotation.start_index is None
    assert annotation.end_index is None


def test_create_file_id():
    annotation = AnnotationContent(file_id="12345")
    assert annotation.file_id == "12345"


def test_create_quote():
    annotation = AnnotationContent(quote="This is a quote.")
    assert annotation.quote == "This is a quote."


def test_create_indices():
    annotation = AnnotationContent(start_index=5, end_index=20)
    assert annotation.start_index == 5
    assert annotation.end_index == 20


def test_create_all_fields():
    annotation = AnnotationContent(
        file_id="12345", quote="This is a quote.", start_index=5, end_index=20
    )
    assert annotation.file_id == "12345"
    assert annotation.quote == "This is a quote."
    assert annotation.start_index == 5
    assert annotation.end_index == 20


def test_update_file_id():
    annotation = AnnotationContent()
    annotation.file_id = "12345"
    assert annotation.file_id == "12345"


def test_update_quote():
    annotation = AnnotationContent()
    annotation.quote = "This is a quote."
    assert annotation.quote == "This is a quote."


def test_update_indices():
    annotation = AnnotationContent()
    annotation.start_index = 5
    annotation.end_index = 20
    assert annotation.start_index == 5
    assert annotation.end_index == 20


def test_to_str():
    annotation = AnnotationContent(file_id="12345", quote="This is a quote.", start_index=5, end_index=20)
    # Keep all unique assertion lines from both branches
    assert (
        str(annotation)
        == "AnnotationContent(file_id=12345, quote=This is a quote., start_index=5, end_index=20)"
        or str(annotation)
        == "AnnotationContent(file_id=12345, url=None, quote=This is a quote., start_index=5, end_index=20)"
        or str(annotation)
        == "AnnotationContent(type=None, file_id=12345, url=None, quote=This is a quote., start_index=5, end_index=20)"
    )


def test_to_element():
    annotation = AnnotationContent(
        file_id="12345", quote="This is a quote.", start_index=5, end_index=20
    )
    element = annotation.to_element()
    assert element.tag == "annotation"
    assert element.get("file_id") == "12345"
    assert element.get("quote") == "This is a quote."
    assert element.get("start_index") == "5"
    assert element.get("end_index") == "20"


def test_from_element():
    element = Element("AnnotationContent")
    element.set("file_id", "12345")
    element.set("quote", "This is a quote.")
    element.set("start_index", "5")
    element.set("end_index", "20")
    annotation = AnnotationContent.from_element(element)
    assert annotation.file_id == "12345"
    assert annotation.quote == "This is a quote."
    assert annotation.start_index == 5
    assert annotation.end_index == 20


def test_to_dict():
    annotation = AnnotationContent(file_id="12345", quote="This is a quote.", start_index=5, end_index=20)
    # Keep all unique logic from both branches
    expected_text = (
        f"type={annotation.citation_type}, {annotation.file_id or annotation.url} {annotation.quote} "
        f"(Start Index={annotation.start_index}->End Index={annotation.end_index})"
    )
    assert annotation.to_dict() == {
        "type": "text",
        "text": expected_text,
    }


@pytest.mark.parametrize("annotation", test_cases)
def test_element_roundtrip(annotation):
    element = annotation.to_element()
    new_annotation = AnnotationContent.from_element(element)
    assert new_annotation == annotation


@pytest.mark.parametrize("annotation", test_cases)
def test_to_dict_call(annotation):
    ctype = annotation.citation_type.value if annotation.citation_type else None
    expected_text = (
        f"type={ctype}, {annotation.file_id or annotation.url} {annotation.quote} "
        f"(Start Index={annotation.start_index}->End Index={annotation.end_index})"
    )
    expected_dict = {
        "type": "text",
        "text": expected_text,
    }
    assert annotation.to_dict() == expected_dict
