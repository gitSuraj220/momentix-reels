# room.json schema

All sizes are in centimetres. Top-down view:

```
        N  (far wall, z = 0)
   ┌───────────────────────┐
 W │  x →                  │ E
   │  z ↓                  │
   └───────────────────────┘
        S  (near wall, z = depth)
```

```json
{
  "name": "Bedroom",
  "room": { "width": 380, "depth": 340, "height": 270, "confidence": "medium" },
  "walls": { "color": "#F1EEE8" },
  "floor": { "type": "wood", "color": "#B98A5E" },
  "wallNames": { "N": "window wall", "S": "door wall" },
  "openings": [
    { "wall": "N", "type": "window", "offset": 210, "width": 130, "height": 150, "sill": 85, "confidence": "medium" },
    { "wall": "S", "type": "door",   "offset": 280, "width": 80,  "height": 205, "confidence": "high" }
  ],
  "items": [
    { "id": "bed", "kind": "bed", "label": "Bed", "w": 160, "d": 205, "h": 50,
      "x": 130, "z": 103, "rot": 0, "color": "#C9B9A6", "confidence": "high" }
  ],
  "layouts": [
    { "name": "As it is now", "items": { "bed": { "x": 130, "z": 103, "rot": 0 } } }
  ],
  "notes": ["Room width worked out from the 80 cm door."]
}
```

| Field | What it is |
|---|---|
| `room.width` | length of walls N and S |
| `room.depth` | length of walls W and E |
| `floor.type` | `wood` (planks) or `plain` |
| `camera.hide` | which 2 walls are hidden at the start: `SE` (default, view from the door), `SW`, `NE`, `NW` |
| `wallNames` | optional: your own wall names shown in the interface |
| `openings[].offset` | for N and S, measured from the left wall W; for W and E, from the far wall N |
| `openings[].sill` | sill height (windows only) |
| `openings[].curtains` | curtains on the window (on by default; `false` removes them), `curtainColor` sets the colour |
| `items[].w / d / h` | width (along the back side) / depth (from the back side to the front) / height |
| `items[].x / z` | centre of the item's base |
| `items[].rot` | which wall the item's back faces: 0 → N, 90 → E, 180 → S, 270 → W. Only these 4 values. Flush to a wall: rot 0 → z = d/2; 180 → z = depth − d/2; 90 → x = width − d/2; 270 → x = d/2 |
| `items[].elevation` | height of the item's bottom above the floor, cm (shelf, wall TV, upper cabinets). Place it flush to a wall |
| `items[].fixed` | `true` means it can't be dragged. kitchen, radiator and anything with elevation are fixed by default |
| `items[].collide` | `false` means it doesn't block other items (rugs by default) |
| `confidence` | `high` / `medium` / `low`; in the sizes table, `low` is marked "re-measure" |
| `layouts` | 3 options; each gives new `x`, `z`, `rot` for the items |

`kind`: bed, sofa, armchair, wardrobe, dresser, nightstand, cabinet, desk, table, chair, tv, shelf, bookcase, plant, rug, lamp, kitchen, fridge, radiator, mirror, art (picture on the wall, with elevation), box (anything else; `other` = box).

`openings[].type`: `door` or `window`. A full-height balcony door is a `door`.

In every layout, list every item except the rug.
