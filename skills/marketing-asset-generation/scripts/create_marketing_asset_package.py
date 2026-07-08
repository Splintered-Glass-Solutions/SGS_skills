#!/usr/bin/env python3
"""Create a reusable Bonfire marketing asset package scaffold."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from textwrap import fill


DEFAULT_PERSONAS = ["persona-selection-needed"]
DEFAULT_SIZES = ["square", "landscape", "story"]
DEFAULT_OUTPUTS = ["headline", "subtitle", "image"]
VALID_SIZES = {"square", "landscape", "story"}
VALID_OUTPUTS = {"headline", "subtitle", "image"}
VALID_ASSET_STATUSES = {"planned", "generated", "reused", "failed", "blocked"}
ASSET_DIMENSIONS = {
    "square": (1080, 1080),
    "landscape": (1200, 675),
    "story": (1080, 1920),
}
BRAND_ORANGE = "#ef6b2d"
BRAND_EMBER = "#b7411e"
BRAND_SLATE = "#25313f"
BRAND_MUTED = "#657385"
BRAND_CREAM = "#fff7ed"
BRAND_WHITE = "#fffefd"
BRAND_BLUE = "#3c6e89"


@dataclass(frozen=True)
class PersonaCopy:
    headline: str
    subtitle: str


PERSONA_COPY: dict[str, PersonaCopy] = {
    "business owner": PersonaCopy(
        "Turn questions into next steps",
        "Help buyers get clear answers before a staff member ever jumps in.",
    ),
    "business employee": PersonaCopy(
        "Fewer repeated questions",
        "Give your team a reliable helper for the questions that keep coming up.",
    ),
    "technical buyer": PersonaCopy(
        "Deploy with confidence",
        "Preview, configure, and launch a controlled Bonfire experience.",
    ),
    "non-technical buyer": PersonaCopy(
        "Launch without the complexity",
        "Give visitors a helpful experience without making setup harder.",
    ),
    "church network leader": PersonaCopy(
        "Scale trusted guidance",
        "Support more churches with consistent, grounded answers.",
    ),
    "senior pastor": PersonaCopy(
        "Guide the next faithful step",
        "Make trusted church answers easier for people to find.",
    ),
    "executive pastor": PersonaCopy(
        "Reduce friction for guests",
        "Help people find ministries, events, and next steps faster.",
    ),
    "communications pastor/director": PersonaCopy(
        "Make your website speak clearly",
        "Turn scattered visitor questions into clear, consistent next steps.",
    ),
    "communications director": PersonaCopy(
        "Make your website speak clearly",
        "Turn scattered visitor questions into clear, consistent next steps.",
    ),
    "ministry leader": PersonaCopy(
        "Connect people faster",
        "Help people find the right ministry, resource, or care path.",
    ),
    "congregant": PersonaCopy(
        "Find answers you can trust",
        "Get clear guidance from the voices your church already trusts.",
    ),
    "persona-selection-needed": PersonaCopy(
        "Choose the audience first",
        "Select one or more personas so the asset can speak to a real need.",
    ),
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "bonfire-feature"


def split_csv(values: list[str] | None) -> list[str]:
    if not values:
        return []
    result: list[str] = []
    for value in values:
        result.extend(part.strip() for part in value.split(",") if part.strip())
    return result


def normalize_unique(values: list[str], fallback: list[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []
    for value in values:
        cleaned = " ".join(value.strip().split())
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(cleaned)
    return normalized or fallback


def default_output_root() -> Path:
    cwd = Path.cwd()
    if (cwd / ".git").exists() or (cwd / "package.json").exists():
        return cwd / "output" / "marketing-assets"
    return Path.home() / "Marketing Assets" / "Bonfire"


def unique_package_dir(base: Path) -> Path:
    if not base.exists():
        return base
    index = 2
    while True:
        candidate = base.with_name(f"{base.name}-{index}")
        if not candidate.exists():
            return candidate
        index += 1


def copy_for_persona(persona: str, feature_name: str) -> PersonaCopy:
    base = PERSONA_COPY.get(persona.lower())
    if base:
        return base
    return PersonaCopy(
        f"{feature_name} for {persona}",
        f"A focused Bonfire asset tailored to {persona}.",
    )


def prompt_for(
    *,
    feature_name: str,
    description: str,
    persona: str,
    size: str,
    copy: PersonaCopy,
    include_screenshot: bool,
) -> str:
    screenshot_line = (
        "Use the provided screenshot as the accurate product UI reference. Do not invent product facts."
        if include_screenshot
        else "Use an honest Bonfire-branded product visual or abstract UI frame; do not fake detailed UI."
    )
    return "\n".join(
        [
            f"# Prompt: {persona} / {size}",
            "",
            "Create a clean Bonfire-branded promotional image.",
            "",
            f"- Feature: {feature_name}",
            f"- Persona: {persona}",
            f"- Size: {size}",
            f"- Headline: {copy.headline}",
            f"- Subtitle: {copy.subtitle}",
            f"- Feature description: {description}",
            f"- Screenshot guidance: {screenshot_line}",
            "- Brand: warm ember accents, crisp white/slate UI framing, generous whitespace, Bonfire logo or mark.",
            "- Keep text minimal, legible, and inside safe margins.",
            "- Avoid clutter, fake metrics, private customer data, exaggerated AI claims, and dark sci-fi styling.",
            "",
        ]
    )


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature-name", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--persona", action="append", default=[])
    parser.add_argument("--personas", action="append", default=[])
    parser.add_argument("--size", action="append", default=[])
    parser.add_argument("--sizes", action="append", default=[])
    parser.add_argument("--output-option", action="append", default=[])
    parser.add_argument("--output-options", action="append", default=[])
    parser.add_argument("--include-screenshot", action="store_true")
    parser.add_argument("--screenshot", action="append", default=[])
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--live-status", default="unknown")
    parser.add_argument(
        "--asset-status",
        choices=sorted(VALID_ASSET_STATUSES),
        default="generated",
        help="Default status for requested image assets.",
    )
    parser.add_argument(
        "--no-generate-images",
        action="store_true",
        help="Write prompts and manifest rows without rendering local PNG assets.",
    )
    parser.add_argument(
        "--reuse-asset",
        action="append",
        default=[],
        metavar="PERSONA:SIZE:PATH",
        help="Mark a specific persona/size row as reused from an existing asset.",
    )
    parser.add_argument(
        "--status-note",
        default="",
        help="Optional note applied to generated, failed, blocked, planned, or reused image rows.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    feature_name = " ".join(args.feature_name.split())
    description = " ".join(args.description.split())
    personas = normalize_unique(
        [*args.persona, *split_csv(args.personas)],
        DEFAULT_PERSONAS,
    )
    requested_sizes = normalize_unique(
        [*args.size, *split_csv(args.sizes)],
        DEFAULT_SIZES,
    )
    sizes = [size for size in requested_sizes if size in VALID_SIZES] or DEFAULT_SIZES
    requested_outputs = normalize_unique(
        [*args.output_option, *split_csv(args.output_options)],
        DEFAULT_OUTPUTS,
    )
    outputs = [
        output for output in requested_outputs if output in VALID_OUTPUTS
    ] or DEFAULT_OUTPUTS

    root = Path(args.output_root).expanduser() if args.output_root else default_output_root()
    package_dir = unique_package_dir(
        root / f"{date.today().isoformat()}-{slugify(feature_name)}"
    )
    prompts_dir = package_dir / "prompts"
    raw_dir = package_dir / "raw-screenshots"
    generated_dir = package_dir / "generated-assets"
    exports_dir = package_dir / "exports"
    for directory in [prompts_dir, raw_dir, generated_dir, exports_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    copied_screenshots: list[str] = []
    for screenshot in args.screenshot:
        source = Path(screenshot).expanduser()
        if source.exists() and source.is_file():
            target = raw_dir / source.name
            if source.resolve() != target.resolve():
                shutil.copy2(source, target)
            copied_screenshots.append(str(target))
        else:
            copied_screenshots.append(f"missing: {screenshot}")

    include_screenshot = args.include_screenshot or bool(args.screenshot)
    reused_assets = parse_reused_assets(args.reuse_asset)
    rows: list[dict[str, str]] = []
    image_generation_errors: list[str] = []
    for persona in personas:
        copy = copy_for_persona(persona, feature_name)
        for size in sizes:
            prompt_path = prompts_dir / f"{slugify(persona)}-{size}.md"
            if "image" in outputs:
                write(
                    prompt_path,
                    prompt_for(
                        feature_name=feature_name,
                        description=description,
                        persona=persona,
                        size=size,
                        copy=copy,
                        include_screenshot=include_screenshot,
                    ),
                )
                reused_path = reused_assets.get((persona.lower(), size))
                image_status = "reused" if reused_path else args.asset_status
                image_path = (
                    reused_path
                    if reused_path
                    else str(generated_dir / f"{slugify(persona)}-{size}.png")
                )
                if (
                    not reused_path
                    and not args.no_generate_images
                    and args.asset_status == "generated"
                ):
                    try:
                        render_marketing_asset(
                            path=Path(image_path),
                            feature_name=feature_name,
                            description=description,
                            persona=persona,
                            size=size,
                            copy=copy,
                            live_status=args.live_status,
                            include_screenshot=include_screenshot,
                        )
                    except Exception as exc:  # pragma: no cover - defensive runtime fallback
                        image_status = "failed"
                        image_generation_errors.append(
                            f"{persona} / {size}: {type(exc).__name__}: {exc}"
                        )
            else:
                image_status = "not-requested"
                image_path = ""
            rows.append(
                {
                    "persona": persona,
                    "size": size,
                    "headline": copy.headline if "headline" in outputs else "",
                    "subtitle": copy.subtitle if "subtitle" in outputs else "",
                    "image_status": image_status,
                    "image_path": image_path,
                    "prompt_path": str(prompt_path) if "image" in outputs else "",
                    "status_note": (
                        args.status_note
                        or (
                            "Generated local Bonfire-branded promotional PNG."
                            if image_status == "generated"
                            else ""
                        )
                    ),
                }
            )

    manifest = {
        "feature_name": feature_name,
        "description": description,
        "live_status": args.live_status,
        "personas": personas,
        "sizes": sizes,
        "output_options": outputs,
        "include_screenshot": include_screenshot,
        "screenshots": copied_screenshots,
        "default_asset_status": args.asset_status,
        "image_generation": {
            "enabled": not args.no_generate_images,
            "errors": image_generation_errors,
        },
        "package_path": str(package_dir),
        "assets": rows,
    }

    write(package_dir / "asset-manifest.json", json.dumps(manifest, indent=2) + "\n")
    write(package_dir / "creative-brief.md", creative_brief(manifest))
    write(package_dir / "copy-matrix.md", copy_matrix(rows))
    write(package_dir / "asset-manifest.md", asset_manifest_md(manifest, rows))
    write(package_dir / "backlog.md", backlog_md(manifest))

    print(json.dumps({"package_path": str(package_dir), "asset_count": len(rows)}, indent=2))
    return 0


def render_marketing_asset(
    *,
    path: Path,
    feature_name: str,
    description: str,
    persona: str,
    size: str,
    copy: PersonaCopy,
    live_status: str,
    include_screenshot: bool,
) -> None:
    from PIL import Image, ImageDraw, ImageFont

    width, height = ASSET_DIMENSIONS[size]
    img = Image.new("RGB", (width, height), BRAND_CREAM)
    draw = ImageDraw.Draw(img)

    draw_gradient(draw, width, height)
    margin = int(width * 0.07)
    top = int(height * 0.08)

    title_font = load_font(size_for(width, height, 66))
    subtitle_font = load_font(size_for(width, height, 28))
    small_font = load_font(size_for(width, height, 21))
    chip_font = load_font(size_for(width, height, 20))
    brand_font = load_font(size_for(width, height, 27))

    draw_brand(draw, margin, top, brand_font)
    content_top = top + int(height * 0.12)

    if size == "story":
        visual_box = (
            margin,
            int(height * 0.50),
            width - margin,
            height - int(height * 0.08),
        )
        text_right = width - margin
    elif size == "landscape":
        visual_box = (
            int(width * 0.58),
            int(height * 0.17),
            width - margin,
            height - int(height * 0.11),
        )
        text_right = int(width * 0.53)
    else:
        visual_box = (
            margin,
            int(height * 0.58),
            width - margin,
            height - int(height * 0.08),
        )
        text_right = width - margin

    eyebrow = f"{persona}  |  {normalize_live_status(live_status)}"
    draw.text((margin, content_top), eyebrow, fill=BRAND_BLUE, font=small_font)
    content_top += int(height * 0.055)

    headline_lines = wrap_text(draw, copy.headline, title_font, text_right - margin)
    for line in headline_lines[:3]:
        draw.text((margin, content_top), line, fill=BRAND_SLATE, font=title_font)
        content_top += int(title_font.size * 1.12)

    content_top += int(height * 0.02)
    subtitle_lines = wrap_text(draw, copy.subtitle, subtitle_font, text_right - margin)
    for line in subtitle_lines[:3]:
        draw.text((margin, content_top), line, fill=BRAND_MUTED, font=subtitle_font)
        content_top += int(subtitle_font.size * 1.35)

    chips = visual_chips_for(feature_name, description)
    if include_screenshot:
        chips.append("Screenshot-guided")
    draw_chips(draw, margin, content_top + int(height * 0.035), text_right, chips, chip_font)
    draw_product_visual(draw, visual_box, feature_name, description, chip_font, small_font)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)


def draw_gradient(draw: object, width: int, height: int) -> None:
    for y in range(height):
        ratio = y / max(height - 1, 1)
        r = int(255 * (1 - ratio) + 250 * ratio)
        g = int(247 * (1 - ratio) + 238 * ratio)
        b = int(237 * (1 - ratio) + 226 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    for i in range(7):
        alpha = 1 - i / 7
        radius = int(width * (0.15 + i * 0.018))
        x = int(width * 0.90)
        y = int(height * 0.12)
        color = blend("#ffd6bd", BRAND_CREAM, 1 - alpha * 0.45)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)


def draw_brand(draw: object, x: int, y: int, font: object) -> None:
    mark = int(font.size * 1.2)
    draw.rounded_rectangle((x, y, x + mark, y + mark), radius=mark // 3, fill=BRAND_ORANGE)
    inner = int(mark * 0.25)
    draw.ellipse((x + inner, y + inner, x + mark - inner, y + mark - inner), fill=BRAND_WHITE)
    draw.text((x + mark + int(mark * 0.35), y + int(mark * 0.05)), "Bonfire", fill=BRAND_SLATE, font=font)


def draw_chips(draw: object, x: int, y: int, max_right: int, chips: list[str], font: object) -> None:
    cursor_x = x
    cursor_y = y
    pad_x = int(font.size * 0.75)
    pad_y = int(font.size * 0.45)
    gap = int(font.size * 0.45)
    for chip in chips:
        box = draw.textbbox((0, 0), chip, font=font)
        chip_w = box[2] - box[0] + pad_x * 2
        chip_h = box[3] - box[1] + pad_y * 2
        if cursor_x + chip_w > max_right:
            cursor_x = x
            cursor_y += chip_h + gap
        draw.rounded_rectangle(
            (cursor_x, cursor_y, cursor_x + chip_w, cursor_y + chip_h),
            radius=chip_h // 2,
            fill="#fffefd",
            outline="#f1d8c8",
            width=2,
        )
        draw.text((cursor_x + pad_x, cursor_y + pad_y - 1), chip, fill=BRAND_SLATE, font=font)
        cursor_x += chip_w + gap


def draw_product_visual(
    draw: object,
    box: tuple[int, int, int, int],
    feature_name: str,
    description: str,
    chip_font: object,
    small_font: object,
) -> None:
    left, top, right, bottom = box
    width = right - left
    height = bottom - top
    shadow = int(width * 0.018)
    draw.rounded_rectangle((left + shadow, top + shadow, right + shadow, bottom + shadow), radius=22, fill="#eed7c8")
    draw.rounded_rectangle((left, top, right, bottom), radius=22, fill=BRAND_WHITE, outline="#ead3c4", width=2)

    header_h = int(height * 0.16)
    draw.rounded_rectangle((left, top, right, top + header_h), radius=22, fill="#fff3ea")
    draw.rectangle((left, top + header_h - 22, right, top + header_h), fill="#fff3ea")
    header, sections, footer = visual_content_for(feature_name, description)
    draw.text((left + int(width * 0.06), top + int(header_h * 0.30)), header, fill=BRAND_SLATE, font=chip_font)
    row_top = top + header_h + int(height * 0.08)
    row_gap = int(height * 0.045)
    row_h = max(int(height * 0.14), chip_font.size * 2)
    for label, color in sections:
        draw.rounded_rectangle(
            (left + int(width * 0.06), row_top, right - int(width * 0.06), row_top + row_h),
            radius=14,
            fill="#fbfaf8",
            outline="#eee1d7",
            width=1,
        )
        dot = int(row_h * 0.25)
        draw.ellipse(
            (left + int(width * 0.10), row_top + int(row_h * 0.34), left + int(width * 0.10) + dot, row_top + int(row_h * 0.34) + dot),
            fill=color,
        )
        draw.text((left + int(width * 0.17), row_top + int(row_h * 0.24)), label, fill=BRAND_SLATE, font=chip_font)
        draw.line(
            (left + int(width * 0.17), row_top + int(row_h * 0.70), right - int(width * 0.14), row_top + int(row_h * 0.70)),
            fill="#e5dbd2",
            width=3,
        )
        row_top += row_h + row_gap

    draw.text((left + int(width * 0.06), bottom - int(height * 0.12)), footer, fill=BRAND_MUTED, font=small_font)


def is_source_skill_feature(feature_name: str, description: str) -> bool:
    key = f"{feature_name} {description}".lower()
    return "source" in key and ("skill" in key or "sync" in key or "connector" in key)


def visual_chips_for(feature_name: str, description: str) -> list[str]:
    if is_source_skill_feature(feature_name, description):
        return ["Content Source", "Connection Source", "Sync behavior"]
    return ["Product clarity", "Persona-specific", "Launch-ready"]


def visual_content_for(
    feature_name: str,
    description: str,
) -> tuple[str, list[tuple[str, str]], str]:
    if is_source_skill_feature(feature_name, description):
        return (
            "Source Details",
            [
                ("Content Source", BRAND_ORANGE),
                ("Sync Behavior", BRAND_BLUE),
                ("Connection Source", BRAND_EMBER),
                ("Skills Enabled", "#6a7d4f"),
            ],
            "Clear source behavior",
        )
    return (
        "Bonfire Feature",
        [
            ("Value", BRAND_ORANGE),
            ("Audience", BRAND_BLUE),
            ("Launch Copy", BRAND_EMBER),
            ("Assets", "#6a7d4f"),
        ],
        "Launch-ready asset",
    )


def load_font(size: int) -> object:
    from PIL import ImageFont

    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default(size=size)


def size_for(width: int, height: int, base: int) -> int:
    scale = math.sqrt((width * height) / (1080 * 1080))
    return max(14, int(base * scale))


def wrap_text(draw: object, text: str, font: object, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def blend(first: str, second: str, ratio: float) -> tuple[int, int, int]:
    ratio = max(0.0, min(1.0, ratio))
    a = tuple(int(first.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    b = tuple(int(second.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    return tuple(int(a[index] * (1 - ratio) + b[index] * ratio) for index in range(3))


def normalize_live_status(value: str) -> str:
    cleaned = " ".join(str(value or "unknown").split())
    return cleaned or "unknown"


def creative_brief(manifest: dict[str, object]) -> str:
    description = str(manifest["description"]) or "No description provided."
    wrapped = fill(description, width=88)
    return f"""# {manifest["feature_name"]} Marketing Asset Brief

