// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;

using System.Collections.Generic;

using System.Collections.Generic;

using System.Collections.Generic;

using System.Collections.Generic;

using System.Collections.Generic;

using System.Collections.Generic;

using System.Collections.Generic;

using System.Diagnostics.CodeAnalysis;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Services;

namespace Microsoft.SemanticKernel.TextToImage;

/// <summary>
/// Interface for text to image services
/// </summary>
[Experimental("SKEXP0001")]
public interface ITextToImageService : IAIService
{
    /// <summary>

    /// Generate an image matching the given description
    /// </summary>

    /// Given a prompt and/or an input text, the model will generate a new image.
    /// </summary>

    /// Given a prompt and/or an input text, the model will generate a new image.
    /// </summary>

    /// Given a prompt and/or an input text, the model will generate a new image.
    /// </summary>

    /// <param name="description">Image generation prompt</param>
    /// <param name="width">Image width in pixels</param>
    /// <param name="height">Image height in pixels</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Generated image in base64 format or image URL</returns>
    [Experimental("SKEXP0001")]
    public Task<string> GenerateImageAsync(
        string description,
        int width,
        int height,

    /// <param name="input">Input text for image generation</param>
    /// <param name="executionSettings">Text to image execution settings</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// Given a prompt and/or an input text, the model will generate a new image.
    /// </summary>

    /// <param name="input">Input text for image generation</param>
    /// <param name="executionSettings">Text to image execution settings</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// Given a prompt and/or an input text, the model will generate a new image.
    /// </summary>
    /// <param name="input">Input text for image generation</param>
    /// <param name="executionSettings">Text to image execution settings</param>
    /// <param name="kernel">The <see cref="Kernel"/> containing services, plugins, and other state for use throughout the operation.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>

    /// <returns>Generated image contents</returns>
    [Experimental("SKEXP0001")]
    Task<IReadOnlyList<ImageContent>> GetImageContentsAsync(
        TextContent input,
        PromptExecutionSettings? executionSettings = null,

        Kernel? kernel = null,
        CancellationToken cancellationToken = default);
}
