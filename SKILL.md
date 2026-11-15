---
name: interactive-book-builder
description: Turn a school book or worksheet (PDF or page photos, one page or many) into an interactive flipbook: placed answers, animated science, geography motion graphics, live math graphs, offline HTML.
---

# Interactive Book Builder

Turns any school material — a whole PDF book, a few pages, or a single page photo — into a published interactive flipbook plus one offline HTML file. Worksheets get answers drawn in place; textbooks get their drawings replaced by animated, controllable versions.

Triggers: "حوّل الكتاب ده لكتاب تفاعلي", "اعمل البوكليت ده بنفس الطريقة", "اعمل إجابات للورق ده", "جرّب على صورة", "كتاب تفاعلي", "flipbook", or a PDF / page photo with a request to make it interactive.

Reference code lives in the skill repo (github: interactive-book-builder): `scripts/` (extract.py, image_to_page.py, imgtools.py, blocks.py, zones.py, build_offline.py), `templates/` (answers-flipbook.html, science-3d-flipbook.html, math-graphs-page.html, cover.html), `examples/` (two full worksheet answer specs). If the repo is available, start from it; otherwise rebuild from the rules below.

## 0. Before building — always
1. Read everything first: render every page and look at it, extract text with coordinates. Never guess content.
2. Decide the mode per page:
   - **Worksheet / question pages** → Answers mode (§3).
   - **Science** (physics, chemistry, biology) experiments, devices, processes, cycles → Animated experiment mode (§4).
   - **Geography** maps, mountains, deserts, rivers, coasts, climate → Motion graphics mode (§5).
   - **Maths** graphs, shapes, transformations → Live graph mode (§6).
   - **Already-answered pages** (teacher guide / answer key): no answers to add — animate the figures instead.
   - Photos, decorations, plain text → leave untouched.
3. Tell the user the plan in their language: page → figure/question type → what the student will do. Mention: no official answer key (you will solve, they review), broken/incomplete source questions, anything you cannot do.
4. More than ~6 pages: build a 3–4 page sample with varied types first, publish, wait for approval.

## 1. Input
### PDF
`scripts/extract.py book.pdf BOOK_DIR` → `img/p{n}.jpg` at 160 dpi + `all.json` (lines and blanks with boxes in PDF points). All overlay coordinates are PDF points; the overlay SVG uses `viewBox="0 0 595.32 841.92"`.
### Images (phone photos, scans, screenshots)
- Run `scripts/image_to_page.py in out.jpg`: finds the paper quad, warps it flat, auto-contrasts. Check the result visually; if no quad was found and the image is already clean (scan/screenshot), use it as is.
- Order multiple images by page number (filename or printed number) and confirm the order with the user if unclear.
- There is no text layer: coordinates are image pixels — set the overlay viewBox to the image size.
- Find text and blanks with OCR (`pytesseract.image_to_data`, 2× upscale, `-l ara+eng` when Arabic) and pixel analysis (`imgtools.hlines` for underline blanks; coloured-pixel row/column density for graph grids and axes).
- Tell the user honestly: accuracy and page sharpness depend on the photo; recommend a scanner app (Adobe Scan, Microsoft Lens, iPhone Notes) → PDF for best results.

## 2. Shell (one self-contained index.html)
- Calm gradient background; a distinct accent/cover colour per book (e.g. navy+gold, green+gold) so editions are told apart.
- Flipbook: two facing pages on wide screens, one on phones (`innerWidth<820 || aspect<1`). Cover is view 0 and the book opens on it. Single-page inputs → no flipping, just the page.
- Direction: Arabic books flip right-to-left, English/French left-to-right.
- Page flip: leaf of ~12 nested strips with rotateY, sin-curved bend and shading; drag (finish if >32% or a fast flick), arrows, keyboard.
- Zoom: pinch 1–4× anchored at the midpoint, one-finger pan when zoomed, double-tap in/out (must work even over a hotspot — cancel the single-tap action), Ctrl+wheel, toolbar button. Re-render hotspot canvases at higher resolution when zoomed.
- Lazy-load page images (current view ± 1).
- Toolbar: TOC + answer-key drawer, "All answers", Zoom. Bottom: prev / page label / next + "Show/Hide this page's answers" (acts on visible pages, syncs with single toggles).
- Teacher answer key tab: all answers per page, yellow ⚑ flags for anything needing a decision, headings jump to the page.
- Fonts: Cairo (UI), Caveat red for handwritten answers at ~1.4× nominal size. On canvas set `ctx.direction='ltr'` for maths/English labels (RTL pages otherwise flip "−6" to "6−"); wrap inline math in an LTR-isolated span.

