using System;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Skills;
using Microsoft.Extensions.Logging;

namespace TerminalSkillDemo
{
    /// <summary>
    /// This sample demonstrates how to use the TerminalSkill to run commands without user input.
    /// </summary>
    class Program
    {
        static async Task Main()
        {
            Console.WriteLine("Initializing Semantic Kernel and Terminal Skill...");

            // Create a kernel builder with logging
            var builder = new KernelBuilder();
            builder.WithLoggerFactory(LoggerFactory.Create(b => b.AddConsole().SetMinimumLevel(LogLevel.Information)));

            // Build the kernel
            var kernel = builder.Build();

            // Register the TerminalSkill
            var terminalSkill = new TerminalSkill();
            kernel.ImportSkill(terminalSkill, nameof(TerminalSkill));

            // Create arguments for the skill
            var arguments = new KernelArguments();

            // Set up examples of terminal commands to run
            string[] commands = new[]
            {
                "ls -la",
                "whoami",
                "echo 'Hello from Semantic Kernel TerminalSkill'",
                "pwd",
                "date"
            };

            // Run each command using the skill
            foreach (var command in commands)
            {
                Console.WriteLine($"\nExecuting command: {command}");
                try
                {
                    var result = await kernel.InvokeAsync(
                        nameof(TerminalSkill),
                        "RunAsync",
                        arguments.Update(command)
                    );

                    Console.WriteLine("\nResult:");
                    Console.WriteLine(result);
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error executing command: {ex.Message}");
                }
            }

            Console.WriteLine("\nTerminalSkill demo completed.");
        }
    }
}
