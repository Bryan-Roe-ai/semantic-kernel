<<<<<<< HEAD
﻿// Copyright (c) Microsoft. All rights reserved.
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using System;

namespace Microsoft.SemanticKernel.Agents.AzureAI;

/// <summary>
/// Configuration and defaults associated with polling behavior for Assistant API run processing.
/// </summary>
public sealed class RunPollingOptions
{
    /// <summary>
<<<<<<< HEAD
    /// The default maximum number or retries when monitoring thread-run status.
=======
    /// Gets the default maximum number of retries when monitoring thread-run status.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    public static int DefaultMaximumRetryCount { get; } = 3;

    /// <summary>
<<<<<<< HEAD
    /// The default polling interval when monitoring thread-run status.
=======
    /// Gets the default polling interval when monitoring thread-run status.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    public static TimeSpan DefaultPollingInterval { get; } = TimeSpan.FromMilliseconds(500);

    /// <summary>
<<<<<<< HEAD
    /// The default back-off interval when  monitoring thread-run status.
=======
    /// Gets the default back-off interval when monitoring thread-run status.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    public static TimeSpan DefaultPollingBackoff { get; } = TimeSpan.FromSeconds(1);

    /// <summary>
<<<<<<< HEAD
    /// The default number of polling iterations before using <see cref="RunPollingBackoff"/>.
=======
    /// Gets the default number of polling iterations before using <see cref="RunPollingBackoff"/>.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    public static int DefaultPollingBackoffThreshold { get; } = 2;

    /// <summary>
<<<<<<< HEAD
    /// The default polling delay when retrying message retrieval due to a 404/NotFound from synchronization lag.
=======
    /// Gets the default polling delay when retrying message retrieval due to a 404/NotFound from synchronization lag.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    public static TimeSpan DefaultMessageSynchronizationDelay { get; } = TimeSpan.FromMilliseconds(500);

    /// <summary>
<<<<<<< HEAD
    /// The maximum retry count when polling thread-run status.
    /// </summary>
    /// <remarks>
    /// Only affects failures that have the potential to be transient.  Explicit server error responses
    /// will result in immediate failure.
=======
    /// Gets or sets the maximum retry count when polling thread-run status.
    /// </summary>
    /// <remarks>
    /// This value only affects failures that have the potential to be transient.
    /// Explicit server error responses will result in immediate failure.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </remarks>
    public int MaximumRetryCount { get; set; } = DefaultMaximumRetryCount;

    /// <summary>
<<<<<<< HEAD
    /// The polling interval when monitoring thread-run status.
=======
    /// Gets or sets the polling interval when monitoring thread-run status.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    public TimeSpan RunPollingInterval { get; set; } = DefaultPollingInterval;

    /// <summary>
<<<<<<< HEAD
    /// The back-off interval when  monitoring thread-run status.
=======
    /// Gets or sets the back-off interval when monitoring thread-run status.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    public TimeSpan RunPollingBackoff { get; set; } = DefaultPollingBackoff;

    /// <summary>
<<<<<<< HEAD
    /// The number of polling iterations before using <see cref="RunPollingBackoff"/>.
=======
    /// Gets or sets the number of polling iterations before using <see cref="RunPollingBackoff"/>.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    public int RunPollingBackoffThreshold { get; set; } = DefaultPollingBackoffThreshold;

    /// <summary>
<<<<<<< HEAD
    /// The polling delay when retrying message retrieval due to a 404/NotFound from synchronization lag.
=======
    /// Gets or sets the polling delay when retrying message retrieval due to a 404/NotFound from synchronization lag.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    /// </summary>
    public TimeSpan MessageSynchronizationDelay { get; set; } = DefaultMessageSynchronizationDelay;

    /// <summary>
    /// Gets the polling interval for the specified iteration count.
    /// </summary>
<<<<<<< HEAD
    /// <param name="iterationCount">The number of polling iterations already attempted</param>
=======
    /// <param name="iterationCount">The number of polling iterations already attempted.</param>
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
    public TimeSpan GetPollingInterval(int iterationCount)
    {
        return iterationCount > this.RunPollingBackoffThreshold ? this.RunPollingBackoff : this.RunPollingInterval;
    }
}
