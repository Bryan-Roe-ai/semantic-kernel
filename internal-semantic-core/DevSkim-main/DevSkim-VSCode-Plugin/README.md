# DevSkim

DevSkim is a framework of IDE extensions and language analyzers that provide inline security analysis in the dev environment as the developer writes code. It has a flexible rule model that supports multiple programming languages. The goal is to notify the developer as they are introducing a security vulnerability in order to fix the issue at the point of introduction, and to help build awareness for the developer.

## Features

* Built-in rules, and support for writing custom rules
* IntelliSense error "squiggly lines" for identified security issues
* Information and guidance provided for identified security issues
* Optional suppression of unwanted findings
* Broad language support including: C, C++, C#, Cobol, Go, Java, Javascript/Typescript, Python, and [more](https://github.com/Microsoft/DevSkim/wiki/Supported-Languages).

## Usage

As a developer writes code, DevSkim will flag identified security issues and call attention to them with errors or warnings. Mousing over the issue will show a description of the problem and how to address it, with a link to more information. For some issues, one or more safe alternatives are available in the lightbulb menu so that the issue can be fixed automatically. For issues where the alternative has different parameters than the unsafe API that is called out, guidance for the parameters will be inserted in the form of \<some guidance info\>. For example, when DevSkim turns gets() into fgets() it adds \<size of firstparamname\> to inform a user that they need to provide the size of the buffer.

![](https://raw.githubusercontent.com/microsoft/DevSkim/9c5a19ab8ff8a182c34ca100112d7c2803e0f180/DevSkim-VSCode-Plugin/vsc-example.gif)

### Suppressions

DevSkim has built-in ability to suppress any of its warnings, either permanently, or for a period of time. Permanent suppressions are for scenarios where, for whatever reason, the flagged code should not be changed. Timed suppressions are for scenarios where the code should change, but the developer does not want to change it immediately. In both cases, DevSkim will insert a comment after the code to notify it (and anyone reviewing the code) that the usage should be ignored, and in the case of timed suppressions, when DevSkim should alert again. Users can add additional comments after the suppression to describe why the issue is being suppressed.

For timed suppressions, the default period is 30 days, but this can be adjusted in the settings file.

Suppressions can be accessed from the lightbulb menu. Once a suppression is added, DevSkim will highlight the issue number that identifies the check being suppressed (the gets() example above is issue number DS181021 for example), and mousing over will provide details. This will let other contributors to a project know what was suppressed, and reduce confusion about the comment.

![](https://raw.githubusercontent.com/microsoft/DevSkim/9c5a19ab8ff8a182c34ca100112d7c2803e0f180/DevSkim-VSCode-Plugin/vsc-suppression-example.png)

## Rules

DevSkim takes an approach that is programming language agnostic. It primarily finds issues via regular expression, so rules can be written for just about any programming language. Out of the box, DevSkim can find dangerous crypto usage in most programming languages, and also includes rules for a range of language specific issues. The built-in ruleset is growing regularly, and it is very easy for users to write their own rules. For more information, see [Writing Rules](https://github.com/Microsoft/DevSkim/wiki/Writing-Rules).

## Building

In order to build you will need the latest .NET Core SDK as well as the appropriate version of node.js.

### Build Extension 
You can build the vsix directly with npm:
`npm run pack-ext`

### Debugging
To debug the code in vscode, you can use the `Client and Server` task that is defined. You will first need to setup the environment and build:

`npm run setup`
`tsc -b`

## Process Tracking Functionality

The DevSkim VS Code plugin now includes functionality to track and display processes happening behind the scenes. This feature helps developers understand what processes are running and provides insights into the development environment.

### Enabling Process Tracking

To enable process tracking, add the following settings to your `.vscode/settings.json` file:

```json
{
  "devskim.processTracking.enabled": true,
  "devskim.processTracking.behavior": "detailed"
}
```

### Running the Process Tracking Task

To run the process tracking task, add the following task to your `.vscode/tasks.json` file:

```json
{
  "label": "Track Processes",
  "type": "shell",
  "command": "node",
  "args": ["${workspaceFolder}/DevSkim-main/DevSkim-VSCode-Plugin/client/out/processTracker.js"],
  "problemMatcher": [],
  "runOptions": {
    "runOn": "fileSave"
  }
}
```

### Usage Example

Once the process tracking functionality is enabled and the task is configured, you can see the processes being tracked in the VS Code output panel. This provides real-time insights into the processes running in your development environment.

## Thank You

Thanks for trying DevSkim! If you find issues, please [report them on GitHub](https://github.com/Microsoft/DevSkim) and feel free to contribute!
