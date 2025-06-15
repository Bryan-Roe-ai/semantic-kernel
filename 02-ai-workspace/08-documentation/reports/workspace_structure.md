# AI Workspace Structure Report

Generated: 2025-06-15 17:52:25

## Directory Structure
```
├── .vscode
│   └── settings.json
├── 01-notebooks
│   ├── notebooks
│   │   ├── ai.ipynb
│   │   ├── app.ipynb
│   │   ├── ipython.ipynb
│   │   └── python3.ipynb
│   ├── README.md
│   ├── ai.ipynb?4e25f261-cb8b-4583-9e1b-1731602b9851
│   ├── app.ipynb?4e25f261-cb8b-4583-9e1b-1731602b9851
│   └── quick-start.ipynb
├── 02-agents
│   ├── AgentDocs
│   │   ├── AI.TaskGenerator
│   │   ├── AgentCollaboration
│   │   ├── AgentPlugins
│   │   ├── AssistantCodeInterpreter
│   │   ├── AssistantFileSearch
│   │   ├── Common
│   │   └── AgentDocs.sln
│   ├── aipmakerday
│   │   ├── .media
│   │   ├── helloagents
│   │   ├── shared
│   │   ├── solutions
│   │   ├── Code Examples.pptx
│   │   ├── Directory.Build.props
│   │   ├── Nuget.config
│   │   ├── Readme.md
│   │   ├── SK101 Agents - Solutions.sln
│   │   └── SK101 Agents.sln
│   ├── README.md
│   └── ai-chat-launcher.hta
├── 03-models-training
│   ├── README.md
│   ├── advanced_llm_trainer.py
│   ├── collect_llm_training_data.py
│   ├── finetune_gpt2_custom.py
│   ├── mcp_server.py
│   └── simple_llm_demo.py
├── 04-plugins
│   ├── plugins
│   │   ├── math
│   │   ├── text
│   │   ├── DataAnalysisFunctions.py
│   │   ├── DataFunctions.py
│   │   ├── FileOperations.py
│   │   ├── FileOperationsFunctions.py
│   │   ├── MathFunctions.py
│   │   └── TextFunctions.py
│   ├── prompt_template_samples
│   │   ├── CalendarPlugin
│   │   ├── ChatPlugin
│   │   ├── ChildrensBookPlugin
│   │   ├── ClassificationPlugin
│   │   ├── CodingPlugin
│   │   ├── FunPlugin
│   │   ├── GroundingPlugin
│   │   ├── IntentDetectionPlugin
│   │   ├── MiscPlugin
│   │   ├── QAPlugin
│   │   ├── SummarizePlugin
│   │   └── WriterPlugin
│   ├── README.md
│   └── github_mcp_integration.py
├── 05-samples-demos
│   ├── samples
│   │   ├── apps
│   │   ├── dotnet
│   │   ├── java
│   │   ├── notebooks
│   │   ├── plugins
│   │   ├── skills
│   │   ├── New Text Document (2).txt
│   │   ├── New Text Document (3).txt
│   │   └── New Text Document.txt
│   ├── README.md
│   ├── custom-llm-studio.html
│   ├── express-rate.js
│   ├── index.html
│   └── server.js
├── 06-backend-services
│   ├── AzureFunctions
│   │   ├── .vscode
│   │   ├── .gitignore
│   │   ├── function_app.py
│   │   ├── host.json
│   │   └── requirements.txt
│   ├── README.md
│   ├── api_server.py
│   ├── app.py
│   ├── backend-starter.py
│   ├── backend.py
│   ├── backend_starter_server.py
│   ├── cloud_deploy.py
│   ├── collect_llm_training_data.py
│   ├── diagnose_system.py
│   ├── error_handling.py
│   ├── file_analyzer.py
│   ├── finetune_gpt2_custom.py
│   ├── mcp_client.py
│   ├── metrics_logger.py
│   ├── plugin_hotreload.py
│   ├── self_heal.py
│   ├── setup.py
│   ├── simple_api_server.py
│   ├── simple_llm_demo.py
│   ├── start_backend.py
│   ├── start_chat_unified.py
│   ├── test_backend.py
│   └── test_system.py
├── 07-data-resources
│   ├── data
│   ├── devdata
│   │   ├── work-items-in
│   │   ├── env-consumer.json
│   │   ├── env-producer.json
│   │   ├── env-reporter.json
│   │   └── env.json
│   ├── resources
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── keywords.robot
│   │   └── variables.py
│   ├── results
│   │   ├── log.html
│   │   ├── output.xml
│   │   └── report.html
│   ├── uploads
│   │   ├── 20250522_222910_TRANSPARENCY_FAQS.md
│   │   ├── company.json
│   │   └── employees.csv
│   ├── README.md
│   ├── index.xml
│   └── output.xml
├── 08-documentation
│   ├── docs
│   │   ├── adr-reports
│   │   ├── code_maps
│   │   ├── decisions
│   │   ├── images
│   │   ├── CODE_OF_CONDUCT.md
│   │   ├── COMMUNITY.md
│   │   ├── CONTRIBUTING.md
│   │   ├── COSINE_SIMILARITY.md
│   │   ├── Code_Comments.md
│   │   ├── DOT_PRODUCT.md
│   │   ├── EMBEDDINGS.md
│   │   ├── EUCLIDEAN_DISTANCE.md
│   │   ├── FAQ.md
│   │   ├── FAQS.md
│   │   ├── FEATURE_MATRIX.md
│   │   ├── GLOSSARY.md
│   │   ├── Getting_Started.md
│   │   ├── Installation.md
│   │   ├── LM_STUDIO_README.md
│   │   ├── PLANNER.md
│   │   ├── PLANNERS.md
│   │   ├── PLUGINS.md
│   │   ├── PROMPT_TEMPLATE_LANGUAGE.md
│   │   ├── README.md
│   │   ├── README_CHAT.md
│   │   ├── README_CHAT_APP.md
│   │   ├── Repository_Structure.md
│   │   ├── SECURITY-01J61242EAQ4X95NFYMEYY0EEG.md
│   │   ├── SECURITY.md
│   │   ├── SETUP_AND_USAGE.md
│   │   ├── SKILLS.md
│   │   ├── TRANSPARENCY_FAQS.md
│   │   ├── UPDATES.md
│   │   ├── automate_runtime.md
│   │   ├── index.html
│   │   └── sample-data.md
│   ├── reports
│   ├── BR-AI.txt
│   ├── Documentation 1.txt
│   ├── Documentation 2.txt
│   ├── Documentation 3.txt
│   └── README.md
├── 09-deployment
│   ├── circleci
│   │   └── config.yml
│   ├── Dockerfile
│   ├── README.md
│   ├── dotnet-install.sh.1
│   ├── dotnet-install.sh.2
│   └── entrypoint.sh.template
├── 10-config
│   ├── config
│   │   ├── appsettings.json
│   │   └── logging.json
│   ├── configs
│   │   ├── Code.prompt.yml
│   │   ├── FastAPI.json
│   │   ├── appsettings.Development.json
│   │   ├── appsettings.json
│   │   ├── astro.yml
│   │   ├── azure-container-webapp.yml
│   │   ├── azure-pipelines.yml
│   │   ├── compose-dev.yaml
│   │   ├── conda.yaml
│   │   ├── config.json
│   │   ├── devcontainer.json
│   │   ├── docker-image.yml
│   │   ├── dotnet-ci.yml
│   │   ├── file-updater.prompt.yml
│   │   ├── jsconfig.json
│   │   ├── main.yml
│   │   ├── mcp.json
│   │   ├── npm-grunt.yml
│   │   ├── npm-gulp.yml
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── python-app.yml
│   │   ├── python-publish.yml
│   │   ├── python-test-coverage.yml
│   │   ├── robot.yaml
│   │   └── static-analysis.datadog.yml
│   ├── README.md
│   ├── nuget.config
│   ├── requirements.txt
│   └── vcpkg-configuration.jsonc
├── backups
│   └── 20250615_162932
│       ├── .vscode
│       └── requirements.txt
├── batches
│   ├── full-deployment.batch
│   ├── maintenance.batch
│   └── quick-setup.batch
├── cache
├── data
├── deployments
│   └── deployment_20250615_175142.json
├── dist
│   ├── backend
│   │   ├── AzureFunctions
│   │   ├── README.md
│   │   ├── api_server.py
│   │   ├── app.py
│   │   ├── backend-starter.py
│   │   ├── backend.py
│   │   ├── backend_starter_server.py
│   │   ├── cloud_deploy.py
│   │   ├── collect_llm_training_data.py
│   │   ├── diagnose_system.py
│   │   ├── error_handling.py
│   │   ├── file_analyzer.py
│   │   ├── finetune_gpt2_custom.py
│   │   ├── metrics_logger.py
│   │   ├── plugin_hotreload.py
│   │   ├── self_heal.py
│   │   ├── setup.py
│   │   ├── simple_api_server.py
│   │   ├── simple_llm_demo.py
│   │   ├── start_backend.py
│   │   ├── start_chat_unified.py
│   │   ├── test_backend.py
│   │   └── test_system.py
│   ├── Dockerfile
│   ├── ISSUE_RESOLUTION.md
│   ├── README-workspace.md
│   ├── README.md
│   ├── SUCCESS_SUMMARY.md
│   ├── _config.yml
│   ├── custom-llm-studio.html
│   ├── deployment-info.txt
│   ├── docker-compose.dev.yml
│   ├── docker-compose.yml
│   ├── index.html
│   └── requirements-minimal.txt
├── docker
│   ├── entrypoint.sh
│   ├── nginx.conf
│   └── supervisord.conf
├── logs
│   └── cleanup.log
├── models
│   └── model_index.json
├── scripts
│   ├── ai_model_manager.py
│   ├── ai_workspace_monitor.py
│   ├── ai_workspace_optimizer.py
│   ├── build_static.sh
│   ├── cleanup_and_automate.sh
│   ├── deployment_automator.py
│   ├── docker_manager.sh
│   ├── github_actions_check.sh
│   ├── integration_test.sh
│   ├── mcp_integration_test.py
│   ├── test_api_endpoints.sh
│   └── validate_deployment.sh
├── test-dist
│   ├── samples
│   │   ├── apps
│   │   ├── dotnet
│   │   ├── java
│   │   ├── notebooks
│   │   ├── plugins
│   │   ├── skills
│   │   ├── New Text Document (2).txt
│   │   ├── New Text Document (3).txt
│   │   └── New Text Document.txt
│   ├── README.md
│   ├── custom-llm-studio.html
│   ├── express-rate.js
│   ├── index.html
│   └── server.js
├── uploads
├── venv
│   ├── bin
│   │   ├── Activate.ps1
│   │   ├── activate
│   │   ├── activate.csh
│   │   ├── activate.fish
│   │   ├── dotenv
│   │   ├── fastapi
│   │   ├── pip
│   │   ├── pip3
│   │   ├── pip3.12
│   │   ├── python
│   │   ├── python3
│   │   ├── python3.12
│   │   ├── uvicorn
│   │   ├── watchfiles
│   │   └── websockets
│   ├── include
│   │   └── python3.12
│   ├── lib
│   │   └── python3.12
│   ├── lib64
│   │   └── python3.12
│   └── pyvenv.cfg
├── .dockerignore
├── .env
├── .env.template
├── ADVANCED_FEATURES_GUIDE.md
├── DEPLOYMENT_READY.md
├── DOCKER_GUIDE.md
├── Dockerfile
├── GITHUB_ACTIONS_GUIDE.md
├── GITHUB_PAGES_GUIDE.md
├── IMPLEMENTATION_COMPLETE.md
├── ISSUE_RESOLUTION.md
├── MCP_INTEGRATION_GUIDE.md
├── README.md
├── SUCCESS_SUMMARY.md
├── ai_workspace_control.py
├── ai_workspace_manager.py
├── docker-compose.dev.yml
├── docker-compose.yml
├── get-pip.py
├── launch.sh
├── organize_files.py
├── requirements-basic.txt
├── requirements-minimal.txt
└── requirements.txt
```