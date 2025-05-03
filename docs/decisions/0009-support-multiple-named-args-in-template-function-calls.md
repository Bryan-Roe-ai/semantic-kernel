consulted: dmytrostruk, matthewbolanos
contact: dmytrostruk
date: 2025-04-07T00:00:00Z
deciders: shawncal, hario90
informed: lemillermicrosoft
status: accepted

# Add Support for Multiple Named Arguments in Template Function Calls

## Context and Problem Statement

Native functions now support multiple parameters, populated from context values with the same name. Semantic functions currently only support calling native functions with no more than one argument.

## Decision Drivers

- Parity with Guidance
- Similarity to languages familiar to SK developers
- YAML compatibility

## Considered Options

### Syntax Idea 1: Using Commas

```handlebars
{{ Skill.MyFunction street="123 Main St", zip="98123", city="Seattle", age=25 }}
```

**Pros**:
- Commas could make longer function calls easier to read, especially if spaces before and after the argument separator are allowed.

**Cons**:
- Guidance doesn't use commas.
- Spaces are already used as delimiters elsewhere, so the added complexity of supporting commas isn't necessary.

### Syntax Idea 2: JavaScript/C#-Style Delimiter (Colon)

```handlebars
{{ Skill.MyFunction street="123 Main St": zip="98123": city="Seattle": age=25 }}
```

**Pros**:
- Resembles JavaScript Object syntax and C# named argument syntax.

**Cons**:
- Doesn't align with Guidance syntax which uses equal signs as argument delimiters.
- Too similar to YAML key/value pairs if we support YAML prompts in the future.

### Syntax Idea 3: Python/Guidance-Style Delimiter

```handlebars
{{ Skill.MyFunction street="123 Main St" zip="98123" city="Seattle" age=25 }}
```

**Pros**:
- Resembles Python's keyword argument syntax.
- Resembles Guidance's named argument syntax.

**Cons**:
- Doesn't align with C# syntax.

### Syntax Idea 4: Allow Whitespace Between Argument Name/Value Delimiter

```handlebars
{{ Skill.MyFunction street="123 Main St" zip="98123" city="Seattle" age=25 }}
```

**Pros**:
- Follows the convention of many programming languages where whitespace flexibility doesn't impact functionality.

**Cons**:
- Promotes code that is harder to read unless commas can be used.
- More complexity to support.
- Doesn't align with Guidance which doesn't support spaces before and after the `=` sign.

## Decision Outcome

- Continue supporting up to one positional argument for backward compatibility. Currently, the argument passed to a function is assumed to be the `$input` context variable.

**Example**:

```handlebars
{{ Skill.MyFunction street="123 Main St" zip="98123" city="Seattle" age=25 }}
```

- Allow argument values to be defined as strings or variables ONLY.

```handlebars
{{ Skill.MyFunction street="123 Main St" zip="98123" city="Seattle" age=25 }}
```

If the function expects a value other than a string for an argument, the SDK will use the corresponding TypeConverter to parse the string provided when evaluating the expression.
```
