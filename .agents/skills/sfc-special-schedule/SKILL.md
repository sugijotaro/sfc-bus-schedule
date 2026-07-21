---
name: sfc-special-schedule
description: Create and verify date-specific special bus schedules in the sfc-bus-schedule repository from official announcements and timetable PDFs. Use when adding or correcting a special schedule, copying the applicable weekday, Saturday, or Sunday/holiday base service, changing terminals or routes, transcribing temporary buses, or validating route symbols, colors, directions, CSV files, YAML, and generated JSON.
---

# SFC Special Schedule

Create a special schedule without dropping unchanged regular service or confusing PDF colors with route symbols. Treat official announcement text, PDF headings, legends, and visible timetable marks as separate evidence.

## Start Safely

1. Confirm the worktree state. Preserve unrelated user changes.
2. Fetch the latest `main`, switch to it, and update it with a fast-forward-only pull.
3. Create and switch to a dedicated branch before editing any schedule files.
   - One date: `special-schedule/YYYYMMDD`
   - Multiple dates: `special-schedule/YYYYMMDD-YYYYMMDD`
   - Do not prepend `codex/`.
   - Follow an explicit user-provided branch name when given.
4. Never commit or push unless the user explicitly requests it.

If a same-purpose branch already exists, inspect it and continue there instead of creating a conflicting branch.

## Establish the Source of Truth

1. Locate the official announcement and every linked timetable PDF. Prefer the operator, university, or other primary publisher.
2. Preserve the announcement text requested by the user exactly unless correcting an obvious formatting artifact.
3. Record separately:
   - operation date;
   - publication date and description;
   - affected directions and route codes;
   - terminal, stop, and route changes;
   - cancellations or added service;
   - PDF legend meanings for colors, symbols, and marks.
4. Read the announcement and notes before transcribing times. They can change terminals or route interpretation for the whole day.
5. Render PDFs to high-resolution images and visually inspect them. Use text extraction only as an aid; never infer colors, symbol placement, columns, or route assignment from extracted text alone.

Ask the user before editing only when a primary source is unavailable, the applicable base service cannot be determined, the legend is unreadable, or official sources conflict materially.

## Select and Copy the Base Service

Determine the normal schedule that would apply on the target date before considering the special notice:

- `weekday`: ordinary weekday service;
- `saturday`: ordinary Saturday service;
- `sunday`: Sunday and holiday service in this repository.

Do not assume every special schedule starts from a holiday schedule. Use the calendar date, the repository's service categories, and the announcement together.

Create the new entry at the top of `config/special_schedules.yaml`:

- `date`: `YYYY-MM-DD`;
- `type`: `special_YYYYMMDD`;
- `description`: the approved announcement text;
- `routes`: a complete copy of all route paths that operate in the selected base service.

For every path in `config/routes.yaml` with a CSV for the selected base service:

1. Copy the route and path metadata into the special schedule.
2. Replace the day-type key under `csv_files` with `special_YYYYMMDD`.
3. Point unchanged paths to their existing regular CSV file.
4. Keep unchanged routes in the special schedule even when the announcement discusses only one or two routes.

After the full base is represented, apply the announced changes. Add a normally non-operating route only when the special notice introduces it. Remove or omit service only when the source explicitly indicates that it does not operate.

## Apply Route and Terminal Changes

For each affected path:

1. Update `name`, `origin`, `destination`, `via`, `sfc_direction`, stops, and cumulative times as required by the notice.
2. Create changed timetable files under `csv/special/` using `YYYYMMDD_<path-id>.csv`.
3. Keep repository direction semantics:
   - `to`: toward SFC;
   - `from`: away from SFC.
4. Determine the PDF's physical direction from its column heading and destination, not from left/right position alone.
5. Do not rename unaffected paths or duplicate unchanged CSV files without a reason.

## Transcribe Timetable PDFs

Process each direction independently.

1. Read every hour row and form the complete list of visible departure times for that direction.
2. Interpret each visual attribute independently:
   - color according to the color legend;
   - printed symbol according to the symbol legend;
   - no symbol according to the legend's unmarked entry;
   - footnotes according to their own note text.
3. A red time is an additional or temporary bus only when the legend says so. Red does not imply a route code.
4. Assign a time to a route only when its printed symbol or the unmarked legend rule says so.
5. For combined 湘23・湘25 tables:
   - an actual `ツ` printed above a time means 湘25;
   - an unmarked time means 湘23;
   - red means 臨時便 independently of whether `ツ` is present;
   - red without `ツ` remains 湘23;
   - red with `ツ` is 湘25.
6. Enter minutes in ascending order as space-separated two-digit values. Retain the repository's full hour-row format, including empty rows.

Do not treat OCR or PDF text-extraction placement as proof that a symbol belongs to a time. Confirm ambiguous marks on the rendered image.

## Verify Before Reporting Completion

Perform all checks below after editing:

1. Base coverage: compare the selected regular service against the special entry and account for every operating route/path.
2. Source coverage: for each PDF direction and hour, compare the union of all route CSV times with every visible PDF time.
3. Route partition: verify each time is assigned to the route indicated by its symbol or lack of symbol; check that no time appears in the wrong route because of color.
4. Direction: verify PDF headings against `origin`, `destination`, and `sfc_direction`.
5. Terminal and stops: verify announcement notes against path metadata and cumulative times.
6. CSV integrity: check valid hours and minutes, ascending order, expected zero padding, and no accidental duplicates.
7. YAML integrity: parse `config/special_schedules.yaml` and confirm `special_YYYYMMDD` keys and CSV paths exist.
8. Generate JSON with `python generate_json_v1.py`. If the environment lacks PyYAML, use an isolated virtual environment rather than modifying global Python.
9. Inspect `data/v1/special/special_YYYYMMDD/to_sfc.json`, `from_sfc.json`, and `data/v1/special_schedules.json` for route code, times, directions, terminals, and description.
10. Run `git diff --check` and review the complete diff. Do not stage unrelated files or ignored generated JSON.

State what was changed, what sources were checked, and what validation ran. If the user requests a commit, stage only the intended YAML and CSV files, recheck the staged diff, then commit with a concise date-specific message.
