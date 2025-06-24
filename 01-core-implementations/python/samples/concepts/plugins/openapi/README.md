### Running the OpenAPI syntax example

For more generic setup instructions, including how to install the `uv` tool, see the [main README](../../../../DEV_SETUP.md).

1. In a terminal, navigate to `semantic_kernel/python/samples/concepts/plugins/openapi`.

2. Run `uv sync` followed by `source .venv/bin/activate` to enter the virtual environment (depending on the os, the activate script may be in a different location).

3. Start the server by running `python openapi_server.py`.

4. In another terminal, do steps 1 & 2. Then, run `python openapi_client.py`, which will register a plugin representing the API defined in openapi.yaml


---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**  
Copyright (c) 2025 Bryan Roe  
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
