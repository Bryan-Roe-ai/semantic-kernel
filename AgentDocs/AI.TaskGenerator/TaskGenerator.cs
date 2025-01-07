using System;
using System.Collections.Generic;

namespace AI.TaskGenerator
{
    public class TaskGenerator
    {
        public List<string> GenerateTasks(string purpose, string audience, string topic, string difficulty, string taskType)
        {
            // Placeholder for task generation logic
            List<string> tasks = new List<string>
            {
                $"Task 1 for {topic}",
                $"Task 2 for {topic}",
                $"Task 3 for {topic}"
            };

            return tasks;
        }

        public List<Task> GenerateTasks(string purpose, string audience, string topic, string difficulty, string taskType, string specificRequirements)
        {
            // Placeholder for task generation logic
            List<Task> tasks = new List<Task>
            {
                new Task { Description = $"Task 1 for {topic} with {specificRequirements}" },
                new Task { Description = $"Task 2 for {topic} with {specificRequirements}" },
                new Task { Description = $"Task 3 for {topic} with {specificRequirements}" }
            };

            return tasks;
        }
    }

    public class Task
    {
        public string Description { get; set; } = string.Empty;
    }
}
