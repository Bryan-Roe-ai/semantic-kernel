// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;

namespace Microsoft.SemanticKernel.Plugins.Grpc.Model;

/// <summary>
/// The gRPC operation.
/// </summary>
internal sealed class GrpcOperation
{
    /// <summary>
    /// Name of 'address' argument used as override for the address provided by gRPC operation.
    /// </summary>
    internal const string AddressArgumentName = "address";

    /// <summary>
    /// Name of 'payload' argument that represents gRPC operation request message.
    /// </summary>
    internal const string PayloadArgumentName = "payload";

    /// <summary>
    /// Creates an instance of a <see cref="GrpcOperation"/> class.
    /// <param name="serviceName">The service name.</param>
    /// <param name="name">The operation name.</param>
    /// <param name="request">The operation request type metadata.</param>
    /// <param name="response">The operation response type metadata.</param>
    /// </summary>
    public GrpcOperation(
        string serviceName,
        string name,
        GrpcOperationDataContractType request,
        GrpcOperationDataContractType response)
    {
        this.ServiceName = serviceName;
        this.Name = name;
        this.Request = request;
        this.Response = response;
    }

    /// <summary>
    /// The service name.
    /// </summary>
    public string ServiceName { get; set; }

    /// <summary>
    /// The operation name.
    /// </summary>
    public string Name { get; private set; }

    /// <summary>
    /// The full service name that includes that 'package' specifier as prefix.
    /// </summary>
    public string FullServiceName
    {
        get
        {
            if (string.IsNullOrEmpty(this.Package))
            {
                return this.ServiceName;
            }

            return $"{this.Package}.{this.ServiceName}";
        }
    }

    /// <summary>
    /// The gRPC request data contract.
    /// </summary>
    public GrpcOperationDataContractType Request { get; private set; }

    /// <summary>
    /// The gRPC response data contract.
    /// </summary>
    public GrpcOperationDataContractType Response { get; private set; }

    /// <summary>
    /// The address.
    /// </summary>
    public string? Address { get; set; }

    /// <summary>
    /// Specifier to prevent name clashes between types.
    /// </summary>
    public string? Package { get; set; }

    /// <summary>
    /// Returns list of gRPC operation parameters.
    /// </summary>
    /// <returns>The list of parameters.</returns>
    internal static List<KernelParameterMetadata> CreateParameters() =>
    [
        // Register the "address" parameter so that it's possible to override it if needed.
        new(GrpcOperation.AddressArgumentName)
        {
            Description = "Address for gRPC channel to use.",
        },

        // Register the "payload" parameter to be used as gRPC operation request message.
        new(GrpcOperation.PayloadArgumentName)
        {
            Description = "gRPC request message.",
        },
    ];
}
