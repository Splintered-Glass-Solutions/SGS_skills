# Stitch MCP Authentication

Use this file when configuring a Stitch MCP client or troubleshooting authentication.

## Endpoint

- Remote MCP URL: `https://stitch.googleapis.com/mcp`

## Auth Modes

### API Key

Use this when the user already has a Stitch API key and wants the simplest setup.

Required header:

```text
X-Goog-Api-Key: <YOUR_API_KEY>
```

Security rule:
- Do not hardcode a live API key into a shared repo, reusable skill, or committed config.
- Prefer local client config or a local uncommitted secret injection path.

### OAuth

Use this when the user explicitly needs Google Cloud project-backed access or when the client/workflow is using OAuth instead of API key auth.

Required headers:

```text
Authorization: Bearer <YOUR_ACCESS_TOKEN>
X-Goog-User-Project: <YOUR_PROJECT_ID>
```

Operational rule:
- OAuth access tokens are short-lived, usually about 1 hour.
- Many clients require manual token refresh and manual config update.

Token generation flow from Stitch docs:

```bash
TOKEN=$(gcloud auth application-default print-access-token)
echo "GOOGLE_CLOUD_PROJECT=$PROJECT_ID" > .env
echo "STITCH_ACCESS_TOKEN=$TOKEN" >> .env
```

## Client Snippets

### Cursor

API key:

```json
{
  "mcpServers": {
    "stitch": {
      "url": "https://stitch.googleapis.com/mcp",
      "headers": {
        "X-Goog-Api-Key": "YOUR-API-KEY"
      }
    }
  }
}
```

OAuth:

```json
{
  "mcpServers": {
    "stitch": {
      "url": "https://stitch.googleapis.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_ACCESS_TOKEN>",
        "X-Goog-User-Project": "<YOUR_PROJECT_ID>"
      }
    }
  }
}
```

### VSCode

API key:

```json
{
  "servers": {
    "stitch": {
      "url": "https://stitch.googleapis.com/mcp",
      "type": "http",
      "headers": {
        "Accept": "application/json",
        "X-Goog-Api-Key": "YOUR-API-KEY"
      }
    }
  }
}
```

OAuth:

```json
{
  "servers": {
    "stitch": {
      "url": "https://stitch.googleapis.com/mcp",
      "type": "http",
      "headers": {
        "Accept": "application/json",
        "Authorization": "Bearer <YOUR_ACCESS_TOKEN>",
        "X-Goog-User-Project": "<YOUR_PROJECT_ID>"
      }
    }
  }
}
```

### Claude Code

API key:

```bash
claude mcp add stitch --transport http https://stitch.googleapis.com/mcp --header "X-Goog-Api-Key: YOUR-API-KEY" -s user
```

OAuth:

```bash
claude mcp add stitch \
  --transport http https://stitch.googleapis.com/mcp \
  --header "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  --header "X-Goog-User-Project: <YOUR_PROJECT_ID>" \
  -s user
```

### Antigravity

API key:

```json
{
  "mcpServers": {
    "stitch": {
      "serverUrl": "https://stitch.googleapis.com/mcp",
      "headers": {
        "X-Goog-Api-Key": "YOUR-API-KEY"
      }
    }
  }
}
```

OAuth:

```json
{
  "mcpServers": {
    "stitch": {
      "serverUrl": "https://stitch.googleapis.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_ACCESS_TOKEN>",
        "X-Goog-User-Project": "<YOUR_PROJECT_ID>"
      }
    }
  }
}
```

### Gemini CLI

Install extension:

```bash
gemini extensions install https://github.com/gemini-cli-extensions/stitch
```

## Notes

- If the user says they already have an API key, prefer API-key snippets first.
- If the user says Stitch stops responding with unauthenticated errors, check whether the flow is OAuth and whether the token expired.
- If the user pasted a live key into chat, recommend rotating it after setup because the key has already been exposed in conversation history.
