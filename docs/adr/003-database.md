# ADR 003: PostgreSQL on Backend

## Status

Accepted

## Context

The five features (coaching plan, reminders, workout logs, progress dashboard, daily check-ins) involve data that requires ACID compliance as well as relational mappings between entities. For example, a user has many workouts, and each workout has many exercises and sets/reps. PostgreSQL checks all of these boxes. I'm fairly confident I can execute well here because a relational databases class gave me a strong foundation in SQL and relational concepts through MySQL, which transfers even though PostgreSQL has some syntax differences. PostgreSQL also integrates well with Django's ORM and is well suited for structured data like user profiles and workout logs.

## Options Considered

- PostgreSQL: Scalable and reliable, heavily used in industry. Handles complex, relational data well, which fits health-related data. Integrates well with Django's ORM.
- SQLite: Better suited for development and learning, zero configuration, and lightweight. Relies on file-system permissions and has minimal built-in security features.
- MongoDB: Flexible schema with horizontal scalability. Well suited for high-volume logs, rapid prototyping, and document-based data.

## Decision

I chose PostgreSQL because it's heavily used in industry and pairs well with Django, with full support for `select_related` and `prefetch_related`. PostgreSQL is well suited for linking users to workout plans, then to daily logs, and finally to AI feedback, all through foreign keys.

## Consequences

PostgreSQL is what I want to learn most, since I'm interested in databases and their architecture, so that alone is a pro. Correctly modeling data and its relationships is also central to how the AI coaching app works. The trade-off is that PostgreSQL requires running a separate database server on my machine, unlike SQLite, which is just a file on disk. If that service isn't running, the app breaks with a connection error, a failure mode SQLite doesn't have. SQLite would simplify the development process with its lightweight, zero-configuration setup, but it locks the database file during write transactions, which would bottleneck multiple users trying to update their profiles at once.
