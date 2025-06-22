// Copyright (c) Microsoft. All rights reserved.

using System;
using System.CommandLine;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using SemanticKernel.AutoTests;

namespace SemanticKernel.AutoTests.CLI;

/// <summary>
/// Console application for running automated tests.
/// </summary>
public class Program
{
    public static async Task<int> Main(string[] args)
    {
        var rootCommand = new RootCommand("Semantic Kernel Automated Test Runner");

        // Run all tests command
        var runAllCommand = new Command("run-all", "Run all discovered tests")
        {
            new Option<bool>("--verbose", "Enable verbose logging"),
            new Option<bool>("--parallel", () => true, "Enable parallel execution"),
            new Option<bool>("--coverage", "Collect code coverage"),
            new Option<string>("--filter", "Test filter pattern"),
            new Option<int>("--timeout", () => 10, "Timeout in minutes per project")
        };

        runAllCommand.SetHandler(async (bool verbose, bool parallel, bool coverage, string filter, int timeout) =>
        {
            var host = CreateHost(verbose);
            var runner = host.Services.GetRequiredService<AutoTestRunner>();

            var options = new TestRunOptions
            {
                Verbose = verbose,
                Parallel = parallel,
                CollectCoverage = coverage,
                Filter = filter,
                TimeoutMinutes = timeout
            };

            var results = await runner.RunAllTestsAsync(options);
            DisplayResults(results);
            
            Environment.ExitCode = results.AllPassed ? 0 : 1;
        }, new VerboseBinder(), new ParallelBinder(), new CoverageBinder(), new FilterBinder(), new TimeoutBinder());

        // Run specific tests command
        var runCommand = new Command("run", "Run tests matching a pattern")
        {
            new Argument<string>("pattern", "Pattern to match test projects"),
            new Option<bool>("--verbose", "Enable verbose logging"),
            new Option<bool>("--parallel", () => true, "Enable parallel execution"),
            new Option<bool>("--coverage", "Collect code coverage"),
            new Option<string>("--filter", "Test filter pattern"),
            new Option<int>("--timeout", () => 10, "Timeout in minutes per project")
        };

        runCommand.SetHandler(async (string pattern, bool verbose, bool parallel, bool coverage, string filter, int timeout) =>
        {
            var host = CreateHost(verbose);
            var runner = host.Services.GetRequiredService<AutoTestRunner>();

            var options = new TestRunOptions
            {
                Verbose = verbose,
                Parallel = parallel,
                CollectCoverage = coverage,
                Filter = filter,
                TimeoutMinutes = timeout
            };

            var results = await runner.RunTestsAsync(pattern, options);
            DisplayResults(results);
            
            Environment.ExitCode = results.AllPassed ? 0 : 1;
        }, new PatternBinder(), new VerboseBinder(), new ParallelBinder(), new CoverageBinder(), new FilterBinder(), new TimeoutBinder());

        // Discover tests command
        var discoverCommand = new Command("discover", "Discover all test projects")
        {
            new Option<bool>("--verbose", "Enable verbose logging")
        };

        discoverCommand.SetHandler(async (bool verbose) =>
        {
            var host = CreateHost(verbose);
            var runner = host.Services.GetRequiredService<AutoTestRunner>();

            var projects = await runner.DiscoverTestProjectsAsync();
            
            Console.WriteLine($"Discovered {projects.Count()} test projects:");
            foreach (var project in projects)
            {
                Console.WriteLine($"  {project.Name} ({project.Framework}, {project.TestType})");
                Console.WriteLine($"    Path: {project.Path}");
                Console.WriteLine($"    Runner: {project.TestRunner}");
                Console.WriteLine();
            }
        }, new VerboseBinder());

        // Watch mode command
        var watchCommand = new Command("watch", "Run tests in watch mode")
        {
            new Option<string>("--pattern", "Pattern to match test projects"),
            new Option<bool>("--verbose", "Enable verbose logging")
        };

        watchCommand.SetHandler(async (string pattern, bool verbose) =>
        {
            var host = CreateHost(verbose);
            var runner = host.Services.GetRequiredService<AutoTestRunner>();

            using var cts = new CancellationTokenSource();
            Console.CancelKeyPress += (_, _) => cts.Cancel();

            await runner.RunWatchModeAsync(pattern, cts.Token);
        }, new PatternWatchBinder(), new VerboseBinder());

        rootCommand.AddCommand(runAllCommand);
        rootCommand.AddCommand(runCommand);
        rootCommand.AddCommand(discoverCommand);
        rootCommand.AddCommand(watchCommand);

        return await rootCommand.InvokeAsync(args);
    }

