#!/usr/bin/env python3
"""Simplified assistant content generation utilities."""

from __future__ import annotations

from semantic_kernel.contents import ChatMessageContent, StreamingChatMessageContent
from semantic_kernel.contents.function_call_content import FunctionCallContent
from semantic_kernel.contents.function_result_content import FunctionResultContent
from semantic_kernel.contents.annotation_content import AnnotationContent
from semantic_kernel.contents.annotations import FilePathAnnotation, FileCitationAnnotation
from semantic_kernel.utils.feature_stage_decorator import experimental_function
from semantic_kernel.contents.author_role import AuthorRole


@experimental_function
def generate_streaming_function_content(agent_name: str, step_details) -> StreamingChatMessageContent:
    items = [
        FunctionCallContent(
            id=tool.id,
            index=getattr(tool, "index", None),
            name=tool.function.name,
            arguments=tool.function.arguments,
        )
        for tool in getattr(step_details, "tool_calls", [])
        if tool.type == "function"
    ]
    return StreamingChatMessageContent(role=AuthorRole.ASSISTANT, name=agent_name, items=items, choice_index=0)


@experimental_function
def generate_function_result_content(agent_name: str, results) -> ChatMessageContent:
    items = [
        FunctionResultContent(id=r.id, index=getattr(r, "index", None), name=r.name, content=str(r.result))
        for r in results
    ]
    return ChatMessageContent(role=AuthorRole.ASSISTANT, name=agent_name, items=items)


@experimental_function
def generate_annotation_content(annotation: FileCitationAnnotation | FilePathAnnotation) -> AnnotationContent:
    file_id = None
    if isinstance(annotation, FilePathAnnotation):
        file_id = annotation.file_path.file_id
    elif isinstance(annotation, FileCitationAnnotation):
        file_id = annotation.file_id
    return AnnotationContent(annotation.type, file_id=file_id)
