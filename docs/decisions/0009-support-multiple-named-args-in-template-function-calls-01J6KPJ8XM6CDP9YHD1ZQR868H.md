consulted: dmytrostruk, matthewbolanos
contact: dmytrostruk
date: 2024-08-31T00:00:00Z
deciders: shawncal, hario90
informed: lemillermicrosoft
runme:
  document:
    relativePath: 0009-support-multiple-named-args-in-template-function-calls.md
  session:
    id: 01J6KPJ8XM6CDP9YHD1ZQR868H
    updated: 2024-08-31 07:57:54Z
status: accepted

# Add support for multiple named arguments in template function calls

## Context and Problem Statement

Native functions now support multiple parameters, populated from context values with the same name. Semantic functions currently only support calling native functions with no more than one argument. This limitation needs to be addressed for better functionality and flexibility.

## Decision Drivers

- Parity with Guidance
- Readability
- Similarity to languages familiar to SK developers
- YAML compatibility

## Considered Options

### Syntax idea 1: Using commas

```handlebars
{{Skill.MyFunction street: "123 Main St", zip: "98123", city:"Seattle", age: 25}}
```

**Pros:**

- Commas could make longer function calls easier to read, especially if spaces before and after the argument separator (a colon in this case) are allowed.

**Cons:**

- Guidance doesn't use commas.
- Spaces are already used as delimiters elsewhere, so the added complexity of supporting commas isn't necessary.

### Syntax idea 2: JavaScript/C#-Style delimiter (colon)

```handlebars
{{MyFunction street:"123 Main St" zip:"98123" city:"Seattle" age: "25"}}
```

**Pros:**

- Resembles JavaScript Object syntax and C# named argument syntax.

**Cons:**

- Doesn't align with Guidance syntax, which uses equal signs as argument part delimiters.
- Too similar to YAML key/value pairs if we support YAML prompts in the future.

### Syntax idea 3: Python/Guidance-Style delimiter

```handlebars
{{MyFunction street="123 Main St" zip="98123" city="Seattle"}}
```

**Pros:**

- Resembles Python's keyword argument syntax.
- Resembles Guidance's named argument syntax.
- Not too similar to YAML key/value pairs if we support YAML prompts in the future.

**Cons:**

- Doesn't align with C# syntax.

### Syntax idea 4: Allow whitespace between argument name/value delimiter

```handlebars
{{MyFunction street="123 Main St" zip="98123" city="Seattle"}}
```

**Pros:**

- Follows the convention followed by many programming languages of whitespace flexibility where spaces, tabs, and newlines within code don't impact a program's functionality.

**Cons:**

- Promotes code that is harder to read unless commas can be used (see [Using Commas](#syntax-idea-1-using-commas)).
- More complexity to support.
- Doesn't align with Guidance, which doesn't support spaces before and after the `=` sign.

## Decision Outcome

**Chosen options:** "Syntax idea 3: Python/Guidance-Style keyword arguments" and "Syntax idea 4: Allow whitespace between argument name/value delimiter" because they align well with Guidance's syntax and are the most compatible with YAML.

### Additional Decisions:

- Continue supporting up to one positional argument for backward compatibility. Currently, the argument passed to a function is assumed to be the `$input` context variable.

**Example:**

```handlebars
{{MyFunction "inputVal" street="123 Main St" zip="98123" city="Seattle"}}
```

- Allow argument values to be defined as strings or variables ONLY.

**Example:**

```handlebars
{{MyFunction street=$street zip="98123" city="Seattle"}}
```

If a function expects a value other than a string for an argument, the SDK will use the corresponding TypeConverter to parse the string provided when evaluating the expression.
```
