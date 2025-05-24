consulted: null
status: superseded by [ADR-0062](0062-open-api-payload.md)
contact: SergeyMenshykh
date: 2023-08-15T00:00:00Z
deciders: shawncal
informed: null

# Dynamic payload building for PUT and POST RestAPI operations and parameter namespacing

## Context and Problem Statement

Currently, the SK OpenAPI does not allow the dynamic creation of payload/body for PUT and POST RestAPI operations, even though all the required metadata is available. One of the reasons the functionality is limited is due to the absence of a mechanism for dynamically constructing payloads.

## Decision Drivers

- Create a mechanism that enables the dynamic construction of the payload/body for PUT and POST RestAPI operations.
- Develop a mechanism (namespacing) that allows differentiation of payload properties with identical names at various levels for PUT and POST RestAPI operations.
- Aim to minimize breaking changes and maintain backward compatibility of the code as much as possible.

## Considered Options

- Enable the dynamic creation of payload and/or namespacing by default.
- Enable the dynamic creation of payload and/or namespacing based on configuration.

## Decision Outcome

Chosen option: "Enable the dynamic creation of payload and/or namespacing based on configuration". This option keeps things compatible, so the change won't affect any SK consumer code. Additionally, it provides flexibility for users to opt-in to the new functionality.

## Additional details

### Enabling dynamic creation of payload

To enable the dynamic creation of payloads/bodies for PUT and POST RestAPI operations, set the `EnableDynamicPayload` property of the `OpenApiSkillExecutionParameters` execution parameters to `true` when importing the AI plugin:

```csharp
var plugin = await kernel.ImportPluginFunctionsAsync("<skill name>", new Uri("<chatGPT-plugin>"), new OpenApiSkillExecutionParameters(httpClient) { EnableDynamicPayload = true });
```

To dynamically construct a payload for a RestAPI operation that requires a payload like this:

```json
{
  "value": "secret-value",
  "attributes": {
    "enabled": true
  }
}
```

Please register the following arguments in the context variables collection:

```csharp
var contextVariables = new ContextVariables();
contextVariables.Set("value", "secret-value");
contextVariables.Set("enabled", true);
```

### Enabling namespacing

To enable namespacing, set the `EnablePayloadNamespacing` property of the `OpenApiSkillExecutionParameters` execution parameters to `true` when importing the AI plugin:

```csharp
var plugin = await kernel.ImportPluginFunctionsAsync("<skill name>", new Uri("<chatGPT-plugin>"), new OpenApiSkillExecutionParameters(httpClient) { EnablePayloadNamespacing = true });
```

Remember that the namespacing mechanism depends on prefixing parameter names with their parent parameter name, separated by dots. So, use the 'namespaced' parameter names when adding arguments for payloads like this:

```json
{
  "upn": "<sender upn>",
  "receiver": {
    "upn": "<receiver upn>"
  },
  "cc": {
    "upn": "<cc upn>"
  }
}
```

The argument registration for the parameters (property values) will look like this:

```csharp
var contextVariables = new ContextVariables();
contextVariables.Set("upn", "<sender-upn-value>");
contextVariables.Set("receiver.upn", "<receiver-upn-value>");
contextVariables.Set("cc.upn", "<cc-upn-value>");
```
```
