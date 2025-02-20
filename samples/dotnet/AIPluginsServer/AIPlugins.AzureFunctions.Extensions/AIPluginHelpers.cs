﻿// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Net;
using System.Threading.Tasks;
using Microsoft.Azure.Functions.Worker.Http;

namespace AIPlugins.AzureFunctions.Extensions;

public static class AIPluginHelpers
{
    private static readonly string[] AllowedDomains = { "example.com", "anotherexample.com" };

    public static async Task<HttpResponseData> GenerateAIPluginJsonResponseAsync(HttpRequestData req, string skillName, string descriptionForHuman, string descriptionForModel)
    {
        string skillUri = req.Url.GetLeftPart(UriPartial.Path);
        skillUri = skillUri.Remove(skillUri.IndexOf($".well-known", StringComparison.InvariantCultureIgnoreCase));
        Uri openApiSpecUri = new(baseUri: new(skillUri), $"openapi/v3.json");

        if (!IsUrlAllowed(openApiSpecUri))
        {
            var response = req.CreateResponse(HttpStatusCode.BadRequest);
            await response.WriteStringAsync("The URL is not allowed.");
            return response;
        }

        AIPluginModel aiPluginModel = new()
        {
            SchemaVersion = "v1",
            NameForModel = skillName,
            NameForHuman = skillName,
            DescriptionForModel = descriptionForModel,
            DescriptionForHuman = descriptionForHuman,
            Api = new()
            {
                Type = "openapi",
                Url = openApiSpecUri.ToString(),
                HasUserAuthentication = false
            },
            Auth = new AIPluginModel.AuthModel
            {
                Type = "none"
            },
            LogoUrl = skillUri + "logo.png",
            ContactEmail = "donnald_oconnor@outlook.com",
            LegalInfoUrl = skillUri + "legal"
        };

        var response = req.CreateResponse(HttpStatusCode.OK);
        await response.WriteAsJsonAsync(aiPluginModel);
        return response;
    }

    private static bool IsUrlAllowed(Uri url)
    {
        foreach (var domain in AllowedDomains)
        {
            if (url.Host.EndsWith(domain, StringComparison.InvariantCultureIgnoreCase))
            {
                return true;
            }
        }
        return false;
    }
}
