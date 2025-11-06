# Study Plan Generator

`study_plan_gen.py` is a lightweight command-line helper that turns a topic, time frame, and experience level into a Markdown study plan stored in `plans/`. Every plan includes clear weekly headings, actionable bullet points, resource placeholders, and guidance on how to reuse the curriculum in 2026.

## Quick Start

```bash
python3 study_plan_gen.py --topic "Anatomy Basics"
```

This creates `plans/anatomy-basics.md` (the script automatically creates `plans/` if needed).

## CLI Arguments

| Flag | Required | Description |
| --- | --- | --- |
| `--topic` | Yes | Subject you want to study (used for the title and slug). |
| `--weeks` | No (default `4`) | Number of weeks the plan should cover. |
| `--level` | No (default `beginner`) | Choose `beginner` or `intermediate` to change tone and tasks. |

## Weekly Template

Each week in the Markdown output looks like this:

```
### Week N
- Primary task pulled from the level-specific template.
- Reflection task that nudges you to document wins, blockers, or open questions.
```

You can personalize the structure by editing the lists in `study_plan_gen.py`:

- Update `actions_for_level` to rewrite the main weekly tasks per experience level.
- Edit the `reflection_prompts` list inside `generate_weekly_section` to adjust the supporting bullet.
- Add more statements to either list; the generator automatically cycles through them for longer plans.

## Customizing the Templates

All of the content templates live in `study_plan_gen.py`:

- Weekly tasks are generated inside `actions_for_level`. Add or adjust entries to change the tone per level.
- Resource links are defined in `resources_section`; update the placeholder URLs with your real sources or pull in localized material.
- The “How to use in 2026” checklist is the `how_to_use` block inside `generate_markdown`.
- Any new variables you add will flow into the Markdown by adjusting `generate_markdown`.

Because everything uses plain Python lists and f-strings, you can easily tailor vocabulary or add new experience levels.

## Example Commands

- Nursing students ramping up on pharmacology:
  ```bash
  python3 study_plan_gen.py --topic "Nursing Pharmacology" --weeks 6 --level beginner
  ```
- Developers planning a deep dive into distributed systems:
  ```bash
  python3 study_plan_gen.py --topic "Distributed Systems Architecture" --weeks 8 --level intermediate
  ```
- Student leaders onboarding classmates to GitHub workflows:
  ```bash
  python3 study_plan_gen.py --topic "GitHub for Students – onboarding" --weeks 5 --level beginner
  ```

## Example Plans in `plans/`

- `plans/anatomy-basics.md` showcases a foundational health sciences study track.
- `plans/github-for-students-onboarding.md` can be handed to student clubs that need a 2026-ready onboarding kit.
- `plans/example.md` mirrors the default output so you can tweak formatting without re-running the CLI.

## How to Contribute

- Open an issue describing the feature or bug you want to tackle (template ideas, better resources, linting, etc.).
- Fork the repo, create a topic branch, and submit a pull request that highlights the CLI flag/behavior you touched.
- Wherever possible, include a generated plan in `plans/` that demonstrates your change so future students can preview it.

## Roadmap for 2026

- Add advanced/accelerated templates for career switchers who already know the basics.
- Bake in YAML/JSON exports so the plans can plug into campus LMS tooling.
- Ship curated resource presets (videos, labs, checklists) for common tracks like nursing, cybersecurity, and open-source onboarding.
- Automate PR checks that run the CLI against sample topics to guarantee formatting stays consistent year over year.
