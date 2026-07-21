# Official source map

Use these URLs as starting points. Navigate from the visible official system lists when a course sequence changes; do not guess replacements.

## Current route lists

- 湘南台駅西口: https://transfer-cloud.navitime.biz/kanachu/courses?busstop=00023860
- 慶応大学: https://transfer-cloud.navitime.biz/kanachu/courses?busstop=00023955
- 慶応大学本館前: https://transfer-cloud.navitime.biz/kanachu/courses?busstop=00023956
- 慶応中高等部前: https://transfer-cloud.navitime.biz/kanachu/courses?busstop=00023994

The absence of a return timetable at 慶応中高等部前 is relevant evidence, but confirm it from the current page during every audit.

## Outbound timetable starting points

- 湘19: https://transfer-cloud.navitime.biz/kanachu/courses/timetables?busstop=00023860&course-sequence=0008002325-1
- 湘23・湘24: https://transfer-cloud.navitime.biz/kanachu/courses/timetables?busstop=00023860&course-sequence=0008001376-1
- 湘25: https://transfer-cloud.navitime.biz/kanachu/courses/timetables?busstop=00023860&course-sequence=0008002337-1
- 湘28: https://transfer-cloud.navitime.biz/kanachu/courses/timetables?busstop=00023860&course-sequence=0008001373-1

## Return timetable starting points

- 慶応大学発、湘19・湘23・湘24および本館前発湘23の通過便を含む表:
  https://transfer-cloud.navitime.biz/kanachu/courses/timetables?busstop=00023955&course-sequence=0008001377-1
- 慶応大学本館前発 湘23:
  https://transfer-cloud.navitime.biz/kanachu/courses/timetables?busstop=00023956&course-sequence=0008002341-1
- 慶応大学発および本館前発の通過便を含む湘25表:
  https://transfer-cloud.navitime.biz/kanachu/courses/timetables?busstop=00023955&course-sequence=0008001370-1
- 慶応大学本館前発 湘25:
  https://transfer-cloud.navitime.biz/kanachu/courses/timetables?busstop=00023956&course-sequence=0008002338-1
- 慶応大学本館前発 湘28:
  https://transfer-cloud.navitime.biz/kanachu/courses/timetables?busstop=00023956&course-sequence=0008002340-1

## Route-detail cross-check

Use the official bus-location route page as supporting evidence when origin and destination are in question. The following example is the **outbound** 湘28 route and must not be mistaken for its return trip:

https://real.kanachu.jp/sp/DisplayRouteInfo?corpno=0&routeno=24084&rtripkbn=1&fromStopNo=24096&toStopNo=24250&routeName=%8F%C328&keikaName=&lastStopName=%8Cc%89%9E%92%86%8D%82%93%99%95%94%91O&fromStopRPS=1&toStopRPS=2

It shows 湘南台駅西口 → 慶応中高等部前. Verify the reverse direction from the return timetable and its 通過時刻表 rather than reversing this page by assumption.

## Filtering rules

The tables at 慶応大学 can mix buses that start there with buses that started at 慶応大学本館前 and pass through one minute later. Always open **系統別の選択** and isolate the option whose text contains the intended origin.

Examples of distinct option text include:

- `湘南台駅西口行 [...(慶応大学発)]`
- `湘南台駅西口行 [...(慶応大学本館前発)]`

When accessible labels contain only the route code and are duplicated, identify the checkbox by the adjacent full destination/origin text or its exact course-sequence ID obtained from the current DOM. Never select the first duplicate by position alone.
