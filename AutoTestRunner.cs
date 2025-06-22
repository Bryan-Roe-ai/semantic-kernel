// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace SemanticKernel.AutoTests;

/// <summary>
/// Automated test runner for Semantic Kernel projects.
/// Discovers and runs tests across .NET and Python implementations.
/// </summary>
public class AutoTestRunner
{
    private readonly ILogger<AutoTestRunner> _logger;
    private readonly IConfiguration _configuration;
    private readonly string _workspaceRoot;
    private readonly List<TestProject> _testProjects;

    public AutoTestRunner(ILogger<AutoTestRunner> logger, IConfiguration configuration)
    {
        this._logger = logger ?? throw new ArgumentNullException(nameof(logger));
        this._configuration = configuration ?? throw new ArgumentNullException(nameof(configuration));
        this._workspaceRoot = FindWorkspaceRoot();
        this._testProjects = new List<TestProject>();
    }

    /// <summary>
    /// Discovers all test projects in the workspace.
    /// </summary>
    public async Task<IEnumerable<TestProject>> DiscoverTestProjectsAsync()
    {
        this._logger.LogInformation("Discovering test projects in workspace: {WorkspaceRoot}", this._workspaceRoot);

        var testProjects = new List<TestProject>();

        // Discover .NET test projects
        await this.DiscoverDotNetTestProjectsAsync(testProjects);

        // Discover Python test projects
        await this.DiscoverPythonTestProjectsAsync(testProjects);

        // Discover JavaScript/TypeScript test projects
        await this.DiscoverJavaScriptTestProjectsAsync(testProjects);

        this._testProjects.AddRange(testProjects);
        this._logger.LogInformation("Discovered {Count} test projects", testProjects.Count);

        return testProjects;
    }

    /// <summary>
    /// Runs all discovered tests with parallel execution.
    /// </summary>
    public async Task<TestRunResults> RunAllTestsAsync(TestRunOptions? options = null)
    {
        options ??= new TestRunOptions();

        if (!this._testProjects.Any())
        {
            await this.DiscoverTestProjectsAsync();
        }

        this._logger.LogInformation("Running {Count} test projects", this._testProjects.Count);

        var results = new TestRunResults();
        var semaphore = new SemaphoreSlim(options.MaxParallelism, options.MaxParallelism);
        var tasks = this._testProjects.Select(async project =>
        {
            await semaphore.WaitAsync();
            try
            {
                var result = await this.RunTestProjectAsync(project, options);
                lock (results)
                {
                    results.AddResult(result);
                }
                return result;
            }
            finally
            {
                semaphore.Release();
            }
        });

        await Task.WhenAll(tasks);

        this._logger.LogInformation("Test run completed. Passed: {Passed}, Failed: {Failed}, Skipped: {Skipped}",
            results.PassedCount, results.FailedCount, results.SkippedCount);

        return results;
    }

    /// <summary>
    /// Runs tests for a specific project type or pattern.
    /// </summary>
    public async Task<TestRunResults> RunTestsAsync(string pattern, TestRunOptions? options = null)
    {
        options ??= new TestRunOptions();

        if (!this._testProjects.Any())
        {
            await this.DiscoverTestProjectsAsync();
        }

        var matchingProjects = this._testProjects.Where(p =>
            p.Name.Contains(pattern, StringComparison.OrdinalIgnoreCase) ||
            p.Path.Contains(pattern, StringComparison.OrdinalIgnoreCase) ||
            p.TestType.ToString().Contains(pattern, StringComparison.OrdinalIgnoreCase)
        ).ToList();

        this._logger.LogInformation("Running {Count} test projects matching pattern '{Pattern}'",
            matchingProjects.Count, pattern);

        var results = new TestRunResults();
        foreach (var project in matchingProjects)
        {
            var result = await this.RunTestProjectAsync(project, options);
            results.AddResult(result);
        }

        return results;
    }

    /// <summary>
    /// Runs a continuous test watch mode for development.
    /// </summary>
    public async Task RunWatchModeAsync(string? pattern = null, CancellationToken cancellationToken = default)
    {
        this._logger.LogInformation("Starting test watch mode...");

        var watcher = new FileSystemWatcher(this._workspaceRoot)
        {
            IncludeSubdirectories = true,
            NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.FileName | NotifyFilters.DirectoryName
        };

        var debounceTimer = new Timer(async _ =>
        {
            try
            {
                this._logger.LogInformation("File changes detected, running tests...");
                await this.DiscoverTestProjectsAsync();

                var results = string.IsNullOrEmpty(pattern)
                    ? await this.RunAllTestsAsync(new TestRunOptions { Verbose = false })
                    : await this.RunTestsAsync(pattern, new TestRunOptions { Verbose = false });

                this._logger.LogInformation("Watch run completed. Passed: {Passed}, Failed: {Failed}",
                    results.PassedCount, results.FailedCount);
            }
            catch (Exception ex)
            {
                this._logger.LogError(ex, "Error during watch mode test run");
            }
        }, null, Timeout.Infinite, Timeout.Infinite);

        watcher.Changed += (_, _) => debounceTimer.Change(2000, Timeout.Infinite);
        watcher.Created += (_, _) => debounceTimer.Change(2000, Timeout.Infinite);
        watcher.Deleted += (_, _) => debounceTimer.Change(2000, Timeout.Infinite);

        watcher.EnableRaisingEvents = true;

        this._logger.LogInformation("Test watch mode started. Press Ctrl+C to stop.");

        try
        {
            await Task.Delay(Timeout.Infinite, cancellationToken);
        }
        finally
        {
            watcher.Dispose();
            debounceTimer.Dispose();
        }
    }

