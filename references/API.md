# InBrief.info Feed API Reference

## Endpoint

```
GET https://inbrief.info/api/feed/
```

## Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_categories` | string | — | Comma-separated list of categories to include: `news`, `opensource`, `discussion`, `kol` |
| `exclude_categories` | string | — | Comma-separated list of categories to exclude |
| `include_sources` | string | — | Comma-separated list of sources to include |
| `exclude_sources` | string | — | Comma-separated list of sources to exclude |
| `hours` | int | 24 | Time window in hours |
| `limit` | int | 20 | Maximum number of items to return |
| `lang` | string | `en` | Response language: `en` or `zh` |

> **Note:** `include_*` takes precedence over `exclude_*` for the same dimension.

## Response Schema

```json
{
  "articles": [
    {
      "title": "Article title",
      "summary": "Short one-line summary",
      "long_summary": "Detailed multi-paragraph summary",
      "category": "news | opensource | discussion | kol",
      "source": "Source platform name (e.g. TechCrunch, Reddit, GitHub)",
      "url": "https://original-article-url.com/...",
      "published_at": "2026-04-07T12:00:00Z"
    }
  ]
}
```

## Error Responses

| Status | Meaning |
|--------|---------|
| 429 | IP rate limit exceeded (anti-spam interval or daily quota). Wait and retry. |
| 5xx | Server error. Retry after a short delay. |

### 429 Response Body

```json
{
  "detail": "Rate limit exceeded. Please wait before making another request."
}
```

## Rate Limiting

- **No API keys required.** Rate limits are applied per IP address.
- Two layers: immediate anti-spam interval and daily request quota.
- If rate-limited, the response includes a descriptive `detail` message.
