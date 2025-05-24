// Copyright (c) Microsoft. All rights reserved.

using System;

namespace Microsoft.SemanticKernel;

/// <summary>
/// Represents the base exception from which all Semantic Kernel exceptions derive.
/// </summary>
/// <remarks>
/// Instances of this class optionally contain telemetry information in the Exception.Data property using keys that are consistent with the OpenTelemetry standard.
/// See https://opentelemetry.io/ for more information.
/// </remarks>
public class KernelException : Exception
{
    /// <summary>
    /// Initializes a new instance of the <see cref="KernelException"/> class.
    /// </summary>
    public KernelException()
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelException"/> class with a specified error message.
    /// </summary>
    /// <param name="message">The error message that explains the reason for the exception.</param>
    public KernelException(string? message) : base(message)
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelException"/> class with a specified error message and a reference to the inner exception that is the cause of this exception.
    /// </summary>
    /// <param name="message">The error message that explains the reason for the exception.</param>
    /// <param name="innerException">The exception that is the cause of the current exception, or a null reference if no inner exception is specified.</param>
    public KernelException(string? message, Exception? innerException) : base(message, innerException)
    {
    }
}

/// <summary>
/// Represents an exception that occurs when a function invocation is canceled.
/// </summary>
public class KernelFunctionCanceledException : KernelException
{
    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionCanceledException"/> class.
    /// </summary>
    public KernelFunctionCanceledException()
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionCanceledException"/> class with a specified error message.
    /// </summary>
    /// <param name="message">The error message that explains the reason for the exception.</param>
    public KernelFunctionCanceledException(string? message) : base(message)
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionCanceledException"/> class with a specified error message and a reference to the inner exception that is the cause of this exception.
    /// </summary>
    /// <param name="message">The error message that explains the reason for the exception.</param>
    /// <param name="innerException">The exception that is the cause of the current exception, or a null reference if no inner exception is specified.</param>
    public KernelFunctionCanceledException(string? message, Exception? innerException) : base(message, innerException)
    {
    }
}

/// <summary>
/// Represents an exception that occurs when a function invocation fails.
/// </summary>
public class KernelFunctionInvocationException : KernelException
{
    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionInvocationException"/> class.
    /// </summary>
    public KernelFunctionInvocationException()
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionInvocationException"/> class with a specified error message.
    /// </summary>
    /// <param name="message">The error message that explains the reason for the exception.</param>
    public KernelFunctionInvocationException(string? message) : base(message)
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionInvocationException"/> class with a specified error message and a reference to the inner exception that is the cause of this exception.
    /// </summary>
    /// <param name="message">The error message that explains the reason for the exception.</param>
    /// <param name="innerException">The exception that is the cause of the current exception, or a null reference if no inner exception is specified.</param>
    public KernelFunctionInvocationException(string? message, Exception? innerException) : base(message, innerException)
    {
    }
}

/// <summary>
/// Represents an exception that occurs when a function invocation times out.
/// </summary>
public class KernelFunctionTimeoutException : KernelException
{
    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionTimeoutException"/> class.
    /// </summary>
    public KernelFunctionTimeoutException()
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionTimeoutException"/> class with a specified error message.
    /// </summary>
    /// <param name="message">The error message that explains the reason for the exception.</param>
    public KernelFunctionTimeoutException(string? message) : base(message)
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionTimeoutException"/> class with a specified error message and a reference to the inner exception that is the cause of this exception.
    /// </summary>
    /// <param name="message">The error message that explains the reason for the exception.</param>
    /// <param name="innerException">The exception that is the cause of the current exception, or a null reference if no inner exception is specified.</param>
    public KernelFunctionTimeoutException(string? message, Exception? innerException) : base(message, innerException)
    {
    }
}

/// <summary>
/// Represents an exception that occurs when a function invocation is unauthorized.
/// </summary>
public class KernelFunctionUnauthorizedException : KernelException
{
    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionUnauthorizedException"/> class.
    /// </summary>
    public KernelFunctionUnauthorizedException()
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionUnauthorizedException"/> class with a specified error message.
    /// </summary>
    /// <param name="message">The error message that explains the reason for the exception.</param>
    public KernelFunctionUnauthorizedException(string? message) : base(message)
    {
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="KernelFunctionUnauthorizedException"/> class with a specified error message and a reference to the inner exception that is the cause of this exception.
    /// </summary>
    /// <param name="message">The error message that explains the reason for the exception.</param>
    /// <param name="innerException">The exception that is the cause of the current exception, or a null reference if no inner exception is specified.</param>
    public KernelFunctionUnauthorizedException(string? message, Exception? innerException) : base(message, innerException)
    {
    }
}