Live status: {manifest["live_status"]}

## Feature Description

{wrapped}

## Personas

{bullet_list(manifest["personas"])}

## Sizes

{bullet_list(manifest["sizes"])}

## Screenshots

{bullet_list(manifest["screenshots"]) if manifest["screenshots"] else "- None provided."}

## Claims To Avoid

- Do not claim production availability unless live status is production and verified.
- Do not imply generated visuals are exact product screenshots unless they use real screenshots.
- Do not include private customer data, access tokens, raw logs, or unreleased-sensitive details.
"""


def copy_matrix(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Persona Copy Matrix",
        "",
        "| Persona | Size | Headline | Subtitle |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['persona']} | {row['size']} | {row['headline']} | {row['subtitle']} |"
        )
    return "\n".join(lines) + "\n"


def asset_manifest_md(manifest: dict[str, object], rows: list[dict[str, str]]) -> str:
    lines = [
        f"# {manifest['feature_name']} Asset Manifest",
        "",
        f"Package path: `{manifest['package_path']}`",
        "",
        "| Persona | Size | Headline | Subtitle | Status | Image Path | Prompt | Note |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {persona} | {size} | {headline} | {subtitle} | {image_status} | `{image_path}` | `{prompt_path}` | {status_note} |".format(
                **row
            )
        )
    return "\n".join(lines) + "\n"


def backlog_md(manifest: dict[str, object]) -> str:
    lines = [
        f"# {manifest['feature_name']} Marketing Asset Backlog",
        "",
        "Use this file for requested asset-generation capabilities that were not safe or scoped for the current run.",
        "",
    ]
    if manifest["personas"] == DEFAULT_PERSONAS:
        lines.extend(
            [
                "## Persona Selection",
                "",
                "- Status: blocked",
                "- Reason: no target personas were selected. Choose at least one audience before generating final assets.",
                "",
            ]
        )
    if not manifest["screenshots"] and manifest["include_screenshot"]:
        lines.extend(
            [
                "## Screenshot Asset",
                "",
                "- Status: blocked",
                "- Reason: screenshot inclusion was requested, but no valid screenshot file was provided.",
                "",
            ]
        )
    lines.extend(
        [
            "## Productized Bonfire App Workflow",
            "",
            "- Status: backlog",
            "- Reason: in-app persona multi-select, screenshot upload/select, persisted asset library, and provider-backed generation jobs require product scope, storage decisions, permissions, and API work outside this local skill.",
            "",
        ]
    )
    return "\n".join(lines)


def bullet_list(values: object) -> str:
    if not isinstance(values, list) or not values:
        return "- None."
    return "\n".join(f"- {value}" for value in values)


def parse_reused_assets(values: list[str]) -> dict[tuple[str, str], str]:
    reused: dict[tuple[str, str], str] = {}
    for value in values:
        persona, separator, remainder = value.partition(":")
        if not separator:
            continue
        size, separator, asset_path = remainder.partition(":")
        if not separator:
            continue
        normalized_size = size.strip()
        if normalized_size not in VALID_SIZES:
            continue
        reused[(persona.strip().lower(), normalized_size)] = asset_path.strip()
    return reused


if __name__ == "__main__":
    raise SystemExit(main())
