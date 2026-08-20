---
name: artifact-template-sgs-refined-proposal-microsite
description: "Create a Site using the SGS Refined Proposal Microsite template and its retained source directory. Use when the user selects this template, names SGS Refined Proposal Microsite, or explicitly invokes $artifact-template-sgs-refined-proposal-microsite. Create client proposal microsites with the refined SGS layout: front-loaded value, icon-led cards, three pacing options, a highlighted recommendation, and responsive mobile behavior."
---

# SGS Refined Proposal Microsite

Create a Site from this template. Keep the source directory unchanged.

## Workflow

1. Read `artifact-template.json` and resolve its paths relative to this skill directory.
2. Load [@Sites](plugin://sites@openai-bundled) and copy the retained source directory into a new working directory.
3. Adapt the existing application to the user's request without replacing its source with a newly scaffolded project.
4. Preserve logical D1/R2 bindings and create a new Site project instead of reusing the original project.
5. Build, deploy, and verify the new Site through the existing Sites workflow.

## Fidelity

Preserve the source application's pages, components, styles, assets, package configuration, migrations, and logical D1/R2 bindings.

User instructions control requested content and explicit deviations. The retained reference controls layout and formatting where the user has not requested a change.