    private async Task DiscoverDotNetTestProjectsAsync(List<TestProject> testProjects)
    {
        var dotnetRoot = Path.Combine(this._workspaceRoot, "01-core-implementations", "dotnet");
        if (!Directory.Exists(dotnetRoot))
            return;

        var testProjectFiles = Directory.GetFiles(dotnetRoot, "*Tests.csproj", SearchOption.AllDirectories)
            .Concat(Directory.GetFiles(dotnetRoot, "*.UnitTests.csproj", SearchOption.AllDirectories))
            .Concat(Directory.GetFiles(dotnetRoot, "*.IntegrationTests.csproj", SearchOption.AllDirectories));

        foreach (var projectFile in testProjectFiles)
        {
            var projectDir = Path.GetDirectoryName(projectFile)!;
            var projectName = Path.GetFileNameWithoutExtension(projectFile);

            var testType = projectName.Contains("Integration") ? TestType.Integration :
                          projectName.Contains("Unit") ? TestType.Unit :
                          TestType.Mixed;

            testProjects.Add(new TestProject
            {
                Name = projectName,
                Path = projectDir,
                ProjectFile = projectFile,
                TestType = testType,
                Framework = TestFramework.DotNet,
                TestRunner = "dotnet test",
                SupportsParallel = true
            });
        }

        this._logger.LogDebug("Discovered {Count} .NET test projects", testProjectFiles.Count());
    }

    private async Task DiscoverPythonTestProjectsAsync(List<TestProject> testProjects)
    {
        var pythonRoot = Path.Combine(this._workspaceRoot, "python");
        if (!Directory.Exists(pythonRoot))
            return;

        var testDirs = new[]
        {
            Path.Combine(pythonRoot, "tests", "unit"),
            Path.Combine(pythonRoot, "tests", "integration"),
            Path.Combine(pythonRoot, "tests", "end-to-end")
        };

        foreach (var testDir in testDirs.Where(Directory.Exists))
        {
            var testType = Path.GetFileName(testDir) switch
            {
                "unit" => TestType.Unit,
                "integration" => TestType.Integration,
                "end-to-end" => TestType.EndToEnd,
                _ => TestType.Mixed
            };

            testProjects.Add(new TestProject
            {
                Name = $"Python.{Path.GetFileName(testDir)}",
                Path = testDir,
                ProjectFile = Path.Combine(pythonRoot, "pyproject.toml"),
                TestType = testType,
                Framework = TestFramework.Python,
                TestRunner = "poetry run pytest",
                SupportsParallel = true
            });
        }

        this._logger.LogDebug("Discovered {Count} Python test projects", testDirs.Count(Directory.Exists));
    }

    private async Task DiscoverJavaScriptTestProjectsAsync(List<TestProject> testProjects)
    {
        var jsRoot = Path.Combine(this._workspaceRoot, "typescript");
        if (!Directory.Exists(jsRoot))
            return;

        var packageJsonFiles = Directory.GetFiles(jsRoot, "package.json", SearchOption.AllDirectories);

        foreach (var packageFile in packageJsonFiles)
        {
            var projectDir = Path.GetDirectoryName(packageFile)!;
            var hasTests = Directory.Exists(Path.Combine(projectDir, "tests")) ||
                          Directory.Exists(Path.Combine(projectDir, "test")) ||
                          Directory.GetFiles(projectDir, "*.test.*", SearchOption.AllDirectories).Any();

            if (hasTests)
            {
                testProjects.Add(new TestProject
                {
                    Name = $"TypeScript.{Path.GetFileName(projectDir)}",
                    Path = projectDir,
                    ProjectFile = packageFile,
                    TestType = TestType.Mixed,
                    Framework = TestFramework.JavaScript,
                    TestRunner = "npm test",
                    SupportsParallel = false
                });
            }
        }

        this._logger.LogDebug("Discovered {Count} JavaScript/TypeScript test projects", packageJsonFiles.Length);
    }

