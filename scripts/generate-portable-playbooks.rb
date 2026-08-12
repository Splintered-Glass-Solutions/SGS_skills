#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"
require "yaml"

ROOT = File.expand_path("..", __dir__)
SKILLS_DIR = File.join(ROOT, "skills")
OUT_DIR = File.join(ROOT, "portable-agent-playbooks")

REPLACEMENTS = [
  ["/Users/preston/.codex/skills", "<agent-config>/skills"],
  ["/Users/preston/.codex/commands", "<agent-config>/commands"],
  ["/Users/preston/.codex/portfolio", "<agent-config>/portfolio"],
  ["/Users/preston/.codex", "<agent-config>"],
  ["/Users/preston/Code", "<workspace>"],
  ["Preston", "the user"],
  ["preston", "the user"],
  ["Codex skills", "agent skills"],
  ["Codex skill", "agent skill"],
  ["Codex commands", "agent commands"],
  ["Codex command", "agent command"],
  ["Codex work", "agent work"],
  ["Codex Desktop", "the agent runtime"],
  ["Codex thread", "agent thread"],
  ["Codex threads", "agent threads"],
  ["Codex", "the agent"],
  ["codex", "agent"]
].freeze

def slug_title(slug)
  title = slug.split("-").map { |part| part == "pm" ? "PM" : part.capitalize }.join(" ")
  title
    .gsub(/^Codex\b/, "Agent")
    .gsub(/^Preston\b/, "User")
end

def load_skill(path)
  text = File.read(path)
  parts = text.split("---", 3)
  frontmatter = parts.length >= 3 ? parts[1] : ""
  body = parts.length >= 3 ? parts[2] : text
  data = YAML.safe_load(frontmatter)
  [data, body.sub(/\A\s+/, "")]
