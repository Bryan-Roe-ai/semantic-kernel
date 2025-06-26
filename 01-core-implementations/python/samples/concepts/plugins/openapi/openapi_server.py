#!/usr/bin/env python3
"""
import asyncio
Openapi Server module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from aiohttp import web

"""OpenAPI Sample Server"""
routes = web.RouteTableDef()


@routes.post("/{name}")
async def hello(request):
    # Get path parameters
    name = request.match_info.get("name", "")
    # Get query parameters
    q = request.rel_url.query.get("q", "")
    # Get body
    body = await request.json()
    # Get headers
    headers = request.headers
    return web.Response(text=f"Hello, {name}: q={q}, body={body}, headers={headers}")


app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app)
