#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const BASE_URL = "https://api.fathom.ai/external/v1";
const DEFAULT_SECRET_PATH = "/Users/preston/.codex/secrets/fathom.env";

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) return;
  const lines = fs.readFileSync(filePath, "utf8").split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const match = trimmed.match(/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
    if (!match) continue;
    const [, key, rawValue] = match;
    if (process.env[key]) continue;
    process.env[key] = rawValue.replace(/^['"]|['"]$/g, "");
  }
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function requireApiKey() {
  loadEnvFile(DEFAULT_SECRET_PATH);
  const key = process.env.FATHOM_API_KEY;
  if (!key) {
    throw new Error(`FATHOM_API_KEY missing; expected env var or ${DEFAULT_SECRET_PATH}`);
  }
  return key;
}

async function getJson(apiKey, endpoint, params = []) {
  const url = new URL(`${BASE_URL}${endpoint}`);
  for (const [key, value] of params) {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.append(key, value);
    }
  }
  const res = await fetch(url, { headers: { "X-Api-Key": apiKey } });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${endpoint} failed with HTTP ${res.status}: ${body.slice(0, 500)}`);
  }
  return res.json();
}

async function listMeetings(apiKey, args) {
  if (!args.start || !args.end) {
    throw new Error("meetings requires --start and --end UTC timestamps");
  }

  const baseParams = [
    ["include_summary", args.include_summary || "true"],
    ["include_action_items", args.include_action_items || "true"],
    ["created_after", args.start],
    ["created_before", args.end],
  ];
  if (args.recorded_by || args["recorded-by"]) {
    baseParams.push(["recorded_by[]", args.recorded_by || args["recorded-by"]]);
  }

  const items = [];
  let cursor = undefined;
  let pages = 0;
  const maxPages = Number(args.max_pages || args["max-pages"] || 20);

  do {
    const params = [...baseParams];
    if (cursor) params.push(["cursor", cursor]);
    const page = await getJson(apiKey, "/meetings", params);
    pages += 1;
    items.push(...(page.items || []));
    cursor = page.next_cursor || undefined;
  } while (cursor && pages < maxPages);

  const payload = {
    start: args.start,
    end: args.end,
    pages,
    count: items.length,
    items,
  };

  if (args.out) {
    fs.mkdirSync(path.dirname(args.out), { recursive: true });
    fs.writeFileSync(args.out, `${JSON.stringify(payload, null, 2)}\n`);
  }

  console.log(JSON.stringify({
    start: payload.start,
    end: payload.end,
    pages: payload.pages,
    count: payload.count,
    out: args.out || null,
    meetings: items.map((meeting) => ({
      recording_id: meeting.recording_id,
      title: meeting.meeting_title || meeting.title,
      created_at: meeting.created_at,
      recorded_by: meeting.recorded_by?.email || null,
      url: meeting.url,
    })),
  }, null, 2));
}

async function fetchTranscripts(apiKey, args) {
  if (!args.ids) throw new Error("transcripts requires --ids comma-separated recording IDs");
  const ids = args.ids.split(",").map((id) => id.trim()).filter(Boolean);
  const outDir = args["out-dir"] || args.out_dir || path.join(os.tmpdir(), "fathom-transcripts");
  fs.mkdirSync(outDir, { recursive: true });

  const results = [];
  for (let i = 0; i < ids.length; i += 3) {
    const batch = ids.slice(i, i + 3);
    const fetched = await Promise.all(batch.map(async (id) => {
      const payload = await getJson(apiKey, `/recordings/${id}/transcript`);
      const out = path.join(outDir, `transcript-${id}.json`);
      fs.writeFileSync(out, `${JSON.stringify({ recording_id: Number(id), ...payload }, null, 2)}\n`);
      return {
        recording_id: Number(id),
        out,
        turns: payload.transcript?.length || 0,
        speakers: [...new Set((payload.transcript || []).map((turn) => turn.speaker?.display_name).filter(Boolean))],
      };
    }));
    results.push(...fetched);
  }

  console.log(JSON.stringify({ out_dir: outDir, count: results.length, transcripts: results }, null, 2));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];
  const apiKey = requireApiKey();

  if (command === "meetings") {
    await listMeetings(apiKey, args);
  } else if (command === "transcripts") {
    await fetchTranscripts(apiKey, args);
  } else {
    throw new Error("Usage: fathom_api.mjs meetings --start <utc> --end <utc> [--recorded-by email] [--out file] | transcripts --ids id1,id2 [--out-dir dir]");
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
