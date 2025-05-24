using System;
using System.Diagnostics;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.SkillDefinition;

namespace Microsoft.SemanticKernel.Skills
{
    /// <summary>
    /// Skill that allows executing shell commands in a terminal without user input.
    /// </summary>
    public class TerminalSkill
    {
        [SKFunction("Runs a shell command asynchronously and returns its output.")]
        [SKFunctionInput(Description = "The shell command to execute.")]
        public async Task<string> RunAsync(string command, SKContext context)
        {
            var psi = new ProcessStartInfo
            {
                FileName = "/bin/bash",
                Arguments = $"-c \"{command}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = psi };
            process.Start();

            string output = await process.StandardOutput.ReadToEndAsync().ConfigureAwait(false);
            string error = await process.StandardError.ReadToEndAsync().ConfigureAwait(false);
            await process.WaitForExitAsync().ConfigureAwait(false);

            if (!string.IsNullOrEmpty(error))
            {
                context.Logger.LogWarning("Command '{Command}' produced errors: {Error}", command, error);
            }

            return string.IsNullOrEmpty(error) ? output : output + "\n" + error;
        }
    }
}
