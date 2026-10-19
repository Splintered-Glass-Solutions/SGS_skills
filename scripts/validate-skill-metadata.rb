#!/usr/bin/env ruby
# frozen_string_literal: true
require "yaml"
root = File.expand_path("..", __dir__)
count = 0
errors = []
Dir[File.join(root, "skills/*/SKILL.md")].sort.each do |path|
  begin
    text = File.read(path)
    raise "missing frontmatter" unless text.start_with?("---\n")
    data = YAML.safe_load(text.split(/^---\s*$/, 3)[1])
    name = File.basename(File.dirname(path))
    raise "name must match folder" unless data["name"] == name
    raise "description missing" if data["description"].to_s.strip.empty?
    metadata = File.join(File.dirname(path), "agents/openai.yaml")
    if File.exist?(metadata)
      agent = YAML.safe_load(File.read(metadata))
      raise "agent interface missing" unless agent["interface"].is_a?(Hash)
    end
    count += 1
  rescue StandardError => error
    errors << "#{path.delete_prefix(root + '/')}: #{error.message.lines.first.strip}"
  end
end
Dir[File.join(root, "commands/*.md")].sort.each do |path|
  begin
    name = File.basename(path, ".md")
    raise "source skill missing" unless File.exist?(File.join(root, "skills", name, "SKILL.md"))
    text = File.read(path)
    YAML.safe_load(text.split(/^---\s*$/, 3)[1]) if text.start_with?("---\n")
  rescue StandardError => error
    errors << "#{path.delete_prefix(root + '/')}: #{error.message.lines.first.strip}"
  end
end
abort errors.join("\n") unless errors.empty?
puts "PASS: #{count} skill frontmatters, available agent metadata and command sources"
