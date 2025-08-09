namespace AgentCore;

/// <summary>
/// Settings controlling basic Agent echo behavior.
/// </summary>
public sealed class AgentSettings
{
    /// <summary>
    /// Format string used for echo responses. {0} = agent name, {1} = message.
    /// </summary>
    public string EchoFormat { get; init; } = "{0}: {1}"; // {name}: {message}
}

/// <summary>
/// Minimal Agent abstraction (echo implementation).
/// Extend with connectors, planners, memory, etc.
/// </summary>
public sealed class Agent
{
    /// <summary>Gets the agent name.</summary>
    public string Name { get; }

    /// <summary>Gets the immutable settings instance.</summary>
    public AgentSettings Settings { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="Agent"/> class.
    /// </summary>
    /// <param name="name">Non-empty agent name.</param>
    /// <param name="settings">Optional settings; if null a default instance is used.</param>
    /// <exception cref="ArgumentException">Thrown when name is null or whitespace.</exception>
    public Agent(string name, AgentSettings? settings = null)
    {
        if (string.IsNullOrWhiteSpace(name)) throw new ArgumentException("Name cannot be empty", nameof(name));
        Name = name;
        Settings = settings ?? new AgentSettings();
    }

    /// <summary>
    /// Echo a message using the format defined in <see cref="AgentSettings.EchoFormat"/>.
    /// </summary>
    /// <param name="message">Non-empty message string.</param>
    /// <returns>Formatted echo string.</returns>
    /// <exception cref="ArgumentException">Thrown when message is null or whitespace.</exception>
    public string SendMessage(string message)
    {
        if (string.IsNullOrWhiteSpace(message)) throw new ArgumentException("Message cannot be empty", nameof(message));
        return string.Format(Settings.EchoFormat, Name, message);
    }
}
