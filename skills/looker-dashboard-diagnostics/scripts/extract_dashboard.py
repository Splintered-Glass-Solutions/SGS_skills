#!/usr/bin/env python3
"""Extract Looker dashboard tile metadata and generated SQL.

This script intentionally uses only the Python standard library so it can run
from a fresh Codex workspace without installing the Looker SDK.
"""

from __future__ import annotations

import argparse
import configparser
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_FIELDS = (
    "id,title,type,query_id,look_id,look,query,result_maker,merge_result_id,"
    "vis_config,body_text,subtitle_text,title_text,edit_uri"
)


def load_ini(path: str | None) -> dict[str, str]:
    if not path:
        candidates = [
            os.environ.get("LOOKERSDK_INI"),
            os.path.join(os.getcwd(), ".looker.ini"),
            os.path.expanduser("~/.looker.ini"),
        ]
        path = next((candidate for candidate in candidates if candidate and os.path.exists(candidate)), None)
    if not path or not os.path.exists(path):
        return {}

    parser = configparser.ConfigParser()
    parser.read(path)
    section = "Looker"
    if section not in parser and parser.sections():
        section = parser.sections()[0]
    values = dict(parser[section]) if section in parser else {}
    return {
        "base_url": values.get("base_url") or values.get("api_url") or values.get("looker_base_url", ""),
        "client_id": values.get("client_id", ""),
        "client_secret": values.get("client_secret", ""),
    }


def normalize_base_url(raw: str) -> str:
    if not raw:
        raise ValueError("Missing LOOKERSDK_BASE_URL or base_url in .looker.ini")
    base = raw.rstrip("/")
    base = re.sub(r"/api/(?:3\.1|4\.0)$", "", base)
    return base


class LookerClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str, timeout: int = 60) -> None:
        self.base_url = normalize_base_url(base_url)
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self.token = ""

    def login(self) -> None:
        body = urllib.parse.urlencode(
            {"client_id": self.client_id, "client_secret": self.client_secret}
        ).encode()
        data = self._request("POST", "/api/4.0/login", body=body, auth=False)
        self.token = data["access_token"]

    def get(self, path: str, params: dict[str, Any] | None = None, text: bool = False) -> Any:
        return self._request("GET", path, params=params, text=text)

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        body: bytes | None = None,
        auth: bool = True,
        text: bool = False,
    ) -> Any:
        query = urllib.parse.urlencode(params or {}, doseq=True)
        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{query}"
        headers = {"Accept": "application/json"}
        if body is not None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        if auth and self.token:
            headers["Authorization"] = f"token {self.token}"

        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                payload = response.read()
                if text:
                    return payload.decode("utf-8", errors="replace")
                if not payload:
                    return None
                return json.loads(payload.decode("utf-8"))
        except urllib.error.HTTPError as exc:
            message = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"{method} {path} failed with HTTP {exc.code}: {message}") from exc


def dashboard_id_from_value(value: str) -> str:
    match = re.search(r"/dashboards/(?:[^/]+::)?([A-Za-z0-9_-]+)", value)
    if match:
        return match.group(1)
    return value


def nested_get(obj: dict[str, Any], keys: list[str]) -> Any:
    current: Any = obj
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def find_query_id(element: dict[str, Any]) -> str | None:
    candidates = [
        element.get("query_id"),
        nested_get(element, ["query", "id"]),
        nested_get(element, ["look", "query_id"]),
        nested_get(element, ["look", "query", "id"]),
        nested_get(element, ["result_maker", "query_id"]),
        nested_get(element, ["result_maker", "query", "id"]),
    ]
    for candidate in candidates:
        if candidate not in (None, ""):
            return str(candidate)
    return None


def summarize_query(element: dict[str, Any]) -> dict[str, Any]:
    query = element.get("query") or nested_get(element, ["look", "query"]) or nested_get(element, ["result_maker", "query"]) or {}
    if not isinstance(query, dict):
        query = {}
    keys = [
        "id",
        "model",
        "view",
        "fields",
        "pivots",
        "fill_fields",
        "filters",
        "filter_expression",
        "sorts",
        "limit",
        "column_limit",
        "dynamic_fields",
        "query_timezone",
    ]
    return {key: query.get(key) for key in keys if key in query and query.get(key) not in (None, "", [])}


