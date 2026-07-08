#!/usr/bin/env python3
"""Print a redacted ClickUp workspace/hierarchy/channel map for Preston's token."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TOKEN_PATHS = [
    Path("/Users/preston/Code/sgs_admin/src/sync/load/.env"),
    Path("/Users/preston/Code/sgs_admin/src/sync/timeentry/.env"),
]


def load_token() -> tuple[str, list[str], int]:
    tokens: dict[str, list[str]] = {}
    env_token = os.environ.get("CLICKUP_PK_TOKEN")
    if env_token:
        tokens.setdefault(env_token, ["$CLICKUP_PK_TOKEN"])

    for path in TOKEN_PATHS:
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            match = re.match(r"\s*CLICKUP_PK_TOKEN\s*=\s*(.+?)\s*$", line)
            if match:
                token = match.group(1).strip().strip("\"'")
                tokens.setdefault(token, []).append(str(path))

    if not tokens:
        raise SystemExit("No CLICKUP_PK_TOKEN found in env or known files.")

    token = next(iter(tokens))
    return token, tokens[token], len(tokens)


class ClickUp:
    def __init__(self, token: str) -> None:
        self.token = token
        self.requests = 0

    def get(self, base: str, path: str, params: dict[str, str] | None = None) -> tuple[int, object]:
        self.requests += 1
        query = f"?{urllib.parse.urlencode(params)}" if params else ""
        request = urllib.request.Request(
            f"{base}{path}{query}",
            headers={"Authorization": self.token, "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            return exc.code, {"error": exc.read().decode("utf-8", errors="replace")[:1000]}


def summarize_list(item: dict) -> dict:
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "task_count": item.get("task_count"),
        "permission_level": item.get("permission_level"),
        "archived": item.get("archived"),
    }


def main() -> int:
    token, token_sources, distinct_tokens = load_token()
    client = ClickUp(token)
    v2 = "https://api.clickup.com/api/v2"
    v3 = "https://api.clickup.com/api/v3"

    user_status, user_body = client.get(v2, "/user")
    team_status, team_body = client.get(v2, "/team")
    if team_status != 200 or not isinstance(team_body, dict):
        print(json.dumps({"team_status": team_status, "team_body": team_body}, indent=2))
        return 1

    output = {
        "token_sources": token_sources,
        "distinct_tokens_found": distinct_tokens,
        "user_status": user_status,
        "user": (user_body or {}).get("user", {}) if isinstance(user_body, dict) else {},
        "workspaces": [],
    }

    for team in team_body.get("teams", []):
        workspace_id = str(team.get("id"))
        workspace = {
            "id": workspace_id,
            "name": team.get("name"),
            "spaces": [],
            "shared": {},
            "chat_channels": [],
            "errors": [],
        }

        space_status, space_body = client.get(v2, f"/team/{workspace_id}/space", {"archived": "false"})
        if space_status == 200 and isinstance(space_body, dict):
            for space in space_body.get("spaces", []):
                space_id = str(space.get("id"))
                space_summary = {
                    "id": space_id,
                    "name": space.get("name"),
                    "private": space.get("private"),
                    "folderless_lists": [],
                    "folders": [],
                }
                list_status, list_body = client.get(v2, f"/space/{space_id}/list", {"archived": "false"})
                if list_status == 200 and isinstance(list_body, dict):
                    space_summary["folderless_lists"] = [summarize_list(item) for item in list_body.get("lists", [])]
                else:
                    workspace["errors"].append({"space": space_id, "scope": "folderless_lists", "status": list_status})

                folder_status, folder_body = client.get(v2, f"/space/{space_id}/folder", {"archived": "false"})
                if folder_status == 200 and isinstance(folder_body, dict):
                    for folder in folder_body.get("folders", []):
                        folder_id = str(folder.get("id"))
                        folder_summary = {"id": folder_id, "name": folder.get("name"), "lists": []}
                        folder_list_status, folder_list_body = client.get(
                            v2, f"/folder/{folder_id}/list", {"archived": "false"}
                        )
                        if folder_list_status == 200 and isinstance(folder_list_body, dict):
                            folder_summary["lists"] = [
                                summarize_list(item) for item in folder_list_body.get("lists", [])
                            ]
                        else:
                            workspace["errors"].append(
                                {"folder": folder_id, "scope": "folder_lists", "status": folder_list_status}
                            )
                        space_summary["folders"].append(folder_summary)
                else:
                    workspace["errors"].append({"space": space_id, "scope": "folders", "status": folder_status})
                workspace["spaces"].append(space_summary)
        else:
            workspace["errors"].append({"scope": "spaces", "status": space_status, "body": space_body})

        shared_status, shared_body = client.get(v2, f"/team/{workspace_id}/shared")
        if shared_status == 200 and isinstance(shared_body, dict):
            shared = shared_body.get("shared", {})
            workspace["shared"] = {
                "folders": [summarize_list(item) for item in shared.get("folders", [])],
                "lists": [summarize_list(item) for item in shared.get("lists", [])],
                "tasks": [summarize_list(item) for item in shared.get("tasks", [])],
            }
        else:
            workspace["errors"].append({"scope": "shared", "status": shared_status, "body": shared_body})

        channel_status, channel_body = client.get(
            v3,
            f"/workspaces/{workspace_id}/chat/channels",
            {"limit": "100", "description_format": "text/plain", "include_closed": "false"},
        )
        if channel_status == 200 and isinstance(channel_body, dict):
            channels = channel_body.get("data", [])
            for channel in channels:
                if not isinstance(channel, dict):
                    continue
                workspace["chat_channels"].append(
                    {
                        "id": channel.get("id"),
                        "name": channel.get("name"),
                        "type": channel.get("type"),
                        "visibility": channel.get("visibility"),
                        "location": channel.get("location") or channel.get("parent"),
                        "latest_comment_at": channel.get("latest_comment_at"),
                    }
                )
        else:
            workspace["errors"].append({"scope": "chat_channels", "status": channel_status, "body": channel_body})

        output["workspaces"].append(workspace)

    output["request_count"] = client.requests
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
