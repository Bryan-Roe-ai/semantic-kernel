#!/usr/bin/env python3
"""
import asyncio
Auth module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

# See https://github.com/microsoft/BotBuilder-Samples/blob/main/samples/python/80.skills-simple-bot-to-bot/echo-skill-bot/authentication/allowed_callers_claims_validator.py
from collections.abc import Awaitable, Callable

from botframework.connector.auth import JwtTokenValidation, SkillValidation
from config import Config


class AllowedCallersClaimsValidator:
    config_key = "ALLOWED_CALLERS"

    def __init__(self, config: Config):
        if not config:
            raise TypeError("AllowedCallersClaimsValidator: config object cannot be None.")

        # ALLOWED_CALLERS is the setting in config.py file
        # that consists of the list of parent bot ids that are allowed to access the skill
        # to add a new parent bot simply go to the AllowedCallers and add
        # the parent bot's microsoft app id to the list
        caller_list = getattr(config, self.config_key)
        if caller_list is None:
            raise TypeError(f'"{self.config_key}" not found in configuration.')
        self._allowed_callers = frozenset(caller_list)

    @property
    def claims_validator(self) -> Callable[[list[dict]], Awaitable]:
        async def allow_callers_claims_validator(claims: dict[str, object]):
            # if allowed_callers is None we allow all calls
            if "*" not in self._allowed_callers and SkillValidation.is_skill_claim(claims):
                # Check that the appId claim in the skill request is in the list of skills configured for this bot.
                app_id = JwtTokenValidation.get_app_id_from_claims(claims)
                if app_id not in self._allowed_callers:
                    raise PermissionError(
                        f'Received a request from a bot with an app ID of "{app_id}".'
                        f" To enable requests from this caller, add the app ID to your configuration file."
                    )

            return

        return allow_callers_claims_validator
