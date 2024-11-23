// Copyright (c) Microsoft. All rights reserved.
using System.Text;
using Microsoft.SemanticKernel;
<<<<<<< HEAD
=======
using Resources;
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

namespace Step05;

/// <summary>
<<<<<<< HEAD
/// DEV HARNESS
=======
/// Demonstrate usage of <see cref="KernelProcessMap"/> for a map-reduce operation.
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
/// </summary>
public class Step05_MapReduce : BaseTest
{
    // Target Open AI Services
    protected override bool ForceOpenAI => true;

    /// <summary>
    /// Factor to increase the scale of the content processed.
<<<<<<< HEAD
    /// Factor to increase the scale of the content processed to highlight the characteristics of
    /// each approach: map vs linear.
=======
    /// Factor to increase the scale of the content processed.
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
    /// </summary>
    private const int ScaleFactor = 100;

    private readonly string _sourceContent;

    public Step05_MapReduce(ITestOutputHelper output)
         : base(output, redirectSystemConsoleOutput: true)
    {
<<<<<<< HEAD
=======
        // Initialize the test content
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        StringBuilder content = new();

        for (int count = 0; count < ScaleFactor; ++count)
        {
<<<<<<< HEAD
            content.AppendLine(File.ReadAllText("Grimms-The-King-of-the-Golden-Mountain.txt"));
            content.AppendLine(File.ReadAllText("Grimms-The-Water-of-Life.txt"));
            content.AppendLine(File.ReadAllText("Grimms-The-White-Snake.txt"));
=======
            content.AppendLine(EmbeddedResource.Read("Grimms-The-King-of-the-Golden-Mountain.txt"));
            content.AppendLine(EmbeddedResource.Read("Grimms-The-Water-of-Life.txt"));
            content.AppendLine(EmbeddedResource.Read("Grimms-The-White-Snake.txt"));
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        }

        this._sourceContent = content.ToString().ToUpperInvariant();
    }

    [Fact]
    public async Task RunMapReduceAsync()
    {
<<<<<<< HEAD
        KernelProcess process = SetupMapReduceProcess(nameof(RunMapReduceAsync), "Start");
=======
        // Define the process
        KernelProcess process = SetupMapReduceProcess(nameof(RunMapReduceAsync), "Start");

        // Execute the process
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        Kernel kernel = new();
        using LocalKernelProcessContext localProcess =
            await process.StartAsync(
                kernel,
                new KernelProcessEvent
                {
                    Id = "Start",
                    Data = this._sourceContent,
                });

<<<<<<< HEAD
=======
        // Display the results
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        Dictionary<string, int> results = (Dictionary<string, int>?)kernel.Data[ResultStep.ResultKey] ?? [];
        foreach (var result in results)
        {
            Console.WriteLine($"{result.Key}: {result.Value}");
        }
    }

<<<<<<< HEAD
    [Fact]
    public async Task RunLinearAsync()
    {
        Dictionary<string, int> counts = [];

        string[] words = this._sourceContent.Split([' ', '\n', '\r', '.', ',', '’'], StringSplitOptions.RemoveEmptyEntries);
        foreach (string word in words)
        {
            if (s_notInteresting.Contains(word))
            {
                continue;
            }

            counts.TryGetValue(word.Trim(), out int count);
            counts[word] = ++count;
        }

        var sorted =
            from kvp in counts
            orderby kvp.Value descending
            select kvp;

        foreach (var result in sorted.Take(10))
        {
            Console.WriteLine($"{result.Key}: {result.Value}");
        }
    }

=======
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
    private KernelProcess SetupMapReduceProcess(string processName, string inputEventId)
    {
        ProcessBuilder process = new(processName);

        ProcessStepBuilder chunkStep = process.AddStepFromType<ChunkStep>();
        process
            .OnInputEvent(inputEventId)
            .SendEventTo(new ProcessFunctionTargetBuilder(chunkStep));

<<<<<<< HEAD
        ProcessStepBuilder countStep = process.AddStepFromType<CountStep>();
        ProcessMapBuilder mapStep = process.AddMapForTarget(new ProcessFunctionTargetBuilder(countStep));
        chunkStep
            .OnEvent(ChunkStep.EventId)
            .SendEventTo(mapStep);
=======
        ProcessMapBuilder mapStep = process.AddMapStepFromType<CountStep>();
        chunkStep
            .OnEvent(ChunkStep.EventId)
            .SendEventTo(new ProcessFunctionTargetBuilder(mapStep));
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

        ProcessStepBuilder resultStep = process.AddStepFromType<ResultStep>();
        mapStep
            .OnEvent(CountStep.EventId)
            .SendEventTo(new ProcessFunctionTargetBuilder(resultStep));

        return process.Build();
    }

<<<<<<< HEAD
=======
    // Step for breaking the content into chunks
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
    private sealed class ChunkStep : KernelProcessStep
    {
        public const string EventId = "ChunkComplete";

