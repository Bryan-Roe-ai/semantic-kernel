# Java Reference Skill gRPC Server
This is a sample Java gRPC server that can be invoked via SK's gRPC client as a Native Skill/Function. The purpose of this project is to demonstrate how Polyglot skills can be supported using either REST or gRPC.

## Prerequisites
* Java 17
* Maven

## Build
To build the project, run the following command:
```
mvn clean package
```
To generate the gRPC classes, run the following command:
```
mvn protobuf:compile
```

## Run
To run the project, run the following command:
```
java -jar ./target/JavaReferenceSkill-1.0-SNAPSHOT-jar-with-dependencies.jar
```



---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**  
Copyright (c) 2025 Bryan Roe  
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