rescue Psych::SyntaxError
  name = frontmatter[/^name:\s*["']?([a-z0-9-]+)["']?/, 1] || File.basename(File.dirname(path))
  desc = frontmatter[/^description:\s*["']?(.+?)["']?\s*$/, 1] || "Portable agent playbook."
  [{ "name" => name, "description" => desc }, body.sub(/\A\s+/, "")]
end

def portable_text(text)
  REPLACEMENTS.reduce(text) do |memo, (from, to)|
    memo.gsub(from, to)
  end
end

def write_file(path, content)
  FileUtils.mkdir_p(File.dirname(path))
  File.write(path, content)
end

def write_binary_file(path, content)
  FileUtils.mkdir_p(File.dirname(path))
  File.binwrite(path, content)
end

FileUtils.rm_rf(OUT_DIR)
FileUtils.mkdir_p(OUT_DIR)
FileUtils.mkdir_p(File.join(OUT_DIR, "playbooks"))
FileUtils.mkdir_p(File.join(OUT_DIR, "adapters"))

skills = Dir[File.join(SKILLS_DIR, "*", "SKILL.md")].sort.map do |path|
  data, body = load_skill(path)
  name = data.fetch("name")
  description = portable_text(data["description"].to_s.strip.gsub(/\s+/, " "))
  title = slug_title(name)
  playbook_dir = File.join(OUT_DIR, "playbooks", name)
  portable_body = portable_text(body).strip

  agent_body = <<~MARKDOWN
    # #{title} Agent Playbook

    This is a platform-neutral version of the `#{name}` skill. It is designed
    for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
    platform that supports reusable instructions.

    ## Trigger

    #{description}

    ## Portability Notes

    - Replace `<agent-config>` with the local configuration folder for the
      target agent platform.
    - Replace `<workspace>` with the user's active project/workspace root.
    - Treat slash commands and `$skill-name` references as invocation hints.
      If the target platform does not support slash commands, paste this
      playbook into the agent's custom instructions or project memory.
    - Keep all original safety gates. Do not send messages, deploy, mutate
      production data, change permissions, or perform irreversible actions
      without explicit approval from the user.
    - If a referenced connector or tool is not available in the target platform,
      stop and report the missing capability instead of simulating external
      actions.

    ## Instructions

    #{portable_body}
  MARKDOWN

  manifest = {
    "name" => name,
    "display_name" => title,
    "description" => description,
    "source" => "skills/#{name}/SKILL.md",
    "entrypoint" => "AGENT.md",
    "target_platforms" => ["claude", "claude-code", "cursor", "openai-agents", "generic-agent"],
    "safety_level" => "approval-gated for external or irreversible actions"
  }

  write_file(File.join(playbook_dir, "AGENT.md"), agent_body)
  write_file(File.join(playbook_dir, "manifest.yaml"), manifest.to_yaml)

  source_root = File.dirname(path)
  Dir[File.join(source_root, "**", "*")].sort.each do |source_file|
    next unless File.file?(source_file)

    relative = source_file.delete_prefix("#{source_root}/")
    next if relative == "SKILL.md" || relative.start_with?("agents/")

    destination = File.join(playbook_dir, relative)
    if relative.match?(/\.(md|markdown|txt|yaml|yml|json|sh|bash|rb|py|js|mjs|ts|tsx|toml)\z/i)
      text = File.read(source_file).gsub("\r\n", "\n")
      write_file(destination, portable_text(text))
    else
      write_binary_file(destination, File.binread(source_file))
    end
  end

  { "name" => name, "display_name" => title, "description" => description }
end

index = <<~MARKDOWN
  # Portable Agent Playbooks

  These are generalized, platform-neutral versions of the SGS custom agent
  skills. They are meant to be usable in Claude, Claude Code, Cursor,
  OpenAI agents, or other agent platforms.

  Start with the [SGS resource library](../README.md) or the [AI Best
  Practices package](../packages/ai-best-practices/README.md). For AI
  implementation guidance, visit [Splintered Glass Solutions](https://splinteredglass.solutions/)
  or [start a conversation](https://splinteredglass.solutions/contact).

  This generated directory contains generalized workflows only. Do not add
  customer data, credentials, private project state, or environment-specific
  operating instructions.

  ## How To Use

  1. Pick a playbook under `playbooks/<name>/AGENT.md`.
  2. Paste it into the target platform's project instructions, custom
     instructions, or agent memory.
  3. Replace placeholders:
     - `<agent-config>`: local agent config folder.
     - `<workspace>`: active project or repo root.
  4. Confirm which tools/connectors are available.
  5. Keep approval gates intact for deploys, sends, production mutation,
     permission changes, billing, protected branches, and destructive cleanup.

  ## Adapters

  - [Claude / Claude Code](adapters/claude.md)
  - [Generic Agent Runtime](adapters/generic-agent.md)

  ## Playbooks

  #{skills.map { |s| "- [`#{s["name"]}`](playbooks/#{s["name"]}/AGENT.md): #{s["description"]}" }.join("\n")}
MARKDOWN

write_file(File.join(OUT_DIR, "README.md"), index)

claude = <<~MARKDOWN
  # Claude / Claude Code Adapter

  Use these playbooks as project-level instructions or command-specific
  prompts.

  ## Claude Project

  1. Open the Claude project.
  2. Add the relevant `AGENT.md` contents to project instructions or knowledge.
  3. Upload any referenced templates or reference docs from the playbook folder.
  4. Tell Claude which tools are available and which actions require approval.

  ## Claude Code

  Recommended pattern:

  - Put persistent project guidance in `CLAUDE.md`.
  - Put specific playbooks in a `playbooks/` or `agent-playbooks/` folder.
  - Start a session with: `Use the <name> playbook from <path> for this task.`

  ## Tool Mapping

  - Shell commands: Claude Code terminal.
  - File edits: Claude Code patch/edit flow.
  - Browser checks: Playwright, browser MCP, or a platform browser tool.
  - External services: use real connectors only when available and authorized.
  - Memory/ledgers: use local markdown/jsonl files if the platform has no native
    memory API.
MARKDOWN

generic = <<~MARKDOWN
  # Generic Agent Runtime Adapter

  A playbook has three parts:

  - trigger: when to use it.
  - portability notes: what to adapt.
  - instructions: the operational procedure.

  Minimum runtime capabilities:

  - Read and edit files.
  - Run shell commands or equivalent validation.
  - Preserve a task log or durable notes.
  - Ask for explicit approval before gated actions.

  If the runtime lacks a capability, treat that as a blocker and report the
  missing tool instead of pretending the action happened.
MARKDOWN

write_file(File.join(OUT_DIR, "adapters", "claude.md"), claude)
write_file(File.join(OUT_DIR, "adapters", "generic-agent.md"), generic)

puts "Generated #{skills.length} portable playbooks in #{OUT_DIR}"
