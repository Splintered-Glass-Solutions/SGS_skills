# Research notes

Observed 2026-11-11; sources are general design guidance, not evidence of a particular product's requirements.

- [GOV.UK notification banner](https://design-system.service.gov.uk/components/notification-banner/): use banners sparingly; put information directly relevant to the current task in the page content. Implication: repeated prominent notices can compete with the task.
- [Atlassian warning messages](https://atlassian.design/content/designing-messages/writing-a-warning-message): warnings address meaningful potential consequences before an action; avoid repeating the title and offer concise advice. Implication: keep actionable, consequential warnings and trim redundant copy.
- [W3C WAI form notifications](https://www.w3.org/WAI/tutorials/forms/notifications/): provide clear success and error feedback, with specific recovery information close to the relevant controls and accessible notification where needed. Implication: removing clutter must not remove feedback or screen-reader support.
- [Nielsen Norman Group usability heuristics](https://media.nngroup.com/media/articles/attachments/Heuristic_Summary_A4_compressed.pdf): irrelevant information competes with relevant information, while system status and error recovery remain important. Implication: judge copy by its role in the task, not by length alone.

The distinction between development-facing copy and decision-relevant disclosure is an application of these principles. Test-mode indicators and data caveats require context: removal can mislead users when the distinction affects real decisions.
