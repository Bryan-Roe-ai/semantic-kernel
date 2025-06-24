# Architectural Decision Records (ADRs)

An Architectural Decision (AD) is a justified software design choice that addresses a functional or non-functional requirement that is architecturally significant. An Architectural Decision Record (ADR) captures a single AD and its rationale.

For more information [see](https://adr.github.io/)

## How are we using ADR's to track technical decisions?

1. Copy docs/decisions/adr-template.md to docs/decisions/NNNN-title-with-dashes.md, where NNNN indicates the next number in sequence.
    1. Check for existing PR's to make sure you use the correct sequence number.
    2. There is also a short form template docs/decisions/adr-short-template.md
2. Edit NNNN-title-with-dashes.md.
    1. Status must initially be `proposed`
    2. List of `deciders` must include the github ids of the people who will sign off on the decision.
    3. The relevant EM and architect must be listed as deciders or informed of all decisions.
    4. You should list the names or github ids of all partners who were consulted as part of the decision.
    5. Keep the list of `deciders` short. You can also list people who were `consulted` or `informed` about the decision.
3. For each option list the good, neutral and bad aspects of each considered alternative.
    1. Detailed investigations can be included in the `More Information` section inline or as links to external documents.
4. Share your PR with the deciders and other interested parties.
   1. Deciders must be listed as required reviewers.
   2. The status must be updated to `accepted` once a decision is agreed and the date must also be updated.
   3. Approval of the decision is captured using PR approval.
5. Decisions can be changed later and superseded by a new ADR. In this case it is useful to record any negative outcomes in the original ADR.

## Purpose of the `docs/decisions` Directory and the Use of ADRs

The purpose of the `docs/decisions` directory is to store architectural decision records (ADRs) for the project. These records document the context, decision drivers, considered options, and outcomes of significant architectural decisions made during the development of the project. This helps in maintaining a transparent decision-making process and provides a historical record of why certain decisions were made.

* The directory contains markdown files that follow a structured template to capture the details of each decision.
* Each file is named with a unique identifier and a descriptive title, making it easy to locate and reference specific decisions.
* The ADRs cover a wide range of topics, including project structure, error handling, support for multiple arguments in functions, and more.
* The records are intended to be easily discoverable for teams involved in the project, ensuring that architectural changes and the associated decision-making process are transparent to the community.
* The directory also includes templates for creating new ADRs, ensuring consistency in how decisions are documented.

## MADR Template and Its Structure

The MADR (Markdown Any Decision Records) template is used to document architectural decisions in a structured way. Here are the key points about the MADR template based on the repository:

* The `docs/decisions` directory contains architectural decision records (ADRs) that follow the MADR template.
* Each ADR is a markdown file named with a unique identifier and a descriptive title, such as `docs/decisions/0001-madr-architecture-decisions.md`.
* The template includes sections like status, date, deciders, context and problem statement, decision drivers, considered options, decision outcome, and more.
* The status of an ADR can be `proposed`, `accepted`, or `superseded`.
* The context and problem statement section describes the issue or decision to be made.
* The decision drivers section lists the factors influencing the decision.
* The considered options section outlines the different options considered for the decision.
* The decision outcome section details the chosen option and its pros and cons.
* The template ensures consistency and transparency in documenting architectural decisions.
* The repository includes a template file `docs/decisions/adr-template.md` for creating new ADRs.
* There is also a short form template `docs/decisions/adr-short-template.md` for simpler decisions.

## Benefits of Using ADRs in Software Projects

* ADRs provide a structured way to document significant architectural decisions, ensuring that the reasoning behind decisions is clear and accessible.
* They help maintain a historical record of decisions, making it easier to understand the evolution of the project's architecture.
* ADRs promote transparency and collaboration among team members, as decisions are documented and shared openly.
* They facilitate better communication and understanding among team members, especially when new members join the project.
* ADRs can serve as a reference for future decision-making, helping to avoid repeating past mistakes and ensuring consistency in the project's architecture.
* They provide a way to capture the context and problem statement for each decision, making it easier to understand the rationale behind the choices made.
* ADRs can help in identifying and evaluating alternative solutions, ensuring that the best possible decision is made based on the available information.
* They support the use of templates, such as the MADR template, which ensures consistency and completeness in documenting decisions.
* ADRs can be easily integrated into version control systems, making them accessible and maintainable alongside the project's codebase.
* They help in managing technical debt by providing a clear record of decisions that may need to be revisited or revised in the future.


---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**  
Copyright (c) 2025 Bryan Roe  
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
