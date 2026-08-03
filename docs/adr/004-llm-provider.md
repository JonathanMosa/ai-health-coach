# ADR 004: Groq on LLM

## Status

Accepted

## Context

This app needs to be able to generate a structured workout plan, respond to free-form check-in text, and adjust plans based on feedback from the user. Preferably no long complex reasoning as to keep the cost down. Groq, used with API endpoints and more structured or predictable output, can handle this since the goal is a free model that can use API calls and is running off of the cloud.

## Options Considered

- Groq: Completely free, but rate limited to 30 requests/min, good enough for this iteration of the project, not production ready. Hosted on the cloud, therefore, no need for computing power locally.
- OpenRouter: Free tier is only 50 requests/day. The free model lineup rotates often and providers change promotions. If the app is built around one model and it gets pulled, then the app breaks.
- OpenAI: Does not have a free tier. Trial credit with new accounts, then it's pay per token. Better with complex reasoning, and OpenAI's Structured Outputs have JSON schema support that's great for predictable outputs.

## Decision

I chose Groq because it fits the project's constraints directly: free with no credit card, works through standard API calls, and supports structured/JSON output for generating workout plans and processing check-in feedback. Since the app doesn't need the greatest reasoning for templated tasks like plan generation, the trade-off in model quality is worth it for what the project needs right now.

## Consequences

This choice lets me build and run the app without any cost or local compute, while still getting real experience calling an LLM through an API. The rate limit (30 requests/min) is fine for a single-user, dev-stage project, but would become a bottleneck if this were ever opened up to multiple users at once. Groq's free models also aren't the best reasoning models, so if the project ever needs more than structured plan generation and feedback, this decision would need to be revisited in later versions.
