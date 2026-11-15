# AI Bubble — remaining Higgsfield images (sections 5–11)

For the Claude account that has Higgsfield. Sections 1–4 are done (`art/`, `art/index.json`).

## How to generate (same for every image)
- Model `gpt_image_2_6`, aspect `16:9`, count 1, `use_unlim: false`. Higgsfield runs max **4 jobs at once** (429 rate_limit otherwise): batches of 4, wait, next 4.
- References on EVERY image (role `image_references`), so the look and cast stay locked:
  - `ae415cbe-722b-48e0-8649-f91f36382004` (style frame)
  - `9139cd25-8816-4c49-8404-b5c9acba10e9` (character sheet)
- Start every prompt with this PREFIX:
  `Same cinematic 2.5D cartoon style and character design as the references (round white heads, dot eyes, expressive brows, bold black outlines, soft cel shading, warm key light + rim light, depth blur, film grain). Wide 16:9 shot:`
- End every prompt with: `No readable text, no logos, no watermark.` (logos/labels are added in code). Never draw a real person's likeness.
- Cast (from the character sheet): **Sam-type** = young exec in plain grey sweater; **Beta** = son in navy hoodie; **Papa** = moustache + round specs + cardigan; **boss** = bald, dark suit, red tie; **engineer** = green hoodie; **investor** = chubby, pinstripe suit, red tie, cigar; **board member/judge** = old, white hair, glasses, grey suit; **leather CEO** = black leather jacket + black tee; **woman exec** = blazer + bun; **intern** = small, calculator, lanyard.
- Download: results are on `d8j0ntlcm91z4.cloudfront.net` (container shell cannot reach it) → open one result URL in Chrome, `fetch()` each URL, blob-download to the Mac's Downloads as `aib_sNNN.png`, `device_stage_files`, copy to `projects/ai-bubble-long/art/sNNN.png`, add to `art/index.json`, commit + push (`ai-bubble:` prefix). Look at a contact sheet before committing; regenerate anything off-model.

## Prompts (file name → text after PREFIX)

### 5. GPU — naya sona
- s049: an empty electronics shop shelf with a hanging blank sign, a few flies buzzing, dust, sad shopkeeper behind the counter.
- s050: a giant brass balance scale in a museum hall; on one side a single glowing green computer chip (GPU card) heavily outweighs a gold bar and an oil barrel on the other side.
- s052: a concert-style tech stage with smoke and spotlights; the leather-jacket CEO holds a glowing chip like a guitar, crowd in front holding up phones (leave a blank badge area on his jacket for a label).
- s053: reverse angle of the same concert: excited crowd cheering, giant foam fingers, phone screens glowing, confetti.
- s060: a young founder in a hoodie fainting backwards onto the floor of a small office, papers flying (a huge bill counter will be added above him in code).
- s061: an underground bunker with metal shelves stacked with boxed GPUs next to rice/atta sacks and instant-noodle packets; the woman exec counts boxes with a clipboard.
- s062: a factory conveyor belt spitting out chips on the left, a frantic crowd of grabbing hands reaching from the right, chips vanishing faster than they appear.
- s064: a dark rainy alley at night, a shady man in a trench coat opens his coat to reveal it lined with GPU cards, neon reflections.
- s065: a border checkpoint at night with a barrier and floodlights; a vegetable truck with GPU cards peeking out from under cabbages, a guard with a torch.

### 6. Sab kuch "AI-powered"
- s067: a kitchen toaster with a blank sticker area pops out two pitch-black smoking toast slices, the Beta character coughing and waving smoke.
- s069: a supermarket self-checkout counter with an old security camera on top, shoppers scanning items, fluorescent light.
- s070: same self-checkout, a bored worker sticks a brand-new shiny label onto the same old camera (label blank).
- s071: a rooftop party of executives at night, disco lights, glowing balloons, city skyline.
- s072: same rooftop party: champagne bottle popping in the foreground, a printer spitting cheques into the air like confetti.
- s073: same rooftop party frozen mid-dance, everyone stopped with awkward faces, one balloon drifting.
- s074: same rooftop party: the small intern with a calculator raises his hand in a single spotlight, everyone turns to stare at him.

