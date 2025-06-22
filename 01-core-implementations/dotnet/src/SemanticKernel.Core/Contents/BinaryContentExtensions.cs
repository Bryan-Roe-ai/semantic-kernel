// Copyright (c) Microsoft. All rights reserved.

using System;
using System.IO;
using System.Threading.Tasks;

namespace Microsoft.SemanticKernel;

/// <summary>
/// Provides extension methods for interacting with <see cref="BinaryContent"/>.
/// </summary>
public static class BinaryContentExtensions
{
    /// <summary>
    /// Writes the content to a file.
    /// </summary>
    /// <param name="content">The content to write.</param>
    /// <param name="filePath">The path to the file to write to.</param>
    /// <param name="overwrite">Whether to overwrite the file if it already exists.</param>
    public static void WriteToFile(this BinaryContent content, string filePath, bool overwrite = false)
    {
        if (string.IsNullOrWhiteSpace(filePath))
        {
            throw new ArgumentException("File path cannot be null or empty", nameof(filePath));
        }

        if (!overwrite && File.Exists(filePath))
        {
            throw new InvalidOperationException("File already exists.");
        }

        if (!content.CanRead)
        {
            throw new InvalidOperationException("No content to write to file.");
        }

        File.WriteAllBytes(filePath, content.Data!.Value.ToArray());
    }

    /// <summary>
    /// Writes the content to a file asynchronously with AGI-enhanced error handling.
    /// </summary>
    /// <param name="content">The content to write.</param>
    /// <param name="filePath">The path to the file to write to.</param>
    /// <param name="overwrite">Whether to overwrite the file if it already exists.</param>
    /// <param name="createBackup">Whether to create a backup before overwriting.</param>
    /// <returns>A task representing the asynchronous operation.</returns>
    public static async Task WriteToFileAsync(this BinaryContent content, string filePath,
        bool overwrite = false, bool createBackup = true)
    {
        if (string.IsNullOrWhiteSpace(filePath))
        {
            throw new ArgumentException("File path cannot be null or empty", nameof(filePath));
        }

        if (!overwrite && File.Exists(filePath))
        {
            throw new InvalidOperationException("File already exists.");
        }

        if (!content.CanRead)
        {
            throw new InvalidOperationException("No content to write to file.");
        }

        // Create backup if requested and file exists
        if (createBackup && overwrite && File.Exists(filePath))
        {
            var backupPath = $"{filePath}.backup.{DateTime.Now:yyyyMMdd_HHmmss}";
            File.Copy(filePath, backupPath);
        }

        await File.WriteAllBytesAsync(filePath, content.Data!.Value.ToArray());
    }

