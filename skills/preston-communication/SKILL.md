---
name: preston-communication
description: Draft, revise, or prepare messages in Preston's communication style. Use whenever the user asks Codex to send, draft, reply to, write, or respond to a text message, iMessage, SMS, email, Gmail thread, client message, vendor support email, family message, wife message, close-friend message, business-partner text, or any outbound personal/professional communication as Preston.
---

# Preston Communication

Use this skill to write outbound messages as Preston. Always choose the channel first, then load the matching reference only as needed.

## Channel Choice

- For email, Gmail, proposals, clients, vendors, support tickets, formal business updates, accounting/admin threads, or messages that document decisions: read `references/email-style-guide.md`.
- For text, iMessage, SMS, Messages, wife/family, close friends, group chats, rapid coordination, founder/operator backchannels, or short mobile replies: read `references/text-message-style-guide.md`.
- If the user says "message" without a channel, infer from context. If unclear and sending would be risky, ask one concise clarifying question; otherwise draft a safe version and label the assumed channel.

## Workflow

1. Identify recipient, channel, purpose, and relationship category.
2. Read the relevant style guide reference before drafting.
3. Match the current thread's tone and cadence when thread context is available.
4. Draft in Preston's voice, not a generic assistant voice.
5. For sensitive or high-risk topics, provide a draft for review rather than sending.
6. Do not send through Gmail/Messages unless the user explicitly asks to send and the applicable safety rule permits it.
7. Before sending any proposal, contract, payment, booking, or other business-critical link, verify the exact live URL that will be sent.

## Text Defaults

For texts, prefer short, mobile-first replies. Use no greeting/signoff unless the thread needs it. Tapback-style acknowledgements, fragments, quick logistics, and relationship-specific shorthand are often correct. Wife/family messages should be intimate and practical, not email-like.

## Messages/iMessage Sending

- When sending through macOS Messages/iMessage, do not type or paste a multi-line message directly into the message field with automation. Messages may treat line breaks as separate sends.
- Convert the draft into one paste-safe message before sending. Prefer short sentences separated by spaces or semicolons instead of bullet lists or paragraph breaks.
- If the content needs structure, either send one concise summary text or explicitly ask before splitting it into multiple messages.
- Before the final send, verify the compose field contains exactly one unsent message. Do not press Enter/Return or use an input method that can submit line-by-line.
- If using Computer Use, avoid `type_text` for multi-line SMS/iMessage bodies. Use a single-line body or a clipboard/paste approach that has been verified not to send line breaks as separate messages.

## Email Defaults

For emails, prefer warm, structured, practical replies. Use greetings and signoffs when appropriate. Lead with acknowledgement/status, include useful context, and end with a concrete next step.

## Link Verification

- Proposal links are business-critical. Before texting, emailing, or otherwise sending a proposal link, verify the exact URL in the message is live.
- Do not rely on a local build, a remembered deployment, or a nearby route. Check the production URL that the recipient will receive.
- The check must confirm HTTP `200` after redirects and page content that uniquely identifies the intended proposal, such as the client name or proposal title.
- If the URL is dead, redirects to the wrong page, or lacks the expected proposal-specific content, do not send the message. Fix or deploy first, then recheck.
- In the final response after sending, mention that the link was verified when applicable.

Example:

```bash
node - <<'NODE'
const url = 'https://proposals.splinteredglass.solutions/proposals/<slug>';
const expected = '<client name or proposal title>';
const res = await fetch(url, { redirect: 'follow' });
const text = await res.text();
if (res.status !== 200 || !text.includes(expected)) {
  console.error({ status: res.status, finalUrl: res.url, hasExpectedContent: text.includes(expected) });
  process.exit(1);
}
console.log({ status: res.status, finalUrl: res.url, hasExpectedContent: true });
NODE
```

## Safety

Draft for review before sending when the message involves:

- Wife/family conflict, parenting tension, health, family plans, or emotionally loaded topics.
- Money, contracts, legal risk, taxes, payroll, debt, or scope commitments.
- Customer data, credentials, private URLs, attachments, or sensitive business details.
- Any relationship where tone uncertainty could create damage.

When safe to proceed, still keep the final message concise and channel-appropriate.
