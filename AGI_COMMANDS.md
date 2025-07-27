# AGI Command Reference

This guide summarizes the main scripts used to interact with the AGI tooling in this repository.

## AGI Command Line Interface

The `agi_cli.py` script exposes several sub‑commands for performing reasoning and automation tasks.

```
python agi_cli.py <command> [args]
```

Available commands:

- `reason <query>` – perform AGI reasoning on a question
- `file <filename> [operation]` – analyze, optimize, transform or summarize a file
- `code <language> <description>` – generate code in the chosen language
- `plan <goal>` – create and execute a plan for a goal
- `help` – show the help message

Example usage:

```
python agi_cli.py reason "How does machine learning work?"
python agi_cli.py file myfile.txt analyze
python agi_cli.py code python "Create a web scraper"
python agi_cli.py plan "Build a recommendation system"
```

## Local Agent Launcher

`local_agent_launcher.py` manages background AGI agents. You can list, start, stop or inspect agent status from the command line:

```
python local_agent_launcher.py list
python local_agent_launcher.py status
python local_agent_launcher.py start
python local_agent_launcher.py stop
```

Running without arguments opens an interactive menu where you can choose these options.

## Demo and Dashboard

- `demo_local_agents.py` – launches an interactive demonstration of local AGI agents.
- `agi_status_dashboard.py` – shows running processes and quick start commands.

Typical commands:

```
python demo_local_agents.py
python agi_status_dashboard.py
```
