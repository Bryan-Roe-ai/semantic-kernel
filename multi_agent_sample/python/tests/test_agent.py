from agent_core import Agent, AgentSettings
import pytest


def test_basic_echo():
    agent = Agent(name="TestAgent")
    out = agent.send_message("hello")
    assert out == "TestAgent: hello"


def test_empty_message_raises():
    agent = Agent(name="X", settings=AgentSettings())
    with pytest.raises(ValueError):
        agent.send_message("")


def test_custom_format():
    settings = AgentSettings(echo_format="[{name}] {message}!")
    agent = Agent(name="PyAgent", settings=settings)
    assert agent.send_message("run") == "[PyAgent] run!"