    private static IHost CreateHost(bool verbose)
    {
        var configuration = new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory())
            .AddJsonFile("appsettings.json", optional: true)
            .AddEnvironmentVariables()
            .Build();

        return Host.CreateDefaultBuilder()
            .ConfigureLogging(logging =>
            {
                logging.ClearProviders();
                logging.AddConsole();
                logging.SetMinimumLevel(verbose ? LogLevel.Debug : LogLevel.Information);
            })
            .ConfigureServices(services =>
            {
                services.AddSingleton<IConfiguration>(configuration);
                services.AddSingleton<AutoTestRunner>();
            })
            .Build();
    }

    private static void DisplayResults(TestRunResults results)
    {
        Console.WriteLine();
        Console.WriteLine("=== Test Results ===");
        Console.WriteLine($"Total Tests: {results.TotalCount}");
        Console.WriteLine($"Passed: {results.PassedCount}");
        Console.WriteLine($"Failed: {results.FailedCount}");
        Console.WriteLine($"Skipped: {results.SkippedCount}");
        Console.WriteLine($"Duration: {results.TotalDuration:mm\\:ss}");
        Console.WriteLine($"Success Rate: {(double)results.PassedCount / Math.Max(1, results.TotalCount):P1}");
        Console.WriteLine();

        if (results.FailedCount > 0)
        {
            Console.WriteLine("=== Failed Projects ===");
            foreach (var result in results.Results.Where(r => !r.Success))
            {
                Console.WriteLine($"❌ {result.Project.Name}");
                if (!string.IsNullOrEmpty(result.ErrorMessage))
                    Console.WriteLine($"   Error: {result.ErrorMessage}");
                if (!string.IsNullOrEmpty(result.ErrorOutput))
                    Console.WriteLine($"   Output: {result.ErrorOutput.Split('\n').FirstOrDefault()}");
            }
            Console.WriteLine();
        }

        Console.WriteLine("=== Project Summary ===");
        foreach (var result in results.Results)
        {
            var status = result.Success ? "✅" : "❌";
            Console.WriteLine($"{status} {result.Project.Name} ({result.Duration:mm\\:ss}) - {result.PassedTests}P/{result.FailedTests}F/{result.SkippedTests}S");
        }
    }
}

// Command binding classes
internal class VerboseBinder : BinderBase<bool>
{
    protected override bool GetBoundValue(BindingContext bindingContext) =>
        bindingContext.ParseResult.GetValueForOption("--verbose");
}

internal class ParallelBinder : BinderBase<bool>
{
    protected override bool GetBoundValue(BindingContext bindingContext) =>
        bindingContext.ParseResult.GetValueForOption("--parallel");
}

internal class CoverageBinder : BinderBase<bool>
{
    protected override bool GetBoundValue(BindingContext bindingContext) =>
        bindingContext.ParseResult.GetValueForOption("--coverage");
}

internal class FilterBinder : BinderBase<string>
{
    protected override string GetBoundValue(BindingContext bindingContext) =>
        bindingContext.ParseResult.GetValueForOption("--filter") ?? string.Empty;
}

internal class TimeoutBinder : BinderBase<int>
{
    protected override int GetBoundValue(BindingContext bindingContext) =>
        bindingContext.ParseResult.GetValueForOption("--timeout");
}

internal class PatternBinder : BinderBase<string>
{
    protected override string GetBoundValue(BindingContext bindingContext) =>
        bindingContext.ParseResult.GetValueForArgument("pattern") ?? string.Empty;
}

internal class PatternWatchBinder : BinderBase<string>
{
    protected override string GetBoundValue(BindingContext bindingContext) =>
        bindingContext.ParseResult.GetValueForOption("--pattern") ?? string.Empty;
}
