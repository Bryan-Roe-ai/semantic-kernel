# Amazon Bedrock AI Agents in Semantic Kernel

## Overview

AWS Bedrock Agents is a managed service that allows users to stand up and run AI agents in the AWS cloud quickly.

## Tools/Functions

Bedrock Agents allow the use of tools via [action groups](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-create.html).

The integration of Bedrock Agents with Semantic Kernel allows users to register kernel functions as tools in Bedrock Agents.

## Enable code interpretation

Bedrock Agents can write and execute code via a feature known as [code interpretation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-code-interpretation.html) similar to what OpenAI also offers.

## Enable user input

Bedrock Agents can [request user input](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-user-input.html) in case of missing information to invoke a tool. When this is enabled, the agent will prompt the user for the missing information. When this is disabled, the agent will guess the missing information.

## Knowledge base

Bedrock Agents can leverage data saved on AWS to perform RAG tasks, this is referred to as the [knowledge base](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-kb-add.html) in AWS.

## Multi-agent

Bedrock Agents support [multi-agent workflows](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html) for more complex tasks. However, it employs a different pattern than what we have in Semantic Kernel, thus this is not supported in the current integration.


---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**  
Copyright (c) 2025 Bryan Roe  
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
