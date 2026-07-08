# Visual Iteration Loop Agent Playbook

This is a platform-neutral version of the `visual-iteration-loop` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Iterative visual quality workflow for auditing, improving, screenshotting, and retesting UI, game, 3D, WebGL, or graphics-heavy projects. Use when the user asks to loop through visuals, improve realism or polish, audit screenshots, compare against a target style, run multiple visual QA passes, continue until visuals improve, or stop after a maximum number of iterations.

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

# Visual Iteration Loop

Use this skill to run bounded audit/improve/retest loops for visual work. Treat visual quality as evidence-based: inspect the current product, make scoped improvements, capture screenshots, judge them, then repeat only while the next iteration is likely to create meaningful visible gain.

## Parameters

Infer these from the user request when possible:

- `max_iterations`: Default to 3. Use the user's requested maximum if provided. Do not exceed 6 unless the user explicitly asks for a longer run.
- `target_style`: Use attached screenshots, mockups, brand refs, or prior audit notes when provided. If no target exists, improve toward the app's existing style and the user's stated quality goal.
- `validation_level`: Default to relevant build/test plus browser or screenshot validation for visual surfaces.

If max iteration count is missing and the work is large or ambiguous, state the default before starting.

## Loop Protocol

For each iteration:

1. Capture the current visual state.
   - Run the app locally if needed.
   - Take screenshots for the relevant viewport/state.
   - For 3D/WebGL/canvas, verify the canvas is nonblank and framed correctly.

2. Audit visible issues.
   - Compare the screenshot to the target style or stated goal.
   - Identify concrete problems: scale, grounding, lighting, density, materials, silhouette, contrast, layout, animation state, clipping, overlap, blank space, or unrealistic props.
   - Rank issues by player/user impact.

3. Choose a scoped improvement.
   - Fix the highest-impact visible issue that can be completed safely in the current codebase.
   - Avoid unrelated refactors and non-MVP feature expansion.
   - Preserve user changes and existing project conventions.

4. Implement and validate.
   - Run relevant typecheck/unit/build checks after meaningful code changes.
   - Re-run browser/screenshot validation for the exact state being improved.
   - For 3D/WebGL, check screenshots or canvas pixels after each visual pass.

5. Decide whether to continue.
   - Continue only if the next issue is visible, important, and scoped.
   - Stop early when visuals meet the current quality bar, remaining work requires authored assets or design decisions, tests fail twice without new evidence, or the next change would be architectural.

## Stop Conditions

Stop before reaching `max_iterations` when any of these are true:

- The screenshot shows the targeted visual issue is fixed and remaining issues are minor.
- Remaining improvements require external assets, user design direction, or a new asset pipeline.
- Validation repeatedly fails for the same reason without new evidence.
- The next fix would touch unrelated systems or expand scope beyond visual quality.
- The repo is too dirty to safely edit the needed files without user direction.

## Reporting

Keep notes compact during the loop. In the final response, include:

- Iterations completed versus maximum.
- Screenshots or artifact paths reviewed.
- Visual issues found.
- Fixes implemented.
- Validation commands and results.
- Remaining visual risks or asset-pipeline gaps.
- Recommended next visual action.

## Quality Bar

For realism or professional polish requests, do not claim "fully realistic" when the project still uses placeholder/procedural assets. Say what improved and clearly separate code-based polish from asset-quality work that needs authored models, textures, lighting references, or animation assets.