        [KernelFunction]
        public async ValueTask ChunkAsync(KernelProcessStepContext context, string content)
        {
            int chunkSize = content.Length / Environment.ProcessorCount;
            string[] chunks = ChunkContent(content, chunkSize).ToArray();

            await context.EmitEventAsync(new() { Id = EventId, Data = chunks });
        }

        private IEnumerable<string> ChunkContent(string content, int chunkSize)
        {
            for (int index = 0; index < content.Length; index += chunkSize)
            {
                yield return content.Substring(index, Math.Min(chunkSize, content.Length - index));
            }
        }
    }

<<<<<<< HEAD
=======
    // Step for counting the words in a chunk
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
    private sealed class CountStep : KernelProcessStep
    {
        public const string EventId = "CountComplete";

        [KernelFunction]
        public async ValueTask ComputeAsync(KernelProcessStepContext context, string chunk)
        {
            Dictionary<string, int> counts = [];

            string[] words = chunk.Split([' ', '\n', '\r', '.', ',', '’'], StringSplitOptions.RemoveEmptyEntries);
            foreach (string word in words)
            {
                if (s_notInteresting.Contains(word))
                {
                    continue;
                }

                counts.TryGetValue(word.Trim(), out int count);
                counts[word] = ++count;
            }

            await context.EmitEventAsync(new() { Id = EventId, Data = counts });
        }
    }

<<<<<<< HEAD
=======
    // Step for combining the results
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
    private sealed class ResultStep : KernelProcessStep
    {
        public const string ResultKey = "WordCount";

        [KernelFunction]
        public async ValueTask ComputeAsync(KernelProcessStepContext context, IList<Dictionary<string, int>> results, Kernel kernel)
        {
            Dictionary<string, int> totals = [];

            foreach (Dictionary<string, int> result in results)
            {
                foreach (KeyValuePair<string, int> pair in result)
                {
                    totals.TryGetValue(pair.Key, out int count);
                    totals[pair.Key] = count + pair.Value;
                }
            }

            var sorted =
                from kvp in totals
                orderby kvp.Value descending
                select kvp;

            kernel.Data[ResultKey] = sorted.Take(10).ToDictionary(kvp => kvp.Key, kvp => kvp.Value);
        }
    }

<<<<<<< HEAD
=======
    // Uninteresting words to remove from content
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
    private static readonly HashSet<string> s_notInteresting =
        [
            "A",
            "ALL",
            "AN",
            "AND",
            "AS",
            "AT",
            "BE",
            "BEFORE",
            "BUT",
            "BY",
            "CAME",
            "COULD",
            "FOR",
            "GO",
            "HAD",
            "HAVE",
            "HE",
            "HER",
            "HIM",
            "HIMSELF",
            "HIS",
            "HOW",
            "I",
            "IF",
            "IN",
            "INTO",
            "IS",
            "IT",
            "ME",
            "MUST",
            "MY",
            "NO",
            "NOT",
            "NOW",
            "OF",
            "ON",
            "ONCE",
            "ONE",
            "ONLY",
            "OUT",
            "S",
            "SAID",
            "SAW",
            "SET",
            "SHE",
            "SHOULD",
            "SO",
            "THAT",
            "THE",
            "THEM",
            "THEN",
            "THEIR",
            "THERE",
            "THEY",
            "THIS",
            "TO",
            "VERY",
            "WAS",
            "WENT",
            "WERE",
            "WHAT",
            "WHEN",
            "WHO",
            "WILL",
            "WITH",
            "WOULD",
            "UP",
            "UPON",
            "YOU",
        ];
}
