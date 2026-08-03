# ADR 002: Django on Backend

## Status

Accepted

## Context

Backend features like a dashboard, or an LLM integration that requires communication with an API, need a framework that's quick to build with. Django is exactly that, not having to build parts of the app from scratch is incredibly useful, and having ORM session handling taken care of saves plenty of time. A backend framework with many extensions also helps when a more curated solution is needed. As someone without a ton of backend experience, I preferred a Python framework that would make the backend process simpler, so I could build something I'm proud of.

## Options Considered

- Django: "Batteries-included" philosophy, provides an overall suite of built-in tools that help accelerate development and enforce security.
- FastAPI: Native asynchronous support to handle requests efficiently, plus auto-generated OpenAPI documentation directly from code. However, parts like an admin interface, Object-Relational Mapper (ORM), and authentication system need to be built separately.
- Flask: Lightweight, open-source micro-framework. Provides only the essentials, such as routing and request handling.

## Decision

I chose Django because I'm currently building toward an MVP (Minimum Viable Product) at this stage of development, and Django's built-in security, automatic admin interface, and comprehensive third-party package ecosystem support that goal directly.

## Consequences

This choice makes admin interfaces and other built-in features easier to implement. However, it does more "magic" behind the scenes, which makes it harder to fully understand what's happening under the hood, since Django's ORM and auth system handle it for me instead of me building it myself in FastAPI. Although the trade-off is clear, I believe Django has more pros, strictly due to its "working out of the box" architecture.
