# Mockups Agent Playbook

This is a platform-neutral version of the `mockups` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Generate three to five realistic image mockups of a planned feature in its actual product UI to compare layout, style, hierarchy, and user experience before implementation. Use for visual alignment or alternative UI directions from a feature discussion, plan, or reference screenshot.

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

# Mockups

Turn the feature being discussed into visually grounded alternatives that help the user decide what to build. Deliver images of the feature inside the product, with enough fidelity to judge how the proposed changes would actually look and feel.

## Establish the visual brief

Reuse the current conversation, accepted plan, and provided references. Extract the target screen, intended user, primary task, required content/actions, constraints, and relevant interaction states. Do not restart discovery or ask the user to repeat an adequate brief.

Default to **three variations**. Honor an explicit count, including four or five. If the user simply requests three to five, use three unless additional directions offer meaningfully different choices. State the chosen count before generating.

For an existing product, inspect its actual visual context:

- View supplied screenshots and attach the actual images to generation.
- If needed, capture the relevant existing UI through an available browser tool, respecting the user's browser preference. Use read-only navigation for this task.
- Inspect only the nearby components, tokens, or design documentation needed to match typography, spacing, colors, icons, navigation, and container dimensions.
- Prefer the current target surface over unrelated inspiration. A screenshot of a similar screen can supplement it.

If the product cannot be visually inspected, identify the missing reference and ask for the screenshot, URL, or correct workspace when that prevents a faithful result. If the user authorizes proceeding without it, disclose the approximation. For a new product, use the available brand direction and state reasonable assumptions. Never claim exact product matching from a text description alone.

## Design meaningful alternatives

Give each direction a short descriptive name and a concrete layout idea before generation. Hold the feature requirements, representative data, product shell, visual language, viewport, and workflow scenario consistent across alternatives. Vary what helps make the decision: information hierarchy, grouping, density, placement, navigation within the feature, or interaction pattern.

For example, compare an inline workspace, a contextual side panel, and a focused detail view when those patterns fit the task. Do not manufacture alternatives by changing only colors or moving a button. Explore a new visual style only when requested or when no established style exists.

Show the surrounding product context so the proposed feature's location is clear. Preserve existing navigation, logos, typography, and unaffected UI as closely as possible. Include every required action; avoid adding unrelated functionality to fill space. Use plausible sample content and clear labels, treating invented data as illustrative. Anchor time-sensitive mock data to the session's current date unless the brief requires other dates.

Match the reference viewport and aspect ratio. Otherwise choose a realistic viewport for the intended surface, using desktop by default when context supports it. Show modals and drawers within their host screen when placement matters. Add a supporting state or mobile frame only when needed to explain the proposed experience; these extra frames do not replace the requested number of alternatives.

## Generate and inspect the images

Use the built-in Image Gen tool, following the available `imagegen` skill's tool guidance. Each variation gets its own image and prompt. Generate sequentially so each image can be inspected and its identity stays clear. Do not substitute a prose description, prompt list, wireframe, or coded prototype for the requested images.

Attach actual reference images using the tool's supported reference mechanism. Inspect local references before using them. Clearly distinguish the existing UI reference, an edit target, and a previous concept being refined. For first-pass alternatives, ground each in the original product reference rather than allowing one generated variant to redefine the product style.

Adapt this prompt outline for each direction:

```text
Use case: ui-mockup
Deliverable: one realistic, high-fidelity screen image for visual design alignment.
Product and target surface: <product, screen, user, primary task>
Reference images and roles: <actual attached references>
Viewport: <dimensions/aspect ratio matching the target>
Feature requirements: <required content, actions, hard constraints>
Direction: <name and concrete layout/interaction strategy>
Visible state: <scenario, selected item, modal or panel state>
Preserve: <existing shell, branding, type, spacing, components, unaffected regions>
Change: <precise feature additions or rearrangements>
Text and sample data: <key labels verbatim; consistent representative content>
Rendering: straight-on product screenshot; readable text and realistic spacing.
Avoid: unrelated features, unintended redesign, clipped controls, decorative device frames.
```

Inspect each result for reference fidelity, required content/actions, legibility, layout feasibility, and meaningful difference from the other directions. Correct material problems with a targeted regeneration; do not repeatedly polish minor artifacts. If a tool call fails, retry once when appropriate. Report a persistent failure and the delivered count honestly; an incomplete set is not a completed comparison.

Display every successful image inline exactly once using the tool's generated-image presentation or an absolute local image path. Assign option numbers in displayed order, recording the associated concept and artifact so a later selection resolves to the right image.

## Deliver the comparison and refine

After all requested images are visible, provide a compact comparison: option number/name, main layout choice, and the practical UX tradeoff. Mention material approximations such as uncertain reference styling or inaccurate generated text. Generated images are design proposals, not proof of implemented behavior or pixel-exact runtime rendering.

Keep a lightweight record of the brief, reference paths/source, prompts, numbered artifact mapping, and any chosen direction beside the saved mockups. Use the user's destination when supplied; otherwise use a clearly named project output folder for project work. For preview-only work, the images may remain in the tool's output location. Preserve earlier sets rather than overwriting them.

Ask which direction the user prefers or what they want to combine or refine. Stop at visual alignment unless implementation is already explicitly requested. Selecting an image identifies the design target; it does not by itself authorize code changes or deployment.

For feedback, refine the chosen image or combine the specified parts into a new image. Preserve the agreed elements, explain what changed, and retain an unambiguous mapping to the new result. If a numeric selection cannot be resolved to a displayed artifact, ask for the concept or image rather than guessing. When the user requests implementation, carry the selected artifact, constraints, and feedback into that workflow.
