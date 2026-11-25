# One chat photo

Discover the live tools and schemas first; these names grant no access. Follow the [photo workflow](../SKILL.md#send-one-photo-with-words), including its one complete review and next-message yes. No direct or custom-group photos, photo-only messages or raw media URLs.

| Operation ID | Inputs besides `catalogVersion: 1` | Result and meaning |
| --- | --- | --- |
| `chat-upload-start` | `body: { kind, channelId, fileName, contentType, size }`; kind `team` or `staff`, channel ID 1–128 characters, trimmed filename 1–255, MIME `image/jpeg` or `image/png`, positive whole-byte size at most 5,242,880 | `{ uploadId, uploadUrl, expiresAt }`; one current Team/Staff chat where the caller is team staff. `expiresAt` is the five-minute send deadline. The single-object no-overwrite Storage address lasts two hours; never log or retain it in conversation history |
| `request-key-new` | Input `{}`, no catalog version | One UUID; use unchanged as this intended send's `messageId` |
| `chat-message-send` | `body: { kind, channelId, messageId, text, uploadId }`; same Team/Staff chat, original message UUID, trimmed nonblank text at most 5,000 characters, the returned upload ID | `{ outcome: "published" | "unknown", messageId }`; published means sent, not read or device delivery. Unknown or lost answers stop writes; no automatic resend, replacement key or history scan |

The bundled uploader reads the start response JSON through private stdin or a host-private file, uses only `uploadUrl` as the PUT destination and checks `expiresAt` before starting. It reads one chosen local JPEG/PNG, refuses over 5 MiB or 2048 px on either edge, and sends its exact bytes once with the detected `Content-Type` and `x-upsert: false`. It accepts only Hype's HTTPS staging Storage path; no redirects, proxies or retries. It prints only `uploaded` (exit 0), `refused: <short reason>` (exit 1), or `unknown` (exit 2), never the response, address or remote error body. Header checks are not full decoding or orientation checks: save the photo upright first; Hype validates it again before publication. Uploading alone sends no message.

Do not store the signed address in a progress record. Keep the original message key, upload ID and exact approved binding for a deliberately requested recovery; a consumed receipt remains bound to that same message even after failure. Never repeat a confirmed publication. A fresh attempt after a definite refusal or expiry needs another complete review and next-message yes, not an automatic repair.