### 7. Bill ki baat
- s076: the chubby investor in his office clutching his chest in shock, staring at a phone, sweat drops, a blood-pressure meter on the desk.
- s082: a leather wallet with little wings flying out of an office window, banknotes trailing behind it in the wind.
- s084: a vast glowing data-centre city at night seen from above, endless server buildings, cooling towers with steam, power lines (huge counter added in code; leave the sky area clear).
- s091: a boardroom: the old board member with glasses holds a thick report; the Sam-type exec in grey sweater stands at a whiteboard with a marker (whiteboard blank).
- s092: same boardroom, closer on Sam proudly drawing a line going straight up on the whiteboard (line can be drawn in code; keep the board clean).
- s095: same boardroom, Sam flipping wall-calendar pages faster and faster, pages flying, nervous smile.
- s097: same boardroom, Sam shrugging with a big carefree smile, palms up.
- s098: three doors behind the board member: a modern glass corporate door, a golden desert-palace door, and an old man in a cap with rose-tinted glasses peeking from a plain door (door signs blank).
- s099: Sam winking with finger-guns, confident grin, boardroom background.
- s102: a casino roulette wheel with 10 slots on a green table, investors in suits eagerly pushing chip stacks onto it.

### 8. Gadbadiyan
- s104: a cute robot with spiral hypnotised eyes and a halo of little stars circling its head.
- s105: the same robot in sunglasses presenting a slide of nonsense scribbles to an audience, chest puffed out.
- s107: a lawyer in a suit opens a case file in a courtroom and finds every page blank, confused face.
- s108: a flying saucer at night beaming a glowing chart down to earth through a tractor beam.
- s109: a pizza kitchen: a chef happily pours a bottle of white glue over a cheese pizza.
- s111: a courtroom: close-up of a judge's wooden gavel slamming down, impact lines.
- s112: an angry crowd of writers, painters and journalists holding pens, brushes, microphones and blank protest signs in front of a shiny tech office.
- s113: a robot company spokesperson at a podium sweating heavily, tiny embarrassed expression.
- s115: a courtroom entrance: writers dragging a robot by the leg up the steps, artists dragging another robot behind them.
- s116: a courtroom: a confident robot lawyer in a suit at the defence table, judge's bench behind.
- s117: same courtroom: the woman exec as an artist (paint-stained apron) points angrily out of the window at a truck being loaded with boxes (truck side blank).
- s118: same courtroom: the robot lawyer slowly sinking low into his chair, embarrassed.
- s121: a dark bedroom at 3 AM, a sleeping investor in bed, a mosquito circling his ear with a dotted flight path, bedside clock glowing.

### 9. Phoota kyun nahi?
- s125: a giant suit trouser pocket filling the frame, endless banknotes pouring down into it from above.
- s126: a sepia 1999 dot-com office with rows of foosball tables, bean bags, employees playing, an empty revenue whiteboard.
- s127: four shiny skyscrapers in a futuristic city with money pouring out of their windows like waterfalls (building tops blank for logos).
- s128: the woman exec in a supermarket casually lifting a small globe-shaped country out of a shopping cart.
- s131: a phone in a hand showing the same meme twice (chat app then social feed), coins dropping around it.
- s133: executives in suits running a race on a track, all looking back over their shoulders nervously.
- s135: a city skyline swiping from day to night and becoming futuristic (hover cars, glowing towers) in a single wide shot.
- s136: an executive standing in front of a huge falling red chart; other executives backing away from him (his sign blank).
- s137: a smoky poker table under a single lamp: four players in suits with blank round heads (logos added in code), towering chip stacks in front of each.
- s139: extreme close-up row of unblinking eyes across the poker table, chips being pushed to a growing pile in the middle.

### 10. Kab phootega?
- s141: a hand pulling a curtain off a stage set, revealing flimsy cardboard props held up by sticks.
- s145: a big brass money tap squeaking shut, the last single coin dripping from it.
- s148: an executive tightening a belt (belt label blank) around his waist; behind him an air hose to a giant balloon kinks.
- s150: a crowd in a dark hall watching a giant screen, all mouths open in shock, screen glow on faces.
- s152: a tall office tower at dusk, an employee walking out with a cardboard box of belongings, rain.
- s153: crypto coins falling off a table, a cracked blank sign on the wall.
- s154a: a giant red report sheet towering over a tiny shocked team.
- s154b: a launch stage where a robot facepalms while the audience stares.
- s154c: a court officer pasting a big red STOP order on the door of a data centre (order text blank).

### 11. Abhi hum kahan hain?
- s161: the smoky poker table: one player slowly lays his cards face down and leans back, others stare.
- s162: a huge shiny balloon drifting above a city skyline at dusk, tethered by a thin rope.
- s164: close-up of a character taking a deep breath, eyes wide, holding it, tense lighting.
- s165: two hands pulling a rope tight, the last few threads in the middle snapping.

When all are in, mark `HF images (≈70) | A | done` in HANDOFF.md STATUS.
