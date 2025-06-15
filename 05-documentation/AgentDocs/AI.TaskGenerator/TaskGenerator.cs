using System;
using System.Collections.Generic;

namespace AI.TaskGenerator
{
    public class TaskGenerator
    {
        public List<Task> GenerateTasks(string purpose, string audience, string topic, string difficulty, string taskType)
        {
            // Placeholder for task generation logic
            List<Task> tasks = new List<Task>
            {
                new Task { Description = $"Task 1 for {topic}" },
                new Task { Description = $"Task 2 for {topic}" },
                new Task { Description = $"Task 3 for {topic}" }
            };

            return tasks;
        }
    }

    public class Task
    {
        public string Description { get; set; } = string.Empty;
    }
}
