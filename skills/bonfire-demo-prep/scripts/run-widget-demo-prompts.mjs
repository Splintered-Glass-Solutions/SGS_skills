#!/usr/bin/env node

import { readFile, writeFile } from "node:fs/promises";
import { randomUUID } from "node:crypto";

function usage() {
	console.log(`Usage:
  node run-widget-demo-prompts.mjs --suite prompts.json [--base-url URL] [--widget-id ID] [--out results.json]

Suite format:
{
  "baseUrl": "https://dev.heybonfire.com",
  "widgetId": "widget-uuid",
  "pageUrl": "https://dev.heybonfire.com/demo-check",
  "pageTitle": "Demo check",
  "metadata": { "source": "codex-demo-qa" },
  "prompts": [
    {
      "key": "identity",
      "prompt": "Who are you?",
      "mustInclude": ["TruCenter"],
      "mustMatch": ["source-backed"],
      "minSources": 1,
      "minChars": 80,
      "maxChars": 1500
    }
  ]
}`);
}

function parseArgs(argv) {
	const args = {};
	for (let i = 2; i < argv.length; i += 1) {
		const arg = argv[i];
		if (arg === "--help" || arg === "-h") {
			args.help = true;
			continue;
		}
		if (!arg.startsWith("--")) {
			throw new Error(`Unexpected positional argument: ${arg}`);
		}
		const key = arg.slice(2).replace(/-([a-z])/g, (_, char) =>
			char.toUpperCase(),
		);
		const value = argv[i + 1];
		if (!value || value.startsWith("--")) {
			throw new Error(`Missing value for ${arg}`);
		}
		args[key] = value;
		i += 1;
	}
	return args;
}

async function readJson(path) {
	return JSON.parse(await readFile(path, "utf8"));
}

function normalizeBaseUrl(value) {
	const baseUrl = String(value || "").trim().replace(/\/+$/, "");
	if (!baseUrl) {
		throw new Error("Missing baseUrl. Set suite.baseUrl or --base-url.");
	}
	return baseUrl;
}

function getText(body) {
	return (
		body?.message?.content ||
		body?.data?.message?.content ||
		body?.response ||
		body?.data?.response ||
		body?.content ||
		""
	);
}

function getSources(body) {
	const sources =
		body?.sources ||
		body?.data?.sources ||
		body?.message?.sources ||
		body?.data?.message?.sources ||
		[];
	return Array.isArray(sources) ? sources : [];
}

async function postJson({ baseUrl, path, body, token }) {
	const headers = {
		"content-type": "application/json",
		"Idempotency-Key": randomUUID(),
		origin: baseUrl,
	};
	if (token) {
		headers.authorization = `Bearer ${token}`;
		headers["x-bonfire-widget-auth-mode"] = "widget-token";
	}

	const response = await fetch(`${baseUrl}${path}`, {
		method: "POST",
		headers,
		body: JSON.stringify(body),
	});
	const text = await response.text();
	let json;
	try {
		json = JSON.parse(text);
	} catch {
		json = { raw: text };
	}
	if (!response.ok) {
		throw new Error(`${path} ${response.status}: ${text.slice(0, 500)}`);
	}
	return json;
}

function scorePrompt(item, body) {
	const text = getText(body);
	const sources = getSources(body);
	const lowerText = text.toLowerCase();
	const missingInclude = (item.mustInclude || []).filter(
		(term) => !lowerText.includes(String(term).toLowerCase()),
	);
	const missingMatch = (item.mustMatch || []).filter((pattern) => {
		const regex = new RegExp(pattern, item.matchFlags || "i");
		return !regex.test(text);
	});
	const minChars = Number.isFinite(item.minChars) ? item.minChars : 80;
	const maxChars = Number.isFinite(item.maxChars) ? item.maxChars : Infinity;
	const minSources = Number.isFinite(item.minSources) ? item.minSources : 1;
	const failures = [];

	if (text.length < minChars) failures.push(`too_short:${text.length}`);
	if (text.length > maxChars) failures.push(`too_long:${text.length}`);
	if (sources.length < minSources) failures.push(`sources:${sources.length}`);
	for (const term of missingInclude) failures.push(`missing:${term}`);
	for (const pattern of missingMatch) failures.push(`missing_regex:${pattern}`);

	return {
		key: item.key,
		pass: failures.length === 0,
		failures,
		chars: text.length,
		sources: sources.length,
		preview: text.replace(/\s+/g, " ").slice(0, 240),
	};
}

async function run() {
	const args = parseArgs(process.argv);
	if (args.help) {
		usage();
		return;
	}
	if (!args.suite) {
		throw new Error("Missing --suite prompts.json");
	}

	const suite = await readJson(args.suite);
	const baseUrl = normalizeBaseUrl(args.baseUrl || suite.baseUrl);
	const widgetId = String(args.widgetId || suite.widgetId || "").trim();
	if (!widgetId) {
		throw new Error("Missing widgetId. Set suite.widgetId or --widget-id.");
	}
	if (!Array.isArray(suite.prompts) || suite.prompts.length === 0) {
		throw new Error("Suite must include a non-empty prompts array.");
	}

	const anonVisitorId = `codex-demo-${Date.now()}`;
	const pageUrl = suite.pageUrl || `${baseUrl}/codex-demo-check`;
	const pageTitle = suite.pageTitle || "Codex demo check";
	const bootstrap = await postJson({
		baseUrl,
		path: "/api/chat/bootstrap",
		body: {
			widget_id: widgetId,
			anon_visitor_id: anonVisitorId,
			page_url: pageUrl,
			page_title: pageTitle,
			domain_pulse: false,
		},
	});
	const bootstrapData = bootstrap.data || bootstrap;
	const token = bootstrapData.widget_token;
	const orgId = bootstrapData.org_id;
	const aiId = bootstrapData.ai_id;
	if (!token || !orgId || !aiId) {
		throw new Error(
			`Bootstrap missing token/org/ai: ${JSON.stringify(bootstrapData)}`,
		);
	}

	const start = await postJson({
		baseUrl,
		path: "/api/chat/start-session",
		token,
		body: {
			org_id: orgId,
			ai_id: aiId,
			metadata: {
				...(suite.metadata || {}),
				page_url: pageUrl,
				source: suite.metadata?.source || "codex-demo-qa",
			},
		},
	});
	const sessionId =
		start?.data?.session_id || start?.session_id || start?.data?.session?.session_id;
	if (!sessionId) {
		throw new Error(`Start session response missing session id.`);
	}

	const results = [];
	for (const item of suite.prompts) {
		const body = await postJson({
			baseUrl,
			path: "/api/chat/message",
			token,
			body: {
				org_id: orgId,
				ai_id: aiId,
				session_id: sessionId,
				input: { role: "user", content: item.prompt },
				stream: false,
			},
		});
		results.push(scorePrompt(item, body));
	}

	const output = {
		checkedAt: new Date().toISOString(),
		baseUrl,
		widgetId,
		orgId,
		aiId,
		sessionId,
		pass: results.every((result) => result.pass),
		results,
	};

	const rendered = JSON.stringify(output, null, 2);
	if (args.out) {
		await writeFile(args.out, `${rendered}\n`);
	}
	console.log(rendered);
	if (!output.pass) {
		process.exitCode = 1;
	}
}

run().catch((error) => {
	console.error(error instanceof Error ? error.message : String(error));
	process.exit(1);
});