## 3. Answers mode (worksheets)
Zones `{id,label,box,a:[elements],key,flag}`; elements are text on a blank (centred, auto-shrunk) or a hand-drawn red ellipse around the right option (animated stroke). Red tick button in the left margin per question; tapping the zone also toggles.
- MCQ: circle the option and write it in the gap.
- Rewrites: left-aligned on the answer line ~14pt. Crowded rule pages: ~11pt and one zone per row.
- Empty "Examples" columns: short model sentences, flagged.
- Reading: circle MCQs, T/F/NG on the dots, two-point answers at a fixed x inside the table.
- Writing: full model answer on the blank response pages + arrow note on the task page; flagged as a model.
- Never "correct" the source; flag broken questions and every place where more than one answer is acceptable.

## 4. Animated experiment mode (science)
- Measure each drawing's bounding box and verify it on a rendered image so the model hides the whole drawing and no text.
- In page: live animated version (three.js r160 via importmap from cdn.jsdelivr; one shared WebGL renderer drawing into per-hotspot canvases at ~30 fps) + "3D" badge placed where it covers no text.
- Tap → focus card rising from the page: orbit/zoom, tap a part for name + function quoted from the book with page number, labels toggle, "Book drawing" comparison, back to page.
- Lesson controls: temperature, speed, quantity, distance, switch, step-by-step, polarity, remove a part; live readouts + the formula. Derive behaviour from a simple physical model and check every sign against the book's rule. Values are relative — say so.
- "Test me": 4 tap-the-part questions with a score.
- Full 3D only where rotating helps (atoms, organs, molecules); shallow animated scenes for circuits/charge flow.

## 5. Motion graphics mode (geography)
Maps/landforms become animated scenes in place: rising relief, plains, valleys, drifting dunes with wind particles, flowing rivers, waves, slow camera move. Tap a region for its name from the book; layer toggles (relief, rivers, labels, climate); time/season sliders for change (erosion, dune movement, rainfall). Same focus card, book comparison and Test me.

## 6. Live graph mode (maths)
- Detect the graph's grid from pixels: grid-line columns/rows (coloured-pixel density), axis position from labels, unit = mean grid spacing. Build the in-page view so `X(x)=(x−x0)·unit` lands exactly on the original; redraw grid, ticks, labels and curves in the book's colours, clipped to the grid box.
- In page: animate the idea (draw the curve, reflect it about y = x, slide the parent function by h then k…) and end on the book's exact picture.
- Focus card: sliders for parameters (h, k, a, reflection progress, a moving point showing (a,b)↔(b,a)), presets for each sub-question, toggles (branches, y = x, domain/range shading, restrict domain), live equation + domain/range readout, tap parts (curve, vertex, start point, line, specific points) with the book's wording, Test me.
- Geometry shapes: sliders for dimensions with area/perimeter/volume and the formula updating live.
- Anything you add that is not in the book (e.g. the line y = x) is labelled "توضيح مضاف".

## 7. Cover
Render HTML (1323×1871) with Playwright → `img/p0.jpg` (templates/cover.html): school logo extracted from the source header, subject, grade tag, title, year, Arabic title line, "Interactive Edition" badge, Cairo. Different colour scheme per book/grade.

## 8. Test before delivering
Playwright + system Chrome (`--use-angle=swiftshader` for WebGL), CDN routed to local copies:
- Screenshot every spread with all answers shown and read them; fix overlaps, misplacement, crowding, reversed RTL numbers.
- Mobile 390×844 with real touch via CDP `Input.dispatchTouchEvent`: pinch, pan, double-tap, swipe flip, per-page button.
- Open every model/graph, move every control, run one quiz tap.
- Say the tests ran in an automated browser, not a real phone.

## 9. Deliver
- Publish the folder as an artifact; republish the same slug for updates.
- `scripts/build_offline.py`: images as base64, Cairo + Caveat inlined from `@fontsource/*`, three.js inlined if used; verify with the network disabled (no external requests, fonts loaded). Explain opening on PC, phone (WhatsApp/Teams/Files) and offline in class.
- Offer a student version without the answer key.
- Final message: what was built, counts, flagged items to review, and that answers were solved without an official key unless one was given.

## Gotchas
- Canvas `fillStyle` needs a CSS string — convert numeric hex colours.
- Base64 can contain "http" — strip data URIs before checking for external links.
- Keep the first view on the cover after resize (default page 0).
- Reset renderer size/scissor after closing a 3D focus view.
- Place badges and in-graph labels where they cover no book text or curves; on phones avoid labels under the readout box.
