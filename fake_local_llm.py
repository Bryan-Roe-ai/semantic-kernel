import sys

print("[LLM DEMO] This is a simulated local LLM response.\n")
if len(sys.argv) > 1:
    print(f"Prompt: {sys.argv[1]}")
else:
    print("Prompt: <none provided>")
print(
    "\nResponse: Coding standards are essential for ensuring code quality, maintainability, and team collaboration."
)
