# Format-specific verification

Use only the branch for the requested deliverable. This is original Agentit
guidance informed by [OpenAI's PDF skill](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/pdf/SKILL.md)
at the pinned Apache-2.0 revision. No upstream installers or helper scripts are
bundled; package license is retained in the third-party notices.

## PDF

Determine fixed-page dimensions, print/screen use, font embedding and whether
searchable text or accessible tags are required. Use the environment's existing
PDF authoring/rendering route. Render actual output pages to images or inspect
them in a supported viewer. Check clipping, substitution glyphs, text size,
table continuation, margins, page numbering and the final page. Extract text
separately to check expected headings/values and broken encoding.

A visually clean PDF can lack reading order, tags or selectable text. Report
which accessibility properties were checked rather than claiming compliance
from image review. Do not replace requested source/editable files with a PDF.

## Editable document

Use real paragraph styles, headings, list numbering, table cells and links.
Keep references and automatic fields consistent with the target editor. Avoid
spaces used as alignment and screenshots of text used as body content.
Open or render with the intended editor when available. Verify pagination,
tables across pages, font substitution, repeated headers, captions and links.
An export through a different office engine is evidence for that engine only.

Inspect hidden comments, tracked changes, author metadata and embedded objects
before distribution when the task calls for a clean final document. Preserve
review history when the user asked for an editable review draft.

## Spreadsheet

Define raw-input, calculation and presentation ranges. Keep numbers numeric,
dates meaningful and inputs visibly distinct. Use formulas for values that
must update; do not write a plausible cached total and claim recalculation.
Check formula results in a supported calculation engine where possible, plus
independent control totals from source data. Test blank input, duplicate keys,
division by zero, a changed input, filter/sort behavior and a realistic maximum
row count. Do not turn missing data into zero through a blanket error wrapper.

Check named ranges, chart ranges, locale number formatting, widths, frozen
headers, print areas and export. Treat formula injection in untrusted imported
strings as an input boundary; data starting with a formula introducer must not
silently become executable spreadsheet logic. No macros or external workbook
connections are required by this procedure.

## Slide deck

Establish aspect ratio and an editable content model. One slide should express
one reader-facing claim, supported by its visual/evidence. Keep charts linked
to the correct series and units; label mock data. Render the actual deck and
inspect all slides at presentation size and thumbnail scale. Check titles,
legends, small annotations, theme/font substitution, cropped images and transitions.

Exported images or a PDF preview can support appearance checks but do not prove
editable objects, speaker notes, animation behavior or presenter compatibility.
Reopen the deliverable and verify those properties when promised. Avoid shipping
a deck whose only useful source is the implementer's generation script.
