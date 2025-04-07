using System;
using System.Net;
using System.Threading.Tasks;
using Microsoft.Azure.Functions.Worker.Http;
using Xunit;

namespace AIPlugins.AzureFunctions.Extensions.Tests
{
    public class AIPluginHelpersTests
    {
        [Fact]
        public async Task GenerateAIPluginJsonResponseAsync_ValidUrl_ReturnsOkResponse()
        {
            // Arrange
            var req = new MockHttpRequestData(new Uri("https://example.com/.well-known"));
            string skillName = "TestSkill";
            string descriptionForHuman = "Test Description for Human";
            string descriptionForModel = "Test Description for Model";

            // Act
            var response = await AIPluginHelpers.GenerateAIPluginJsonResponseAsync(req, skillName, descriptionForHuman, descriptionForModel);

            // Assert
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        }

        [Fact]
        public async Task GenerateAIPluginJsonResponseAsync_InvalidUrl_ReturnsBadRequestResponse()
        {
            // Arrange
            var req = new MockHttpRequestData(new Uri("https://invalid.com/.well-known"));
            string skillName = "TestSkill";
            string descriptionForHuman = "Test Description for Human";
            string descriptionForModel = "Test Description for Model";

            // Act
            var response = await AIPluginHelpers.GenerateAIPluginJsonResponseAsync(req, skillName, descriptionForHuman, descriptionForModel);

            // Assert
            Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        }

        [Fact]
        public void IsUrlAllowed_ValidUrl_ReturnsTrue()
        {
            // Arrange
            var url = new Uri("https://example.com");

            // Act
            var result = AIPluginHelpers.IsUrlAllowed(url);

            // Assert
            Assert.True(result);
        }

        [Fact]
        public void IsUrlAllowed_InvalidUrl_ReturnsFalse()
        {
            // Arrange
            var url = new Uri("https://invalid.com");

            // Act
            var result = AIPluginHelpers.IsUrlAllowed(url);

            // Assert
            Assert.False(result);
        }
    }

    public class MockHttpRequestData : HttpRequestData
    {
        public MockHttpRequestData(Uri url) : base(null)
        {
            Url = url;
        }

        public override Stream Body => new MemoryStream();
        public override HttpHeadersCollection Headers => new HttpHeadersCollection();
        public override IReadOnlyCollection<IHttpCookie> Cookies => new List<IHttpCookie>();
        public override Uri Url { get; }
        public override IEnumerable<ClaimsIdentity> Identities => new List<ClaimsIdentity>();
        public override string Method => "GET";
        public override HttpResponseData CreateResponse() => new MockHttpResponseData(this);
    }

    public class MockHttpResponseData : HttpResponseData
    {
        public MockHttpResponseData(HttpRequestData request) : base(request)
        {
        }

        public override HttpHeadersCollection Headers => new HttpHeadersCollection();
        public override HttpStatusCode StatusCode { get; set; }
        public override Stream Body { get; set; } = new MemoryStream();
        public override HttpCookies Cookies => new HttpCookies();
    }
}
