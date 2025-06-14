# SK Prompt Template Syntax

This document has been moved to the Semantic Kernel Documentation site. You can find it by navigating to the [What are prompts?](https://learn.microsoft.com/en-us/semantic-kernel/concepts/prompts) page.

To make an update on the page, file a PR on the [docs repo.](https://github.com/MicrosoftDocs/semantic-kernel-docs/blob/main/semantic-kernel/prompt-engineering/prompt-template-syntax.md)
Prompts are the inputs or queries that a user or a program gives to an LLM AI,
in order to elicit a specific response from the model.

Prompts can be natural
language sentences or questions, or code snippets or commands, or any combination
of text or code, depending on the domain and the task.

Prompts can also be nested
or chained, meaning that the output of one prompt can be used as the input of another
prompt, creating more complex and dynamic interactions with the model.

# SK Prompt Template Syntax

The Semantic Kernel prompt template language is a simple and powerful way to
define and compose AI
[functions](GLOSSARY.md)
**using plain text**.
You can use it to create natural language prompts, generate responses, extract
information, **invoke other prompts** or perform any other task that can be
expressed with text.

The language supports three basic features that allow you to (**#1**) include
variables, (**#2**) call external functions, and (**#3**) pass parameters to functions.

You don't need to write any code or import any external libraries, just use the
curly braces `{{...}}` to embed expressions in your prompts.
Semantic Kernel will parse your template and execute the logic behind it.
This way, you can easily integrate AI into your apps with minimal effort and
maximum flexibility.

## Variables

To include a variable value in your text, use the `{{$variableName}}` syntax.
For example, if you have a variable called `name` that holds the user's name,
you can write:

    Hello {{$name}}, welcome to Semantic Kernel!

This will produce a greeting with the user's name.

Spaces are ignored, so if you find it more readable, you can also write:

    Hello {{ $name }}, welcome to Semantic Kernel!

## Function calls

To call an external function and embed the result in your text, use the
`{{namespace.functionName}}` syntax.
For example, if you have a function called `weather.getForecast` that returns
the weather forecast for a given location, you can write:

    The weather today is {{weather.getForecast}}.

This will produce a sentence with the weather forecast for the default location
stored in the `input` variable.
The `input` variable is set automatically by the kernel when invoking a function.
For instance, the code above is equivalent to:

    The weather today is {{weather.getForecast $input}}.

## Function parameters

To call an external function and pass a parameter to it, use the
`{{namespace.functionName $varName}}` and
`{{namespace.functionName "value"}}` syntax.
For example, if you want to pass a different input to the weather forecast
function, you can write:

    The weather today in {{$city}} is {{weather.getForecast $city}}.
    The weather today in Schio is {{weather.getForecast "Schio"}}.

This will produce two sentences with the weather forecast for two different
locations, using the city stored in the _`city`_ **variable** and the _"Schio"_
location **value** hardcoded in the prompt template.

## Design Principles

The template language is designed to be simple and fast to render, allowing
to create functions with a simple text editor, reducing special syntax to a
minimum, and minimizing edge cases.

The template language uses the **«`$`»** symbol on purpose, to clearly distinguish
between function calls that retrieve content executing some code, from variables,
which are replaced with data from the local temporary memory.

Branching features such as _"if"_, _"for"_, and code blocks are not part of SK's
template language. This reflects SK's design principle of using natural language
as much as possible, with a clear separation from traditional programming code.

By using a simple language, the kernel can also avoid complex parsing and
external dependencies, resulting in a fast and memory efficient processing.

## Semantic function example

Here's a very simple example of a semantic function defined with a prompt
template, using the syntax described.

`== File: skprompt.txt ==`

```
My name: {{msgraph.GetMyName}}
My email: {{msgraph.GetMyEmailAddress}}
My hobbies: {{memory.recall "my hobbies"}}
Recipient: {{$recipient}}
Email to reply to:
=========
{{$sourceEmail}}
=========
Generate a response to the email, to say: {{$input}}

Include the original email quoted after the response.
```

If we were to write that function in C#, it would look something like:

```csharp
async Task<string> GenResponseToEmailAsync(
    string whatToSay,
    string recipient,
    string sourceEmail)
{
    try {
        string name = await this._msgraph.GetMyName();
    } catch {
        ...
    }

    try {
        string email = await this._msgraph.GetMyEmailAddress();
    } catch {
        ...
    }

    try {
        // Use AI to generate an email using the 5 given variables
        // Take care of retry logic, tracking AI costs, etc.
        string response = await ...

        return response;
    } catch {
        ...
    }
}
```

# Notes about special chars

Semantic function templates are text files, so there is no need to escape special chars
like new lines and tabs. However, there are two cases that require a special syntax:

1. Including double curly braces in the prompt templates
2. Passing to functions hardcoded values that include quotes

## Prompts needing double curly braces

Double curly braces have a special use case, they are used to inject variables,
values, and functions into templates.

If you need to include the **`{{`** and **`}}`** sequences in your prompts, which
could trigger special rendering logic, the best solution is to use string values
enclosed in quotes, like `{{ "{{" }}` and `{{ "}}" }}`

For example:

    {{ "{{" }} and {{ "}}" }} are special SK sequences.

will render to:

    {{ and }} are special SK sequences.

## Values that include quotes, and escaping

Values can be enclosed using **single quotes** and **double quotes**.

To avoid the need for special syntax, when working with a value that contains
_single quotes_, we recommend wrapping the value with _double quotes_. Similarly,
when using a value that contains _double quotes_, wrap the value with _single quotes_.

For example:

    ...text... {{ functionName "one 'quoted' word" }} ...text...
    ...text... {{ functionName 'one "quoted" word' }} ...text...

For those cases where the value contains both single and double quotes, you will
need _escaping_, using the special **«`\`»** symbol.

When using double quotes around a value, use **«`\"`»** to include a double quote
symbol inside the value:

    ... {{ "quotes' \"escaping\" example" }} ...

and similarly, when using single quotes, use **«`\'`»** to include a single quote
inside the value:

    ... {{ 'quotes\' "escaping" example' }} ...

Both are rendered to:

    ... quotes' "escaping" example ...

Note that for consistency, the sequences **«`\'`»** and **«`\"`»** do always render
to **«`'`»** and **«`"`»**, even when escaping might not be required.

For instance:

    ... {{ 'no need to \"escape" ' }} ...

is equivalent to:

    ... {{ 'no need to "escape" ' }} ...

and both render to:

    ... no need to "escape"  ...

In case you may need to render a backslash in front of a quote, since **«`\`»**
is a special char, you will need to escape it too, and use the special sequences
**«`\\\'`»** and **«`\\\"`»**.

For example:

    {{ 'two special chars \\\' here' }}

is rendered to:

    two special chars \' here

Similarly to single and double quotes, the symbol **«`\`»** doesn't always need
to be escaped. However, for consistency, it can be escaped even when not required.

For instance:

    ... {{ 'c:\\documents\\ai' }} ...

is equivalent to:

    ... {{ 'c:\documents\ai' }} ...

and both are rendered to:

    ... c:\documents\ai ...

Lastly, backslashes have a special meaning only when used in front of
**«`'`»**, **«`"`»** and **«`\`»**.

In all other cases, the backslash character has no impact and is rendered as is.
For example:

    {{ "nothing special about these sequences: \0 \n \t \r \foo" }}

is rendered to:

    nothing special about these sequences: \0 \n \t \r \foo

## Examples and Use Cases

### Example 1: Generating a Personalized Greeting

```csharp
string template = "Hello {{$name}}, welcome to Semantic Kernel!";
var variables = new Dictionary<string, string> { { "name", "John" } };
string result = SemanticKernel.Render(template, variables);
Console.WriteLine(result); // Output: Hello John, welcome to Semantic Kernel!
```

### Example 2: Fetching Weather Forecast

```csharp
string template = "The weather today is {{weather.getForecast}}.";
var functions = new Dictionary<string, Func<string>> { { "weather.getForecast", () => "sunny" } };
string result = SemanticKernel.Render(template, functions: functions);
Console.WriteLine(result); // Output: The weather today is sunny.
```

### Example 3: Using Function Parameters

```csharp
string template = "The weather today in {{$city}} is {{weather.getForecast $city}}.";
var variables = new Dictionary<string, string> { { "city", "New York" } };
var functions = new Dictionary<string, Func<string, string>> { { "weather.getForecast", city => city == "New York" ? "rainy" : "unknown" } };
string result = SemanticKernel.Render(template, variables, functions);
Console.WriteLine(result); // Output: The weather today in New York is rainy.
```

### Example 4: Creating a Response Email

```csharp
string template = @"
My name: {{msgraph.GetMyName}}
My email: {{msgraph.GetMyEmailAddress}}
My hobbies: {{memory.recall 'my hobbies'}}
Recipient: {{$recipient}}
Email to reply to:
=========
{{$sourceEmail}}
=========
Generate a response to the email, to say: {{$input}}
Include the original email quoted after the response.";
var variables = new Dictionary<string, string>
{
    { "recipient", "Jane" },
    { "sourceEmail", "Hello, how are you?" },
    { "input", "I am doing well, thank you!" }
};
var functions = new Dictionary<string, Func<string>>
{
    { "msgraph.GetMyName", () => "John Doe" },
    { "msgraph.GetMyEmailAddress", () => "john.doe@example.com" },
    { "memory.recall", key => key == "my hobbies" ? "reading, hiking" : "unknown" }
};
string result = SemanticKernel.Render(template, variables, functions);
Console.WriteLine(result);
```

This will produce:

```
My name: John Doe
My email: john.doe@example.com
My hobbies: reading, hiking
Recipient: Jane
Email to reply to:
=========
Hello, how are you?
=========
Generate a response to the email, to say: I am doing well, thank you!
Include the original email quoted after the response.
```

### Example 5: Generating a Personalized Greeting with Additional Information

```csharp
string template = "Hello {{$name}}, welcome to Semantic Kernel! Your role is {{$role}}.";
var variables = new Dictionary<string, string> { { "name", "John" }, { "role", "Developer" } };
string result = SemanticKernel.Render(template, variables);
Console.WriteLine(result); // Output: Hello John, welcome to Semantic Kernel! Your role is Developer.
```

### Example 6: Fetching Weather Forecast with Location

```csharp
string template = "The weather today in {{$location}} is {{weather.getForecast $location}}.";
var variables = new Dictionary<string, string> { { "location", "San Francisco" } };
var functions = new Dictionary<string, Func<string, string>> { { "weather.getForecast", location => location == "San Francisco" ? "foggy" : "unknown" } };
string result = SemanticKernel.Render(template, variables, functions);
Console.WriteLine(result); // Output: The weather today in San Francisco is foggy.
```

### Example 7: Using Function Parameters with Default Values

```csharp
string template = "The weather today in {{$city}} is {{weather.getForecast $city}}.";
var variables = new Dictionary<string, string> { { "city", "Los Angeles" } };
var functions = new Dictionary<string, Func<string, string>> { { "weather.getForecast", city => city == "Los Angeles" ? "sunny" : "unknown" } };
string result = SemanticKernel.Render(template, variables, functions);
Console.WriteLine(result); // Output: The weather today in Los Angeles is sunny.
```

### Example 8: Creating a Response Email with Additional Information

```csharp
string template = @"
My name: {{msgraph.GetMyName}}
My email: {{msgraph.GetMyEmailAddress}}
My hobbies: {{memory.recall 'my hobbies'}}
Recipient: {{$recipient}}
Email to reply to:
=========
{{$sourceEmail}}
=========
Generate a response to the email, to say: {{$input}}
Include the original email quoted after the response.
Additional information: {{$additionalInfo}}";
var variables = new Dictionary<string, string>
{
    { "recipient", "Jane" },
    { "sourceEmail", "Hello, how are you?" },
    { "input", "I am doing well, thank you!" },
    { "additionalInfo", "Looking forward to our meeting next week." }
};
var functions = new Dictionary<string, Func<string>>
{
    { "msgraph.GetMyName", () => "John Doe" },
    { "msgraph.GetMyEmailAddress", () => "john.doe@example.com" },
    { "memory.recall", key => key == "my hobbies" ? "reading, hiking" : "unknown" }
};
string result = SemanticKernel.Render(template, variables, functions);
Console.WriteLine(result);
```

This will produce:

```
My name: John Doe
My email: john.doe@example.com
My hobbies: reading, hiking
Recipient: Jane
Email to reply to:
=========
Hello, how are you?
=========
Generate a response to the email, to say: I am doing well, thank you!
Include the original email quoted after the response.
Additional information: Looking forward to our meeting next week.
```
To make an update on the page, file a PR on the [docs repo.](https://github.com/MicrosoftDocs/semantic-kernel-docs/blob/main/semantic-kernel/concepts/prompts/index.md)