    private async Task<TestProjectResult> RunTestProjectAsync(TestProject project, TestRunOptions options)
    {
        this._logger.LogInformation("Running tests for {ProjectName} ({Framework})", project.Name, project.Framework);

        var stopwatch = Stopwatch.StartNew();
        var result = new TestProjectResult
        {
            Project = project,
            StartTime = DateTime.UtcNow
        };

        try
        {
            var processInfo = new ProcessStartInfo
            {
                FileName = GetTestCommand(project),
                Arguments = GetTestArguments(project, options),
                WorkingDirectory = project.Path,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = processInfo };

            var outputBuilder = new List<string>();
            var errorBuilder = new List<string>();

            process.OutputDataReceived += (_, e) =>
            {
                if (e.Data != null)
                {
                    outputBuilder.Add(e.Data);
                    if (options.Verbose)
                        this._logger.LogDebug("[{ProjectName}] {Output}", project.Name, e.Data);
                }
            };

            process.ErrorDataReceived += (_, e) =>
            {
                if (e.Data != null)
                {
                    errorBuilder.Add(e.Data);
                    if (options.Verbose)
                        this._logger.LogWarning("[{ProjectName}] {Error}", project.Name, e.Data);
                }
            };

            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            var timeout = options.TimeoutMinutes > 0
                ? TimeSpan.FromMinutes(options.TimeoutMinutes)
                : TimeSpan.FromMinutes(10); // Default timeout

            if (!process.WaitForExit((int)timeout.TotalMilliseconds))
            {
                process.Kill();
                result.Success = false;
                result.ErrorMessage = $"Test execution timed out after {timeout.TotalMinutes} minutes";
            }
            else
            {
                result.Success = process.ExitCode == 0;
                result.ExitCode = process.ExitCode;
            }

            result.Output = string.Join(Environment.NewLine, outputBuilder);
            result.ErrorOutput = string.Join(Environment.NewLine, errorBuilder);

            // Parse test results from output
            this.ParseTestResults(result);
        }
        catch (Exception ex)
        {
            result.Success = false;
            result.ErrorMessage = ex.Message;
            this._logger.LogError(ex, "Error running tests for {ProjectName}", project.Name);
        }
        finally
        {
            stopwatch.Stop();
            result.Duration = stopwatch.Elapsed;
            result.EndTime = DateTime.UtcNow;
        }

        var status = result.Success ? "PASSED" : "FAILED";
        this._logger.LogInformation("Tests for {ProjectName} {Status} in {Duration:mm\\:ss}",
            project.Name, status, result.Duration);

        return result;
    }

    private void ParseTestResults(TestProjectResult result)
    {
        var output = result.Output ?? string.Empty;

        // Parse .NET test results
        if (result.Project.Framework == TestFramework.DotNet)
        {
            // Example: "Total tests: 42. Passed: 40. Failed: 2. Skipped: 0."
            var lines = output.Split('\n');
            foreach (var line in lines)
            {
                if (line.Contains("Total tests:"))
                {
                    var parts = line.Split('.');
                    foreach (var part in parts)
                    {
                        if (part.Contains("Total tests:"))
                            result.TotalTests = ExtractNumber(part);
                        else if (part.Contains("Passed:"))
                            result.PassedTests = ExtractNumber(part);
                        else if (part.Contains("Failed:"))
                            result.FailedTests = ExtractNumber(part);
                        else if (part.Contains("Skipped:"))
                            result.SkippedTests = ExtractNumber(part);
                    }
                    break;
                }
            }
        }
        // Parse Python pytest results
        else if (result.Project.Framework == TestFramework.Python)
        {
            // Example: "= 42 passed, 2 failed, 1 skipped in 10.5s ="
            var lines = output.Split('\n');
            foreach (var line in lines)
            {
                if (line.Contains("passed") && line.Contains("failed"))
                {
                    result.PassedTests = ExtractPytestNumber(line, "passed");
                    result.FailedTests = ExtractPytestNumber(line, "failed");
                    result.SkippedTests = ExtractPytestNumber(line, "skipped");
                    result.TotalTests = result.PassedTests + result.FailedTests + result.SkippedTests;
                    break;
                }
            }
        }
    }

    private static int ExtractNumber(string text)
    {
        var match = System.Text.RegularExpressions.Regex.Match(text, @"\d+");
        return match.Success ? int.Parse(match.Value) : 0;
    }

    private static int ExtractPytestNumber(string line, string keyword)
    {
        var pattern = $@"(\d+)\s+{keyword}";
        var match = System.Text.RegularExpressions.Regex.Match(line, pattern);
        return match.Success ? int.Parse(match.Groups[1].Value) : 0;
    }

    private static string GetTestCommand(TestProject project)
    {
        return project.Framework switch
        {
            TestFramework.DotNet => "dotnet",
            TestFramework.Python => "poetry",
            TestFramework.JavaScript => "npm",
            _ => throw new NotSupportedException($"Framework {project.Framework} not supported")
        };
    }