    /// <summary>
    /// Writes the content to a file with AGI integration for autonomous updates.
    /// </summary>
    /// <param name="content">The content to write.</param>
    /// <param name="filePath">The path to the file to write to.</param>
    /// <param name="options">File writing options including AGI integration settings.</param>
    /// <returns>A task representing the asynchronous operation with AGI metadata.</returns>
    public static async Task<FileWriteResult> WriteToFileWithAGIAsync(this BinaryContent content,
        string filePath, AGIFileWriteOptions? options = null)
    {
        options ??= new AGIFileWriteOptions();

        var result = new FileWriteResult
        {
            FilePath = filePath,
            Timestamp = DateTime.UtcNow,
            Success = false
        };

        try
        {
            // Validate inputs
            if (string.IsNullOrWhiteSpace(filePath))
            {
                throw new ArgumentException("File path cannot be null or empty", nameof(filePath));
            }

            if (!content.CanRead)
            {
                throw new InvalidOperationException("No content to write to file.");
            }

            // Check if file exists and handle accordingly
            var fileExists = File.Exists(filePath);
            if (fileExists && !options.Overwrite)
            {
                throw new InvalidOperationException("File already exists.");
            }

            // Create directory if it doesn't exist
            var directory = Path.GetDirectoryName(filePath);
            if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
                result.DirectoryCreated = true;
            }

            // Create backup if requested
            if (options.CreateBackup && fileExists)
            {
                var backupPath = $"{filePath}.backup.{DateTime.Now:yyyyMMdd_HHmmss}";
                File.Copy(filePath, backupPath);
                result.BackupPath = backupPath;
            }

            // Write the file
            await File.WriteAllBytesAsync(filePath, content.Data!.Value.ToArray());

            result.Success = true;
            result.BytesWritten = content.Data!.Value.Length;

            // Log to AGI system if enabled
            if (options.LogToAGI)
            {
                await LogToAGISystemAsync(filePath, "file_write", result);
            }

            return result;
        }
        catch (Exception ex)
        {
            result.Error = ex.Message;
            result.Exception = ex;

            // Log error to AGI system if enabled
            if (options.LogToAGI)
            {
                await LogToAGISystemAsync(filePath, "file_write_error", result);
            }

            if (options.ThrowOnError)
            {
                throw;
            }

            return result;
        }
    }

    /// <summary>
    /// Logs file operations to the AGI system for autonomous learning and optimization.
    /// </summary>
    private static async Task LogToAGISystemAsync(string filePath, string operation, FileWriteResult result)
    {
        try
        {
            // In a real implementation, this would integrate with the AGI logging system
            var logEntry = new
            {
                timestamp = DateTime.UtcNow,
                operation = operation,
                filePath = filePath,
                success = result.Success,
                bytesWritten = result.BytesWritten,
                error = result.Error,
                metadata = new
                {
                    backupCreated = !string.IsNullOrEmpty(result.BackupPath),
                    directoryCreated = result.DirectoryCreated
                }
            };

            // This would be replaced with actual AGI system integration
            var logPath = Path.Combine(Path.GetTempPath(), "agi_file_operations.log");
            var logJson = System.Text.Json.JsonSerializer.Serialize(logEntry);
            await File.AppendAllTextAsync(logPath, logJson + Environment.NewLine);
        }
        catch
        {
            // Silently fail AGI logging to not interfere with main operation
        }
    }
}

/// <summary>
/// Options for AGI-enhanced file writing operations.
/// </summary>
public class AGIFileWriteOptions
{
    /// <summary>
    /// Whether to overwrite existing files.
    /// </summary>
    public bool Overwrite { get; set; } = false;

    /// <summary>
    /// Whether to create a backup before overwriting.
    /// </summary>
    public bool CreateBackup { get; set; } = true;

    /// <summary>
    /// Whether to log operations to the AGI system.
    /// </summary>
    public bool LogToAGI { get; set; } = true;

    /// <summary>
    /// Whether to throw exceptions on errors or return them in the result.
    /// </summary>
    public bool ThrowOnError { get; set; } = true;
}

/// <summary>
/// Result of an AGI-enhanced file write operation.
/// </summary>
public class FileWriteResult
{
    /// <summary>
    /// The path to the file that was written.
    /// </summary>
    public string FilePath { get; set; } = string.Empty;

    /// <summary>
    /// Whether the operation was successful.
    /// </summary>
    public bool Success { get; set; }

    /// <summary>
    /// Number of bytes written to the file.
    /// </summary>
    public int BytesWritten { get; set; }

    /// <summary>
    /// Timestamp of the operation.
    /// </summary>
    public DateTime Timestamp { get; set; }

    /// <summary>
    /// Path to the backup file if one was created.
    /// </summary>
    public string? BackupPath { get; set; }

    /// <summary>
    /// Whether a directory was created for the file.
    /// </summary>
    public bool DirectoryCreated { get; set; }

    /// <summary>
    /// Error message if the operation failed.
    /// </summary>
    public string? Error { get; set; }

    /// <summary>
    /// Exception that occurred if the operation failed.
    /// </summary>
    public Exception? Exception { get; set; }
}
