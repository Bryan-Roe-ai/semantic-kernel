# GitHub Copilot Instructions

This file provides guidelines for using GitHub Copilot in this repository.

## General Guidelines

- Follow the project's coding standards and best practices.
- Write clear, concise, and well-documented code.
- Ensure compatibility with Alpine Linux v3.20.
- Use available command line tools when scripting or automating tasks.

## Opening Webpages

To open a webpage in the host's default browser, use:

`"$BROWSER" <url>`

For advanced web operations:
- Use `curl -L -o output.html <url>` to download and save webpage content
- Use `wget --recursive --no-clobber --page-requisites --html-extension --convert-links <url>` to mirror entire websites
- Use `curl -s <url> | grep -oP 'pattern'` to extract specific data from web pages
- Use `curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' <url>` for API interactions
- Use `curl -I <url>` to fetch only HTTP headers for debugging
- Use `curl -w "%{http_code}" <url>` to get HTTP status codes
- Use `wget --spider <url>` to check if a URL is accessible without downloading

