open System
open Microsoft.AspNetCore.Builder
open Microsoft.Extensions.Hosting
open Microsoft.Extensions.Logging
open Microsoft.Extensions.DependencyInjection

[<EntryPoint>]
let main args =
    try
        let builder = WebApplication.CreateBuilder(args)
        
        // Add basic services
        builder.Services.AddLogging() |> ignore
        builder.Services.AddRouting() |> ignore
        
        let app = builder.Build()
        
        // Configure middleware pipeline
        app.UseRouting() |> ignore
        app.UseHttpsRedirection() |> ignore
        
        // Add minimal endpoint
        app.MapGet("/", Func<string>(fun () -> "Hello World!")) |> ignore
        
        // Run the application
        app.Run()
        
        0 // Success exit code
    with
    | ex ->
        printfn "Application failed to start: %s" ex.Message
        1 // Error exit code