def extract_tables(sql: str) -> list[str]:
    pattern = re.compile(
        r'\b(?:from|join)\s+((?:"[^"]+"|`[^`]+`|\[[^\]]+\]|[A-Za-z0-9_$]+)(?:\s*\.\s*(?:"[^"]+"|`[^`]+`|\[[^\]]+\]|[A-Za-z0-9_$]+)){0,3})',
        re.IGNORECASE,
    )
    tables: list[str] = []
    for match in pattern.finditer(sql or ""):
        table = re.sub(r"\s+", "", match.group(1)).replace('"', "").replace("`", "")
        if table not in tables:
            tables.append(table)
    return tables


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dashboard", required=True, help="Looker dashboard id or dashboard URL")
    parser.add_argument("--output", help="Write JSON artifact to this path")
    parser.add_argument("--ini", help="Optional .looker.ini path")
    parser.add_argument("--base-url", help="Override LOOKERSDK_BASE_URL")
    parser.add_argument("--client-id", help="Override LOOKERSDK_CLIENT_ID")
    parser.add_argument("--client-secret", help="Override LOOKERSDK_CLIENT_SECRET")
    parser.add_argument("--no-sql", action="store_true", help="Skip generated SQL extraction")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    ini = load_ini(args.ini)
    base_url = args.base_url or os.environ.get("LOOKERSDK_BASE_URL") or ini.get("base_url", "")
    client_id = args.client_id or os.environ.get("LOOKERSDK_CLIENT_ID") or ini.get("client_id", "")
    client_secret = args.client_secret or os.environ.get("LOOKERSDK_CLIENT_SECRET") or ini.get("client_secret", "")
    if not client_id or not client_secret:
        print("Missing LOOKERSDK_CLIENT_ID/LOOKERSDK_CLIENT_SECRET or .looker.ini credentials", file=sys.stderr)
        return 2

    dashboard_id = dashboard_id_from_value(args.dashboard)
    client = LookerClient(base_url, client_id, client_secret, timeout=args.timeout)
    client.login()

    dashboard = client.get(
        f"/api/4.0/dashboards/{urllib.parse.quote(dashboard_id)}",
        params={"fields": "id,title,description,folder,dashboard_filters,created_at,updated_at,user_id"},
    )
    elements = client.get(
        f"/api/4.0/dashboards/{urllib.parse.quote(dashboard_id)}/dashboard_elements",
        params={"fields": DEFAULT_FIELDS},
    )

    tile_reports: list[dict[str, Any]] = []
    for element in elements:
        query_id = find_query_id(element)
        report = {
            "element_id": element.get("id"),
            "title": element.get("title") or element.get("title_text"),
            "type": element.get("type"),
            "look_id": element.get("look_id"),
            "query_id": query_id,
            "query": summarize_query(element),
            "vis_config": element.get("vis_config"),
            "status": "ok",
        }
        if not query_id:
            report["status"] = "missing_query_id"
        elif not args.no_sql:
            try:
                sql = client.get(f"/api/4.0/queries/{urllib.parse.quote(query_id)}/run/sql", text=True)
                report["generated_sql"] = sql
                report["warehouse_objects"] = extract_tables(sql)
            except Exception as exc:  # Keep one failing tile from blocking inventory.
                report["status"] = "sql_error"
                report["error"] = str(exc)
        tile_reports.append(report)
        time.sleep(0.1)

    artifact = {
        "extracted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "looker_base_url": normalize_base_url(base_url),
        "dashboard_id": dashboard_id,
        "dashboard": dashboard,
        "tile_count": len(tile_reports),
        "tiles": tile_reports,
    }

    output = json.dumps(artifact, indent=2, sort_keys=True)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
            handle.write("\n")
        print(args.output)
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
