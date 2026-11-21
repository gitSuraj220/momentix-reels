---
name: room-from-photos
description: "Turn 2-4 phone photos of a real room into an interactive 3D dollhouse (one HTML file, Three.js): estimated sizes with confidence, draggable furniture, wall colours, 3 layouts, a will-it-fit check and a top-down plan. Use when the user sends room photos and wants a 3D model or plan of their room, to rearrange furniture, repaint walls, or check whether a sofa, bed or wardrobe fits. Also: 'mere kamre ka 3D bana do', 'sofa fit hoga kya'."
---

# Room from Photos (English edition)

Room photos → a 3D dollhouse in the browser. Drag furniture, repaint walls, compare 3 layouts, check "will it fit?", and see a table of every size Claude estimated.

The skill's files sit next to this SKILL.md. Below, `<SKILL>` means this folder.

**Language:** reply in the language the user writes in (English, Hindi, Hinglish or any other). Labels inside room.json (`name`, `label`, layout names, `notes`, `wallNames`) also go in the user's language, written in Latin script if they write Hinglish.

## 1. Photos
- Best is 2 photos: the first from the doorway, the second from the opposite corner. Extra photos of each wall help.
- **Wall N is the wall facing the camera in the first photo.** The others: W on the left, E on the right, S behind (usually the door wall the photo was taken from).
- If the user knows even one real size, ask for it. One true size makes everything else more accurate. If they say "the room is 3 m wide", that is the length of wall N unless they say otherwise. Sizes in feet or inches: convert to cm (1 ft = 30.5 cm, 1 in = 2.54 cm).
- Only one photo, or a poor one: build it anyway. Anything you can't see gets `confidence: "low"` and a line in `notes` saying it was a blind guess.

## 2. Sizes: work from objects of known size
- interior door 80 × 200 cm (front door 90 × 205), handle ~100 cm from the floor;
- power socket ~30 cm from the floor (in India often 25–30 cm, or at switchboard height ~120 cm), light switch 90–120 cm, window sill 80–90 cm;
- table 75 cm high, chair and sofa seat 42–46 cm;
- bed widths 90/120/150/180 × 190–200 cm (Indian single, double, queen, king); floor tiles 30/60/60×120 cm; laminate plank ~20 cm wide;
- ceiling in an apartment 250–300 cm.
Cross-check 2–3 references against each other. Round to 5 cm. `confidence`: `high` means the reference is close by and the object is fully visible; `medium` is the usual; `low` means a bad angle, the object is hidden, or it's a guess.

## 3. room.json
Full schema: `<SKILL>/references/schema.md`. The essentials:

**Axes.** Everything is in centimetres. `x` runs from the left wall W to the right, `z` from the far wall N towards the near wall S. An item's `x`, `z` is the **centre** of its base.

**Rotation `rot`** is the wall the item's **back** faces (bed headboard, back of a sofa or chair, back panel of a wardrobe, back edge of a desk): `0` → N, `90` → E, `180` → S, `270` → W. The front (seat, doors, screen) faces the opposite way. A chair at a desk has its back away from the desk. Rug, plant and floor lamp: `rot: 0`. Only 0, 90, 180, 270.

**Width and depth.** `w` runs along the back side, `d` from the back side to the front. Flush to a wall:
- `rot 0` → `z = d/2`; `rot 180` → `z = depth − d/2`;
- `rot 90` → `x = width − d/2`; `rot 270` → `x = d/2`.
With `rot 90/270`, the item takes up `d` along x and `w` along z.

**Built-in and wall-mounted.** Kitchen (`kitchen`) and radiator (`radiator`) are fixed and can't be dragged. Shelf, wall TV and upper cabinets get `elevation` (height of their bottom above the floor, cm) and sit flush to a wall. A rug doesn't block anything.

**kind:** bed, sofa, armchair, wardrobe, dresser, nightstand, cabinet, desk, table, chair, tv, shelf, bookcase, plant, rug, lamp, kitchen, fridge, radiator, mirror, box (anything else).

**Colours** of furniture, floor and walls come from the photos (`color`, hex).

**Layouts `layouts`.** 3 options, the first is "As it is now". In each, list **every** item (except the rug) with `x`, `z`, `rot`. Rules: items don't overlap or cross the walls, 80 cm in front of the door stays clear, walkways are at least 60 cm, the bed's headboard is against a wall. If the room is a weak guess (`room.confidence: "low"`), 1–2 layouts are enough.

## 4. Build
```bash
python3 <SKILL>/scripts/build.py room.json -o my-room.html
```
- "Error": the build stopped; fix room.json.
- "Warning": overlaps, furniture in the door swing, an item outside a wall. Fix and build again until there are no warnings.
The output is one HTML file (~570 KB) that works offline. Give the file to the user.

## 5. Reply to the user
Short, in their language:
1. How to use it: drag furniture with the mouse or a finger, R rotates, "Top-down plan", wall colours (all walls or one), layouts, "Will it fit?".
2. The sizes table, and what to check with a tape measure first (everything marked `low`).
3. "Tell me one real size and I'll recalculate everything more accurately."

## Changes on request
- "Rearrange the furniture so that…": change `layouts` / `x z rot` and rebuild.
- "Paint the wall…": `walls.color`, or point them to the "One wall" button.
- "Will a 220 × 95 sofa fit?": the file has a "Will it fit?" button. To work it out yourself: the free stretch along a wall at the item's depth, minus the door zone (a square the width of the door), minus windows if the item is taller than the sill, minus radiators.

## Honest about accuracy
Sizes from photos are approximate, with a 5–15% error. Use a tape measure before buying furniture.

---
English edition by Momentix, based on room-from-photos by Stas Rise (MIT licence, see LICENSE).
