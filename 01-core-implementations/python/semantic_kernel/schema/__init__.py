
import pytest
import asyncio

class CodeBlock:
	def __init__(self, code):
		self._code = code

	async def render_code_async(self, kernel):
		# Simulate async behavior
		await asyncio.sleep(0.01)
		return self._code.strip('\'')

class ValBlock:
	def __init__(self, value):
		self._value = value

	def get_value(self) -> str:
		return self._value.strip('\'')

class TestCodeBlock:
	@pytest.mark.asyncio
	async def test_it_renders_code_block_consisting_of_just_a_val_block_2_async(self):
		# Arrange
		val_block = ValBlock("'arrivederci'")

		# Act
		code_block = CodeBlock(val_block.get_value())
		result = await code_block.render_code_async(None)

		# Assert
		assert result == "arrivederci"

import pytest
import asyncio

class CodeBlock:
	def __init__(self, code):
		self._code = code

	async def render_code_async(self, kernel):
		# Simulate async behavior
		await asyncio.sleep(0.01)
		return self._code.strip('\'')

class ValBlock:
	def __init__(self, value):
		self._value = value

	def get_value(self) -> str:
		return self._value.strip('\'')

class TestCodeBlock:
	@pytest.mark.asyncio
	async def test_it_renders_code_block_consisting_of_just_a_val_block_2_async(self):
		# Arrange
		val_block = ValBlock("'arrivederci'")

		# Act
		code_block = CodeBlock(val_block.get_value())
		result = await code_block.render_code_async(None)

		# Assert
		assert result == "arrivederci"

