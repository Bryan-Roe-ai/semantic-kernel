// Copyright (c) Microsoft. All rights reserved.

public class YourAppException : Exception
{
    public YourAppException() : base()
    {
    }

    public YourAppException(string message) : base(message)
    {
    }

    public YourAppException(string message, Exception innerException) : base(message, innerException)
    {
    }
}
