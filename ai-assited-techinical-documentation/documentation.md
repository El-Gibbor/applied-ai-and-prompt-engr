# TaskFlow Documentation
**Getting Started, API Reference, and Troubleshooting**
*AI-Assisted Technical Documentation Lab Submission*

---

## Contents

1. [About This Document](#about-this-document)
2. [Reference Specification Baseline](#reference-specification-baseline)
3. [Getting Started](#getting-started)
4. [API Reference](#api-reference)
5. [Troubleshooting and Frequently Asked Questions](#troubleshooting-and-frequently-asked-questions)
6. [Prompt History](#prompt-history)
7. [Reflection](#reflection)

---

## About This Document

This document is the consolidated documentation set for TaskFlow, a task management web application. It gathers material that previously existed only in developer notes, chat threads, and outdated wiki pages, and presents it in three parts: a Getting Started guide for end users, an API reference for developers, and a troubleshooting section for common problems.


---

## Reference Specification Baseline

The following baseline is the single source of truth for every example in this document. It is stated explicitly so that the API reference, the Getting Started guide, and the troubleshooting section cannot drift apart.

**Base URL:** `https://api.taskflow.app`

**Authentication:** TaskFlow uses bearer tokens. A client obtains a token from the login endpoint and then sends it on every protected request in an `Authorization` header, formatted as `Authorization: Bearer <token>`.

**Task object schema:**

| Field | Type | Notes |
|---|---|---|
| `id` | string | Server-generated, for example `t_10482` |
| `title` | string | Required on creation |
| `description` | string | Optional |
| `status` | string | One of `todo`, `in_progress`, or `done` |
| `priority` | string | One of `low`, `medium`, or `high` |
| `dueDate` | string | Date in `YYYY-MM-DD` format, optional |
| `projectId` | string | Identifier of the parent project |
| `assigneeId` | string | Identifier of the assigned user, optional |
| `createdAt` | string | Timestamp in ISO 8601 format |
| `updatedAt` | string | Timestamp in ISO 8601 format |

**Supported task endpoints:** create, read one, read many, partially update, and delete. TaskFlow does not expose a full-replacement update, so `PATCH` is used for edits and there is no `PUT`.

---

## Getting Started

This guide is written for people who simply want to use TaskFlow. No technical background is needed. It walks through creating an account, signing in, and managing your first tasks.

### Create Your Account

1. Open the TaskFlow website and select **Sign Up**.
2. Enter your name, your email address, and a password.
3. Select **Create Account**. You will be signed in straight away and taken to your dashboard.

Your password must be at least eight characters long. If the email address is already registered, TaskFlow will ask you to sign in instead.

### Sign In

1. Select **Log In** from the top of the page.
2. Enter the email address and password you registered with.
3. Select **Log In** to reach your dashboard.

If you cannot remember your password, use the **Forgot Password** link on the sign-in page and follow the emailed instructions.

### Create Your First Project

A project is simply a container that groups related tasks, for example "Marketing" or "Home Move".

1. On the dashboard, select **New Project**.
2. Give the project a name.
3. Select **Create**. The empty project opens, ready for tasks.

### Add and Manage Tasks

1. Inside a project, select **Add Task**.
2. Type a title. This is the only detail you must provide.
3. Optionally add a description, a due date, a priority of low, medium, or high, and a person to assign the task to.
4. Select **Save**.

Each task begins with the status **To Do**. To show that work has started, open the task and change its status to **In Progress**. When the task is finished, set its status to **Done**.

### Edit or Remove a Task

To change a task, open it, adjust any detail, and select **Save**. Only the fields you change are updated, so the rest of the task stays as it was. To remove a task, open it and select **Delete**. Deletion is permanent, so remove a task only when you are certain.

### A Typical First Session

A common first session looks like this. Create your account, create one project, add three or four tasks, and set a due date on the most urgent one. As you work through the day, move each task from To Do to In Progress and finally to Done. That short loop covers everything most people need on their first visit.

---

## API Reference

This reference is for developers integrating with TaskFlow. Every request and response below follows the [Reference Specification Baseline](#reference-specification-baseline).

### Overview and Authentication

All requests are made to the base URL `https://api.taskflow.app`. Request and response bodies are JSON, so send a `Content-Type: application/json` header on any request that carries a body.

Every endpoint except register and login requires authentication. First obtain a token from the login endpoint, then include it on each protected request:

```
Authorization: Bearer <token>
```

A request to a protected endpoint without a valid token returns a `401 Unauthorized` response.

### Register a New User

Creates a user account and returns an authentication token.

- **Method and path:** `POST /api/auth/register`
- **Authentication:** Not required

Request body:

```json
{
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "password": "a-strong-password"
}
```

Success response, `201 Created`:

```json
{
  "user": {
    "id": "u_88",
    "name": "Ada Lovelace",
    "email": "ada@example.com"
  },
  "token": "eyJhbGciOiJI..."
}
```

Error response, `409 Conflict`, returned when the email is already registered:

```json
{
  "error": "email_already_registered",
  "message": "An account with this email already exists."
}
```

### Log In

Exchanges valid credentials for an authentication token.

- **Method and path:** `POST /api/auth/login`
- **Authentication:** Not required

Request body:

```json
{
  "email": "ada@example.com",
  "password": "a-strong-password"
}
```

Success response, `200 OK`:

```json
{
  "user": {
    "id": "u_88",
    "name": "Ada Lovelace",
    "email": "ada@example.com"
  },
  "token": "eyJhbGciOiJI..."
}
```

Error response, `401 Unauthorized`, returned when the email or password is incorrect:

```json
{
  "error": "invalid_credentials",
  "message": "The email or password is incorrect."
}
```

### List Tasks

Returns the tasks the authenticated user can see.

- **Method and path:** `GET /api/tasks`
- **Authentication:** Required

Optional query parameters:

| Parameter | Description |
|---|---|
| `status` | Filters by `todo`, `in_progress`, or `done` |
| `projectId` | Returns only tasks within the given project |
| `page` | Selects a page of results, starting at 1 |

Example request:

```
GET /api/tasks?status=todo&projectId=p_204
Authorization: Bearer <token>
```

Success response, `200 OK`:

```json
{
  "data": [
    {
      "id": "t_10482",
      "title": "Write release notes",
      "description": "Summarise the version two changes",
      "status": "todo",
      "priority": "high",
      "dueDate": "2026-08-01",
      "projectId": "p_204",
      "assigneeId": "u_88",
      "createdAt": "2026-07-15T09:12:00Z",
      "updatedAt": "2026-07-15T09:12:00Z"
    }
  ],
  "page": 1,
  "totalPages": 1
}
```

### Create a Task

Creates a new task in a project.

- **Method and path:** `POST /api/tasks`
- **Authentication:** Required

Request body. Only `title` is required, and the remaining fields fall back to their defaults when omitted:

```json
{
  "title": "Write release notes",
  "description": "Summarise the version two changes",
  "priority": "high",
  "dueDate": "2026-08-01",
  "projectId": "p_204",
  "assigneeId": "u_88"
}
```

Success response, `201 Created`, returns the full task object, including the server-generated `id`, the default `status` of `todo`, and both timestamps.

Error response, `400 Bad Request`, returned when `title` is missing:

```json
{
  "error": "validation_error",
  "message": "The field 'title' is required."
}
```

### Retrieve a Single Task

Returns one task by its identifier.

- **Method and path:** `GET /api/tasks/{taskId}`
- **Authentication:** Required

Success response, `200 OK`, returns the task object. If no task matches the identifier, the endpoint returns `404 Not Found`:

```json
{
  "error": "not_found",
  "message": "No task exists with the given id."
}
```

### Update a Task

Applies a partial update. Send only the fields you want to change, and the others are left untouched.

- **Method and path:** `PATCH /api/tasks/{taskId}`
- **Authentication:** Required

Example request body that moves a task into progress:

```json
{
  "status": "in_progress"
}
```

Success response, `200 OK`, returns the updated task object with a refreshed `updatedAt` timestamp. An unknown identifier returns `404 Not Found`, and an invalid value, such as a `status` outside the allowed set, returns `400 Bad Request`.

### Delete a Task

Permanently removes a task.

- **Method and path:** `DELETE /api/tasks/{taskId}`
- **Authentication:** Required

A successful deletion returns `204 No Content` with an empty body. An unknown identifier returns `404 Not Found`.

### Summary of Status Codes

| Code | Meaning in TaskFlow |
|---|---|
| `200 OK` | The request succeeded and a body is returned |
| `201 Created` | A new user or task was created |
| `204 No Content` | The request succeeded and no body is returned |
| `400 Bad Request` | The request body failed validation |
| `401 Unauthorized` | The token is missing, invalid, or expired |
| `404 Not Found` | The requested resource does not exist |
| `409 Conflict` | The resource already exists, for example a duplicate email |

---

## Troubleshooting and Frequently Asked Questions

This section is divided into problems that end users are likely to meet and problems that developers are likely to meet when calling the API.

### For Users

**I cannot sign in.** Confirm that the email address is spelled correctly and that the password matches the one you registered. If you have forgotten the password, use the **Forgot Password** link on the sign-in page.

**I did not receive the password reset email.** Check the spam or junk folder first. If nothing arrives within a few minutes, request the reset again, since the earlier link expires once a new one is issued.

**My task disappeared.** A task that has been deleted cannot be recovered, because deletion is permanent. If the task is simply missing from view, check whether a status filter is active, since a filter set to To Do will hide tasks already marked Done.

**My changes were not saved.** Make sure you selected **Save** after editing. If the connection dropped while saving, reopen the task to confirm which version is stored, then apply your change again.

### For Developers

**Every protected request returns `401 Unauthorized`.** Confirm that the `Authorization` header is present and formatted as `Bearer <token>`. This status is also returned when a token has expired, in which case the client should log in again to obtain a fresh token.

**A create or update request returns `400 Bad Request`.** The body failed validation. For task creation, confirm that `title` is present. For updates, confirm that any `status` value is one of `todo`, `in_progress`, or `done`, and that any `priority` value is one of `low`, `medium`, or `high`.

**A request returns `404 Not Found`.** The identifier in the path does not match any resource. Confirm that the `taskId` is correct and that the task has not already been deleted.

**Registration returns `409 Conflict`.** An account already exists for that email address. Direct the user to the login flow rather than retrying registration.

**Requests occasionally fail under heavy use.** The API applies rate limiting and returns `429 Too Many Requests` when a client sends too many requests in a short period. Pause briefly and retry, and where possible reduce the frequency of polling.

---

## Prompt History

This log records how the documentation was produced. Each stage began with a deliberately thin prompt, whose output was then compared against the reference specification, corrected for accuracy, and rebuilt into a stronger prompt. A final chaining pass unified the tone and heading levels across all three sections.

### Stage One. First-Pass Prompts

These initial prompts carried no project context, so they were expected to produce generic templates.

```
Prompt A: Write a getting started guide for a task management web app.
Prompt B: Write an API reference for a task management app.
Prompt C: Write a troubleshooting section for a web app.
```

The output from Prompt B illustrates the problem. The model produced a plausible reference that included endpoints and fields TaskFlow does not have. It added a `PUT /api/tasks/{id}` route for full replacement, referred to a `tags` array on the task object, and described an email verification step during registration. None of these appear in the reference specification, and none were marked as assumptions.

### Stage Two. Refined Prompts With Pasted Context

The refined prompts supplied the model with the real schema and endpoint list and required a fixed structure, which is the step that removed the invented content.

```
Act as a technical writer documenting the TaskFlow API. Use only the specification below,
and do not invent endpoints, fields, or behaviours that are not listed.

Base URL: https://api.taskflow.app
Authentication: bearer token in an Authorization header.
Task object fields: id, title, description, status (todo, in_progress, done),
priority (low, medium, high), dueDate, projectId, assigneeId, createdAt, updatedAt.
Endpoints: register, login, list tasks, create task, get one task, patch task, delete task.
There is no PUT endpoint and no tags field.

For each endpoint, document the method and path, whether authentication is required, the
request body, and an example success response and an example error response. Keep the language
plain, and place each endpoint under its own level-three heading.
```

This produced a reference that matched the specification. The fabricated `PUT` route, the `tags` field, and the verification step were all absent, because the prompt named them as out of scope.

### Stage Three. Fact-Checking Pass

Each refined draft was read against the specification a second time, checking one detail at a time: every route, every field name, every status code, and every allowed value. Two further issues surfaced. The draft had described the create endpoint as returning `200 OK` rather than `201 Created`, and it had listed `dueDate` as required. Both were corrected to agree with the baseline.

### Stage Four. Chaining for a Consistent Style

With the three sections drafted and fact-checked, a final prompt used the earlier outputs as its input and standardised them.

```
Here are three drafted sections: a Getting Started guide, an API reference, and a
troubleshooting section. Rewrite all three so that they share one plain, professional tone.
Place every main section heading at level two and every subsection heading at level three.
Keep the technical content unchanged, and only adjust wording, structure, and headings.
```

This pass removed the differences in voice that came from generating the sections separately, and it aligned the heading levels across the whole document.

---

## Reflection

Writing accurate documentation turned out to be harder than writing readable documentation. On my first read of the draft API reference, the prose was confident and polished, and that confidence is exactly what made it dangerous: I found a `PUT /api/tasks/{id}` route, a `tags` array on the task object, and an email verification step during registration, none of which exist in TaskFlow. Nothing about the tone signalled uncertainty, so I would not have caught any of it by skimming. I had to go through the draft line by line against the reference specification I had written down beforehand, checking every route, every field, and every status code one at a time.

That first pass taught me something about how I needed to prompt. My earliest prompts, things like "write an API reference for a task management app," gave the model nothing to ground itself in, so it filled the gaps with the most generic shape of a task API, which is not the same as TaskFlow's actual shape. When I rewrote the prompt to paste in the exact schema, name the seven real endpoints, and state explicitly that there is no `PUT` endpoint and no `tags` field, the fabrications stopped appearing. That was the clearest lesson of the exercise for me: giving the model less room to guess mattered more than giving it better instructions on tone or structure.

Even after that correction, I still caught two smaller drift errors on a second fact-checking pass: the create endpoint was documented as returning `200 OK` instead of `201 Created`, and `dueDate` was listed as required when it is actually optional. Both are the kind of detail that reads as plausible if I was not actively cross-checking against the spec, which is why I treated fact-checking as its own separate stage rather than trusting the refined prompt to get everything right in one shot.

The last stage, chaining the three already-corrected sections through a single rewrite prompt, was the one part of the process that was about polish rather than accuracy. It fixed something I had not planned for: because I drafted the Getting Started guide, the API reference, and the troubleshooting section as three separate prompts, each one came back in a slightly different voice and used inconsistent heading levels. Feeding all three back in together and asking for one tone and one heading scheme fixed that in a single pass, which was faster than editing each section by hand.

If I did this again, I would write the reference specification baseline first and treat it as a fixed constraint from the very first prompt, rather than drafting content and reconciling it against the spec afterward. That would have prevented the entire first round of fabricated content and let me spend that time on the fact-checking pass instead.