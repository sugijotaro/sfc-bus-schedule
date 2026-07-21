---
name: sfc-timetable-audit
description: Audit the current regular SFC bus schedules for 湘19, 湘23, 湘24, 湘25, and 湘28 against Kanachu's official NAVITIME timetable and bus-route pages. Use when checking whether regular CSV times and route metadata are current, investigating a timetable discrepancy, or preparing for a regular timetable correction after a service change. This skill excludes special schedules and future/revised schedules that are not yet effective.
---

# SFC Regular Timetable Audit

Audit only the currently effective regular timetable. Tell the user at the start and in the final report that special schedules are not included.

## Guardrails

- Limit the audit to 湘19, 湘23, 湘24, 湘25, and 湘28.
- If `config/routes.yaml` contains another SFC route, stop and tell the user to update this skill before auditing that route.
- Check only the timetable marked current by the official site. Do not incorporate a linked future revision.
- If a future revision is advertised, mention its effective date as a caveat without auditing or editing it.
- Treat `config/special_schedules.yaml`, `csv/special/`, and generated special JSON as out of scope.
- Report discrepancies and a concrete correction proposal. Do not edit files, commit, push, or open a PR until the user explicitly chooses what to do.
- Preserve 湘19往路 as an SFC-scoped API path ending at 慶応大学 even though the physical bus continues to 綾瀬車庫. This is the only approved metadata exception.

## Prepare

1. Confirm the worktree state without changing branches or files.
2. Read `config/routes.yaml` and every regular CSV referenced by its `csv_files` entries.
3. Read [references/official-sources.md](references/official-sources.md) completely before browsing.
4. Run `python3 .agents/skills/sfc-timetable-audit/scripts/validate_regular.py` for local structural checks.
5. Use the browser to access the official pages. Do not replace the live-page check with search snippets, cached pages, or guessed URLs.

## Browse the Official Timetables

1. Open the 湘南台駅西口 system list and confirm the displayed “現在” date.
2. Open each outbound timetable from the official system list.
3. Open the 慶応大学 and 慶応大学本館前 system lists for return service.
4. On every timetable containing multiple services, open **系統別の選択**.
5. Leave exactly one service/origin selected at a time. Use the full destination text to distinguish identical route labels.
6. Record each hour and minute independently for 平日, 土曜, and 休日.
7. Open at least one **通過時刻表** for every distinct path to verify:
   - actual departure stop;
   - destination;
   - stop order;
   - travel-time offsets relevant to `cumulative_time`.
8. Treat the route heading, selected option text, trip detail, and stop sequence as separate evidence. When they conflict, prefer the trip detail for the actual origin and stop order, and report the conflict.

For return trips, never merge these campus origins:

- 慶応大学
- 慶応大学本館前
- 慶応中高等部前

An arrival at a campus stop does not prove that return service departs there.

## Compare with the Repository

Compare all referenced regular CSV files, not only the route that prompted the audit.

For each route, direction, origin, and day type:

1. Compare the complete ordered list of official departures with its CSV.
2. Report missing and extra departures as `HH:MM`.
3. Verify `origin` equals the first API stop and `destination` equals the last API stop, except for the approved 湘19往路 scope rule.
4. Verify `name`, `via`, `sfc_direction`, stop order, and cumulative times against official trip details.
5. Check minutes are zero-padded, sorted, in `00..59`, and not duplicated.
6. Distinguish a departure-time error from a metadata error.

Do not compare a timetable shown only under a future “改正” link with the current CSV.

## Report and Stop

State clearly that the result covers **regular schedules only**.

Report:

- official “現在” date;
- official pages checked;
- number of regular CSV files checked;
- exact matching areas;
- every discrepancy, including route, direction, actual origin, day type, and time;
- proposed file-level correction;
- any advertised future revision date;
- confirmation that special schedules were not checked.

Then ask the user whether to apply the proposed corrections. Make no repository changes before their answer.
