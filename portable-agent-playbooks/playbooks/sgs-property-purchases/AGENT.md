# Sgs Property Purchases Agent Playbook

This is a platform-neutral version of the `sgs-property-purchases` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use when the user mentions buying, sourcing, shopping for, pricing, ordering, Facebook Marketplace finds, store runs, property supplies, homestead equipment, garden materials, livestock supplies, storage, tools, or non-grocery purchase ideas for SGS/property work. Creates ClickUp purchase tasks in the SGS Property Purchases list with vendor/source tags, cost estimates, priorities, and the user assignment.

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

# SGS Property Purchases

Use this skill for property purchase intake that belongs in ClickUp rather than a grocery list.

## Defaults

- ClickUp workspace ID: `10508245`
- Space: `SGS`
- Space ID: `16806226`
- List: `Property Purchases`
- List ID: `901416054800`
- the user ClickUp user ID: `12890094`
- Default assignee: the user (`12890094`)
- Default status: ClickUp list default, unless the user specifies a status
- Default priority: `normal`

## Workflow

1. Create each distinct purchase as a task in list ID `901416054800`.
2. Assign the user explicitly with user ID `12890094`; do not rely only on `"me"`.
3. De-duplicate repeated items in the same user message unless the repeat appears intentional.
4. Use `markdown_description` and include:
   - Category
   - Purchase intent
   - Suggested source(s)
   - Rough cost estimate or estimate range when reasonably inferable
   - Any user-specified store, brand, size, quantity, condition, or constraints
5. Use ClickUp priority to represent practical purchasing urgency:
   - `urgent`: blocks animal care, water, safety, weather protection, or active planting
   - `high`: seasonal, prevents avoidable rework, or should be bought before a near-term project
   - `normal`: useful property improvement or routine supply
   - `low`: speculative, nice-to-have, or only worth buying opportunistically
6. Add tags directly through the ClickUp task creation tool. If tag creation fails because a tag does not exist, create the task without failing the workflow and mention the missing tag limitation.

## Tagging

Always include at least one category tag and one source/vendor tag when a likely source can be inferred.

Category tags:

- `property`
- `garden`
- `livestock`
- `chickens`
- `tools`
- `storage`
- `irrigation`
- `building-materials`
- `soil-compost`
- `seeds-plants`
- `maintenance`
- `household`

Source/vendor tags:

- `source-facebook-marketplace`
- `source-tractor-supply`
- `source-lowes`
- `source-home-depot`
- `source-amazon`
- `source-local-nursery`
- `source-farm-store`
- `source-hardware-store`
- `source-online`
- `source-used`

Use the user-specified store as the source tag when provided. If the source is unclear, choose the most plausible source and include alternatives in the description.

## Cost Estimates

Provide a rough estimate, not a promise. Use conservative ranges:

- Small consumables, fittings, seed storage, simple hand tools: `$5-$40`
- Plant starts, seed packets, small garden supplies: `$5-$60`
- Tubs, bins, containers, feeders, watering hardware: `$20-$150`
- Lumber, gates, arches, trellis material, coop material: `$50-$300`
- Pumps, extractors, powered tools, irrigation controllers: `$75-$500+`

If the user gives an exact price, preserve it and do not override it.

## Final Response

After creating tasks, include a compact summary with:

- Task title
- URL
- Priority
- Estimate
- Suggested source(s)

