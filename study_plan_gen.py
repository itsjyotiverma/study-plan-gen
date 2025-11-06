#!/usr/bin/env python3
"""Simple study plan generator CLI."""

import argparse
import os
import textwrap


def parse_args():
    parser = argparse.ArgumentParser(
        prog="study-plan-gen",
        description="Create a week-by-week study plan Markdown file.",
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Main subject of the study plan (e.g., Anatomy Basics).",
    )
    parser.add_argument(
        "--weeks",
        type=int,
        default=4,
        help="Number of weeks to cover. Defaults to 4.",
    )
    parser.add_argument(
        "--level",
        choices=("beginner", "intermediate"),
        default="beginner",
        help="Experience level to shape the plan tone.",
    )
    return parser.parse_args()


def validate_args(args):
    topic = (args.topic or "").strip()
    if not topic:
        raise ValueError("Please provide a non-empty --topic value.")
    if args.weeks < 1:
        raise ValueError("The --weeks value must be a positive integer.")
    args.topic = topic
    return args


def slugify(text):
    normalized = []
    for char in text.lower():
        if char.isalnum():
            normalized.append(char)
        elif char.isspace():
            normalized.append(" ")
        else:
            normalized.append(" ")
    collapsed = "-".join("".join(normalized).split())
    return collapsed or "study-plan"


def actions_for_level(level):
    if level == "intermediate":
        return [
            "Audit your current {topic} workflow and log specific gaps.",
            "Rebuild a complex example or dataset tied to {topic} insights.",
            "Ship a public artifact (blog, demo, briefing) teaching part of {topic}.",
            "Stress-test mastery via timed drills, peer reviews, or mock scenarios.",
        ]
    return [
        "Clarify learning goals for {topic} and gather foundational glossaries.",
        "Follow curated primers or videos covering {topic} essentials.",
        "Apply the basics in a small project or reflection journal tied to {topic}.",
        "Review questions that surfaced and revisit weak spots with spaced repetition.",
    ]


def generate_weekly_section(topic, weeks, level):
    templates = actions_for_level(level)
    reflection_prompts = [
        "Summarize breakthroughs and pain points for {topic} in your log.",
        "Share a short update or loom explaining what you practiced for {topic}.",
        "List the open questions you still have about {topic} and schedule follow-ups.",
    ]
    lines = []
    for index in range(weeks):
        template = templates[index % len(templates)]
        reflection = reflection_prompts[index % len(reflection_prompts)]
        lines.append(
            textwrap.dedent(
                f"""\
                ### Week {index + 1}
                - {template.format(topic=topic)}
                - {reflection.format(topic=topic)}
                """
            ).strip()
        )
    return "\n\n".join(lines)


def resources_section(slug):
    links = [
        ("Kickoff guide", f"https://example.com/{slug}/kickoff"),
        ("Practice drills", f"https://example.com/{slug}/drills"),
        ("Community forum", f"https://example.com/{slug}/community"),
    ]
    return "\n".join(f"- [{label}]({url})" for label, url in links)


def generate_markdown(topic, weeks, level):
    slug = slugify(topic)
    description = {
        "beginner": f"Structured ramp-up plan to go from zero to confident in {topic}.",
        "intermediate": f"Focused roadmap to sharpen and showcase existing {topic} skills.",
    }[level]
    weekly = generate_weekly_section(topic, weeks, level)
    resources = resources_section(slug)
    how_to_use = textwrap.dedent(
        """\
        - Anchor this plan to your 2026 milestones or certification deadlines.
        - Reserve weekly retros to adapt scope as new tools or policies emerge.
        - Archive insights in a living doc so 2026 teammates can reuse the playbook.
        """
    ).strip()
    return textwrap.dedent(
        f"""# Study Plan: {topic}

{description}

## Weekly Focus

{weekly}

## Resources

{resources}

## How to use in 2026

{how_to_use}
"""
    ).strip()


def main():
    args = parse_args()
    try:
        args = validate_args(args)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 1

    base_dir = os.path.dirname(os.path.abspath(__file__))
    plans_dir = os.path.join(base_dir, "plans")
    os.makedirs(plans_dir, exist_ok=True)

    slug = slugify(args.topic)
    markdown = generate_markdown(args.topic, args.weeks, args.level)
    output_path = os.path.join(plans_dir, f"{slug}.md")

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(markdown + "\n")

    print(f"Study plan created: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
