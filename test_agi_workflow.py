import sys
import types
import asyncio
import pytest


@pytest.fixture(autouse=True)
def stub_semantic_kernel(monkeypatch):
    """Provide a minimal stub for the semantic_kernel package."""
    stub = types.ModuleType("semantic_kernel")

    class Kernel:
        def __init__(self):
            self.plugins = {}

        def add_plugin(self, plugin, plugin_name=None):
            self.plugins[plugin_name] = plugin

        def get_function(self, plugin_name, function_name):
            if not hasattr(self.plugins[plugin_name], function_name):
                class Func:
                    async def invoke(self, kernel, **kwargs):
                        raise AttributeError(f"Function '{function_name}' not found in plugin '{plugin_name}'.")
                return Func()
            func = getattr(self.plugins[plugin_name], function_name)

            class Func:
                async def invoke(self, kernel, **kwargs):
                    return func(**kwargs)

            return Func()

    functions = types.ModuleType("semantic_kernel.functions")

    def kernel_function(*args, **kwargs):
        def decorator(fn):
            return fn
        return decorator

    functions.kernel_function = kernel_function
    stub.Kernel = Kernel
    stub.functions = functions

    sys.modules["semantic_kernel"] = stub
    sys.modules["semantic_kernel.functions"] = functions
    yield
    sys.modules.pop("semantic_kernel", None)
    sys.modules.pop("semantic_kernel.functions", None)


def test_process_workflow_success():
    from demo_local_agents import LocalAGIAgent, AGIWorkflowOrchestrator

    orchestrator = AGIWorkflowOrchestrator()
    orchestrator.add_agent("file_agent", LocalAGIAgent("FileAgent"))
    orchestrator.add_agent("chat_agent", LocalAGIAgent("ChatAgent"))

    workflow = [
        {"agent": "file_agent", "function": "file_operation", "params": {"operation": "create", "filename": "demo.txt"}},
        {"agent": "chat_agent", "function": "process_request", "params": {"request": "hello"}},
    ]

    results = asyncio.run(orchestrator.process_workflow(workflow))

    assert results["file_agent_file_operation"] == "📝 Created file: demo.txt"
    assert "Hello" in results["chat_agent_process_request"]


def test_process_workflow_error():
    from demo_local_agents import LocalAGIAgent, AGIWorkflowOrchestrator

    orchestrator = AGIWorkflowOrchestrator()
    orchestrator.add_agent("chat_agent", LocalAGIAgent("ChatAgent"))

    workflow = [{"agent": "chat_agent", "function": "unknown_function"}]

    results = asyncio.run(orchestrator.process_workflow(workflow))

    key = "chat_agent_unknown_function"
    assert key in results
    assert results[key].startswith("Error:")
