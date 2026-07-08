# Sgs Personal Todo Agent Playbook

This is a platform-neutral version of the `sgs-personal-todo` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use when the user lists personal, home, garden, orchard, chicken, cleanup, maintenance, seasonal planting, harvesting, or property to-do items that should become ClickUp tasks in the SGS Personal list. Applies practical priorities, due dates, categorization tags, dependency notes, and the user assignment.

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

# SGS Personal To-Do

Use this skill for personal/home/property task intake into ClickUp.

## Defaults

- ClickUp workspace ID: `10508245`
- Space: `SGS`
- Space ID: `16806226`
- List: `Personal`
- List ID: `901416054721`
- the user ClickUp user ID: `12890094`
- Default assignee: the user (`12890094`)
- Default status: ClickUp list default, unless the user specifies a status
- Default priority: infer from urgency; fall back to `normal`

## Workflow

1. Create each distinct to-do as a task in list ID `901416054721`.
2. Assign the user explicitly with user ID `12890094`; do not rely only on `"me"`.
3. De-duplicate repeated items in the same user message unless the repeat appears intentional.
4. Split nested items into separate tasks when they have different timing, dependencies, locations, or completion criteria.
5. Use `markdown_description` and include:
   - Category
   - Location
   - Original intent or important wording
   - Due-date reasoning when a date is inferred
   - Dependencies, planting constraints, or "do not plant yet" style cautions
   - Tags
6. Add one location tag and one or more work/category tags. Use ClickUp tags directly through task creation. If a tag is unavailable, create the task without failing and mention the limitation.

## Priority Heuristics

- `urgent`: live plant/animal welfare, drying out, active weather risk, imminent seasonal window, or task blocks several next steps
- `high`: seasonal garden work, chicken infrastructure, irrigation, harvest timing, or tasks that should happen before summer heat
- `normal`: organization, research, nonblocking prep, storage, sourcing, or flexible improvements
- `low`: nice-to-have, opportunistic, or speculative cleanup

## Due Dates

Use exact dates. Convert relative dates using the user's locale/timezone from context.

Due dates are work-by prompts unless the user explicitly says a date is a true deadline. For personal/home/property planning, a due date means "try to have this handled or at least actively scheduled by this date."

When assigning or rebalancing dates:

- Prioritize seasonality, animal/plant welfare, safety, utilities, dependencies, and weather windows over old dates.
- Use weekend-heavy dates for hands-on property work.
- Use weekdays for calls, quotes, ordering, research, and design.
- Assume a sustainable load of roughly 5-8 personal/property tasks per week unless the user says otherwise.
- For backlog batches, give every task a work-by date spread across quarters instead of leaving tasks undated.
- For large projects, date the next action or planning milestone unless the user gives a real completion deadline.

For Central US spring/summer gardening when the user does not provide a city or USDA zone:

- Warm-season planting after frost: early to late May
- Corn first block: early May if soil is warming
- Corn succession: about 2 weeks after the first block
- Watermelon and warm herbs: by late May
- Yard-long beans: after supports/companion crops establish, but preferably by late June
- Orchard companion planting: prep early May, amend mid-May, plant by late May
- Irrigation or plant-watering setup: earlier than planting dates, especially for container plants
- Chicken ventilation and feed systems: before summer heat and daily chore pressure increase

Make the date conservative and explain the reasoning in the task description.

## Tagging

Use one `loc-*` tag for where the task physically happens. Keep location separate from the work/category tags so later filtering is clean.

Location tags:

- `loc-barn`: barn, barn drawers, barn corners, barn-adjacent work
- `loc-garden`: general garden beds, shade garden, south barn bed, berry bed, magnolia bed, tea grove unless a more specific location applies
- `loc-house`: house exterior, porch, general house tasks
- `loc-house-interior`: inside the house, interior rooms, indoor storage, indoor drawers/cabinets
- `loc-ranch`: broader property/ranch work that is not tied to a named garden, barn, orchard, chicken, court, or greenhouse area
- `loc-pickleball-courts`: pickleball courts and court-adjacent work
- `loc-chickens`: coop, run, chicken feed/water, chicken-specific infrastructure
- `loc-orchard`: orchard trees, Orchard A, fruit trees, orchard guilds
- `loc-greenhouse`: greenhouse, greenhouse staging, seed-starting area if located there

Use a small set of practical work/category tags, adding specific ones when useful:

- `home`
- `garden`
- `orchard`
- `planting`
- `harvest`
- `cleanup`
- `maintenance`
- `irrigation`
- `chickens`
- `livestock`
- `storage`
- `research`
- `seasonal`
- `dependency`
- `companion-planting`
- `bed-prep`
- `tools`

Prefer tags that will help with later filtering by context, location, and work mode.

## Custom Fields

Do not use unrelated existing fields such as `Team` or `Epic` for property locations. If a real ClickUp `Location` custom field becomes available and its field ID/options are known, use it in addition to the `loc-*` tag. Until then, `loc-*` tags are the source of truth for location grouping.

## Privacy

This skill can place tasks in the `Personal` list and assign the user. It cannot guarantee ClickUp list-level privacy unless the available ClickUp tools expose permission controls. If privacy matters and the list is inside a shared space, mention that the list may inherit SGS space visibility.

## Final Response

After creating tasks, include a compact summary with:

- Number of tasks created
- Important de-duplication or task-splitting decisions
- Any inferred dates or assumptions that matter
- Privacy caveat when relevant

