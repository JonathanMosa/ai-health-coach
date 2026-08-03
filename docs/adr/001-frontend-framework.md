# ADR 001: React on Frontend

## Status

Accepted

## Context

What is the situation forcing you to make this decision?
This app requires a dynamic, interactive UI with multiple views: onboarding, dashboard, workout logs, and check-ins, that need to update without full page reloads. A component-based framework is needed to manage this complexity without duplicating code.

## Options Considered

- React: Virtual DOM to effectively update changes made to UI and component based architecture allows reusable UI to make more complex UIs.
- Angular: Faster development, it provides tools for scalability and maintenance, however, its complex tools are unnecessary for small apps.
- Vue: Component-based architecture by enabling reusable and modular UI elements, but it has fewer tools and resources when compared to React.

## Decision

What did you choose?
React was chosen due to my prior exposure. I have used react countless times in the past, especially with the CS job market, this seems like a choice that would prove useful the more I practice it. Also the speed at which I could build the front-end with React is appealing.

## Consequences

What does this choice make easier? What does it make harder?
This choice makes reusable UI possible, therefore, reducing development time (gamechanger for a single developer). React has no built-in state management for complex data, in which I'll need Context API or a library like Redux if the app grows.