    private static string GetTestArguments(TestProject project, TestRunOptions options)
    {
        return project.Framework switch
        {
            TestFramework.DotNet => BuildDotNetArgs(project, options),
            TestFramework.Python => BuildPythonArgs(project, options),
            TestFramework.JavaScript => BuildJavaScriptArgs(project, options),
            _ => throw new NotSupportedException($"Framework {project.Framework} not supported")
        };
    }

    private static string BuildDotNetArgs(TestProject project, TestRunOptions options)
    {
        var args = new List<string> { "test" };

        if (!string.IsNullOrEmpty(project.ProjectFile))
            args.Add($"\"{project.ProjectFile}\"");

        args.Add("--configuration Release");
        args.Add("--logger \"console;verbosity=normal\"");

        if (options.CollectCoverage)
            args.Add("--collect:\"XPlat Code Coverage\"");

        if (!string.IsNullOrEmpty(options.Filter))
            args.Add($"--filter \"{options.Filter}\"");

        if (options.Parallel && project.SupportsParallel)
            args.Add("--parallel");

        return string.Join(" ", args);
    }

    private static string BuildPythonArgs(TestProject project, TestRunOptions options)
    {
        var args = new List<string> { "run", "pytest" };

        args.Add($"\"{project.Path}\"");
        args.Add("-v");

        if (options.CollectCoverage)
            args.Add("--cov=semantic_kernel --cov-report=xml");

        if (!string.IsNullOrEmpty(options.Filter))
            args.Add($"-k \"{options.Filter}\"");

        if (options.Parallel && project.SupportsParallel)
            args.Add("-n auto");

        return string.Join(" ", args);
    }

    private static string BuildJavaScriptArgs(TestProject project, TestRunOptions options)
    {
        return "test";
    }

    private string FindWorkspaceRoot()
    {
        var current = Directory.GetCurrentDirectory();
        while (current != null)
        {
            if (File.Exists(Path.Combine(current, "LICENSE")) &&
                Directory.Exists(Path.Combine(current, "dotnet")) &&
                Directory.Exists(Path.Combine(current, "python")))
            {
                return current;
            }
            current = Directory.GetParent(current)?.FullName;
        }
        return Directory.GetCurrentDirectory();
    }
}

/// <summary>
/// Represents a test project in the workspace.
/// </summary>
public class TestProject
{
    public string Name { get; set; } = string.Empty;
    public string Path { get; set; } = string.Empty;
    public string ProjectFile { get; set; } = string.Empty;
    public TestType TestType { get; set; }
    public TestFramework Framework { get; set; }
    public string TestRunner { get; set; } = string.Empty;
    public bool SupportsParallel { get; set; }
}

/// <summary>
/// Test execution options.
/// </summary>
public class TestRunOptions
{
    public bool Verbose { get; set; } = false;
    public bool Parallel { get; set; } = true;
    public bool CollectCoverage { get; set; } = false;
    public string? Filter { get; set; }
    public int MaxParallelism { get; set; } = Environment.ProcessorCount;
    public int TimeoutMinutes { get; set; } = 10;
}

/// <summary>
/// Results from running a single test project.
/// </summary>
public class TestProjectResult
{
    public TestProject Project { get; set; } = null!;
    public bool Success { get; set; }
    public int ExitCode { get; set; }
    public TimeSpan Duration { get; set; }
    public DateTime StartTime { get; set; }
    public DateTime EndTime { get; set; }
    public string? Output { get; set; }
    public string? ErrorOutput { get; set; }
    public string? ErrorMessage { get; set; }
    public int TotalTests { get; set; }
    public int PassedTests { get; set; }
    public int FailedTests { get; set; }
    public int SkippedTests { get; set; }
}

/// <summary>
/// Aggregated results from multiple test projects.
/// </summary>
public class TestRunResults
{
    private readonly List<TestProjectResult> _results = new();

    public IReadOnlyList<TestProjectResult> Results => this._results;
    public int PassedCount => this._results.Sum(r => r.PassedTests);
    public int FailedCount => this._results.Sum(r => r.FailedTests);
    public int SkippedCount => this._results.Sum(r => r.SkippedTests);
    public int TotalCount => this._results.Sum(r => r.TotalTests);
    public TimeSpan TotalDuration => TimeSpan.FromTicks(this._results.Sum(r => r.Duration.Ticks));
    public bool AllPassed => this._results.All(r => r.Success);

    public void AddResult(TestProjectResult result)
    {
        this._results.Add(result);
    }
}

public enum TestType
{
    Unit,
    Integration,
    EndToEnd,
    Mixed
}

public enum TestFramework
{
    DotNet,
    Python,
    JavaScript
}
