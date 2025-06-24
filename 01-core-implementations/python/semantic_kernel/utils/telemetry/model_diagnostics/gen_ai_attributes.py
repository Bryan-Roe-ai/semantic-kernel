#!/usr/bin/env python3
"""
AI module for gen ai attributes

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.contents.utils.author_role import AuthorRole

# Constants for tracing activities with semantic conventions.
# Ideally, we should use the attributes from the semcov package.
# However, many of the attributes are not yet available in the package,
# so we define them here for now.

# Activity tags
OPERATION = "gen_ai.operation.name"
SYSTEM = "gen_ai.system"
ERROR_TYPE = "error.type"
MODEL = "gen_ai.request.model"
SEED = "gen_ai.request.seed"
PORT = "server.port"
ENCODING_FORMATS = "gen_ai.request.encoding_formats"
FREQUENCY_PENALTY = "gen_ai.request.frequency_penalty"
MAX_TOKENS = "gen_ai.request.max_tokens"
STOP_SEQUENCES = "gen_ai.request.stop_sequences"
TEMPERATURE = "gen_ai.request.temperature"
TOP_K = "gen_ai.request.top_k"
TOP_P = "gen_ai.request.top_p"
FINISH_REASON = "gen_ai.response.finish_reason"
RESPONSE_ID = "gen_ai.response.id"
INPUT_TOKENS = "gen_ai.usage.input_tokens"
OUTPUT_TOKENS = "gen_ai.usage.output_tokens"
TOOL_CALL_ID = "gen_ai.tool.call.id"
TOOL_DESCRIPTION = "gen_ai.tool.description"
TOOL_NAME = "gen_ai.tool.name"
ADDRESS = "server.address"

# Activity events
PROMPT_EVENT = "gen_ai.content.prompt"
COMPLETION_EVENT = "gen_ai.content.completion"

# Activity event attributes
PROMPT_EVENT_PROMPT = "gen_ai.prompt"
COMPLETION_EVENT_COMPLETION = "gen_ai.completion"

