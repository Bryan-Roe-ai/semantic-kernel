# Copyright (c) Microsoft. All rights reserved.

from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel_pydantic import KernelBaseModel


class TextPlugin(KernelBaseModel):
    """TextPlugin provides a set of functions to manipulate strings.

    Usage:
        kernel.add_plugin(TextPlugin(), plugin_name="text")
    """

    @kernel_function(description="Change all string chars to uppercase.")
    def uppercase(self, input: str) -> str:
        """Convert a string to uppercase.

        Example:
            KernelArguments["input"] = "hello world"
            {{text.uppercase $input}} => "HELLO WORLD"
        """
        return input.upper()

    @kernel_function(description="Change all string chars to lowercase.")
    def lowercase(self, input: str) -> str:
        """Convert a string to lowercase.

        Example:
            KernelArguments["input"] = "HELLO WORLD"
            {{text.lowercase $input}} => "hello world"
        """
        return input.lower()

    @kernel_function(description="Return the length of the input text.")
    def length(self, input: str) -> str:
        """Get the length of a string.

        Example:
            KernelArguments["input"] = "hello world"
            {{text.length $input}} => "11"
        """
        return str(len(input))

    @kernel_function(description="Trim whitespace from the start and end of a string.")
    def trim(self, input: str) -> str:
        """Trim whitespace from the start and end of a string.

        Example:
            KernelArguments["input"] = "  hello world  "
            {{text.trim $input}} => "hello world"
        """
        return input.strip()

    @kernel_function(description="Trim whitespace from the start of a string.")
    def trim_start(self, input: str) -> str:
        """Trim whitespace from the start of a string.

        Example:
             KernelArguments["input"] = "  hello world  "
             {{text.trim_start $input}} => "hello world  "
        """
        return input.lstrip()

    @kernel_function(description="Trim whitespace from the end of a string.")
    def trim_end(self, input: str) -> str:
        """Trim whitespace from the end of a string.

        Example:
             KernelArguments["input"] = "  hello world  "
             {{text.trim_end $input}} => "  hello world"
        """
        return input.rstrip()

    @kernel_function(description="Concat two strings into one.")
    def concat(self, input: str, input2: str) -> str:
        """Concatenate two strings.

        Args:
            input (str): The first string.
            input2 (str): The second string.

        Returns:
            str: The concatenated string.

        Example:
            KernelArguments["input"] = "hello"
            KernelArguments["input2"] = " world"
            {{text.concat $input $input2}} => "hello world"
        """
        return input + input2

    @kernel_function(description="Echo the input text back.")
    def echo(self, text: str) -> str:
        """Echo the input text back.

        Args:
            text (str): The input text.

        Returns:
            str: The same input text.

        Example:
            KernelArguments["text"] = "hello world"
            {{text.echo $text}} => "hello world"
        """
        return text
