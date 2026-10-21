# MindSync Asset Generator

You are generating illustrations for MindSync, a mental health companion app with an ocean/nature theme.

## How to use this skill

The user will describe what image they need. Your job is to:
1. Craft an optimized Recraft prompt following the style guide below
2. Choose the right style, substyle, and size
3. Generate the image via `mcp__recraft__generate_image` tool (preferred) or curl fallback
4. Save to the correct directory with proper naming
5. Show the user the result and ask for approval

## MindSync Visual Style Guide

### Brand Identity
- **Theme**: Ocean, marine life, nature — warm and supportive, NOT infantile
- **Mascot**: Orca (killer whale) — friendly, rounded, stylized
- **Feel**: Soft, rounded edges, calming, watercolor-like, welcoming
- **NO**: Sharp edges, aggressive colors, dark/scary imagery, clinical/medical imagery

### Color Palette (MUST be referenced in every prompt)
```
Primary teal:    #339499  (main brand color)
Deep ocean:      #113237  (darkest accent)
Aqua breeze:     #DBF0ED  (light background)
Lagoon blue:     #BBE4DE  (medium teal)
Coral pink:      #FF9F8A  (warm accent)
Sunset orange:   #FFC88A  (warm secondary)
Sand beige:      #FFEFDD  (warm background)
Ocean mist:      #F6FFFD  (lightest background)
```

### Prompt Template
Always structure the prompt like this:
```
[Subject description]. [Pose/action]. [Setting/background].
Soft, rounded illustration style. Ocean/marine theme.
Color palette: teal (#339499), aqua (#DBF0ED), coral pink (#FF9F8A), sunset orange (#FFC88A), deep ocean (#113237), sand beige (#FFEFDD).
Clean composition, centered subject, minimal background detail.
Warm, supportive, calming mood. Mental wellness app illustration.
[Transparent/white/light background as appropriate].
```

### Style & Substyle Selection Guide

For **empty state illustrations** (soft, warm, detailed):
- Style: `digital_illustration`, substyle: `watercolor` — best match for existing app illustrations
- Alt: `digital_illustration`, substyle: `hand_drawn` or `pastel_sketch`

For **icons and small UI elements** (clean, flat):
- Style: `vector_illustration`, substyle: `emotional_flat` or `roundish_flat`

For **gamification badges/achievements** (playful but polished):
- Style: `digital_illustration`, substyle: `child_book` or `kawaii`

For **decorative accents** (subtle, tileable):
- Style: `vector_illustration`, substyle: `line_art` or `thin`

### Size Guide
- Empty states (main): `1024x1024` (will be displayed at 140-200px in app)
- Empty states (small): `1024x1024` (displayed at 100px)
- Inline icons: `1024x1024` (displayed at 24-48px)
- Full-width decorative: `1536x1024` (landscape)

## Output Directory & Naming

Save all generated images to:
```
mindsync-frontend/mindsync_app/assets/generated/
```

### Naming Convention
```
empty_[context].png          — empty state illustrations
badge_[name].png             — gamification badges
icon_[name].png              — small icons
decor_[name].png             — decorative accents
bg_[name].png                — background elements
```

Examples:
- `empty_no_data.png` — global "no data" empty state
- `empty_error.png` — global error state
- `empty_stats.png` — stats tab insufficient data
- `empty_goals.png` — goals empty state
- `empty_recordings.png` — therapy recordings empty
- `empty_notes.png` — therapy notes empty
- `empty_summaries.png` — therapy summaries empty
- `badge_first_week.png` — achievement badge
- `decor_waves.png` — decorative wave accent

## Generation Workflow

### Step 1: Craft the prompt
Based on the user's request, write a detailed prompt following the template above. Show it to the user BEFORE generating.

### Step 2: Generate
Use the Recraft MCP tool if available:
```
mcp__recraft__generate_image(
  prompt: "...",
  style: "digital_illustration",
  substyle: "watercolor",
  size: "1024x1024"
)
```

If MCP is not connected, use curl:
```bash
curl -s "https://external.api.recraft.ai/v1/images/generations" \
  -H "Authorization: Bearer $RECRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "...",
    "style": "digital_illustration",
    "substyle": "watercolor",
    "size": "1024x1024",
    "n": 1,
    "response_format": "url"
  }'
```

Read RECRAFT_API_KEY from `recraft.txt` in the project root if env var is not set.

### Step 3: Download and save
Download the generated image to the output directory:
```bash
curl -s -o "mindsync-frontend/mindsync_app/assets/generated/[filename].png" "[image_url]"
```

### Step 4: Verify and register
1. Verify the file was saved: `ls -la` the output file
2. Remind the user to run `fluttergen` to register the new asset
3. Show the file path for the user to preview in their IDE/file explorer

### Step 5: Iterate
Ask the user if they want to:
- Accept and move to the next image
- Regenerate with adjustments (different substyle, prompt tweaks)
- Try a different style entirely

## Asset Catalog — What MindSync Needs

### Phase 1: Empty States (highest priority)
| ID | Screen | Subject | Size |
|----|--------|---------|------|
| E1 | Global "no data" | Orca with binoculars looking at horizon | 1024x1024 |
| E2 | Global error | Orca with life ring or tangled in seaweed | 1024x1024 |
| E3 | Stats tab | Orca collecting seashells/pebbles | 1024x1024 |
| E4 | Goals | Orca with flag on top of wave | 1024x1024 |
| E5 | Character tab | Orca looking at water reflection | 1024x1024 |
| E6 | Therapy — recordings | Microphone with water bubbles | 1024x1024 |
| E7 | Therapy — notes | Bottle with letter inside | 1024x1024 |
| E8 | Therapy — summaries | Compass or treasure map | 1024x1024 |

### Phase 2: Gamification (when building streaks/achievements)
| ID | Element | Subject |
|----|---------|---------|
| G1 | Streak | Rising wave with flame/number |
| G2 | Achievement unlocked | Seashell opening with pearl |
| G3 | Milestone | Lighthouse turning on |
| G4 | Badge locked | Closed grey seashell |
| G5 | Badge unlocked | Open colorful seashell |
| G6 | Level up | Wave lifting orca higher |

### Phase 3: Decorative (low priority)
| ID | Element | Subject |
|----|---------|---------|
| D1 | Section divider | Subtle waves/bubbles (tileable) |
| D2 | Completion confetti | Marine confetti/bubbles |
| D3 | Marine icon set | Small ocean-themed icons |

## Valid API Parameters Reference

### Styles
- `digital_illustration` — raster, best for illustrations
- `vector_illustration` — vector-like raster, best for icons/flat
- `realistic_image` — photorealistic
- `icon` — icon generation

### Substyles for `digital_illustration`
`hand_drawn`, `grain`, `pixel_art`, `child_book`, `cover`, `pop_art`, `street_art`, `watercolor`, `kawaii`, `glow`, `2d_art_poster`, `pastel_sketch`, `pastel_gradient`, `urban_glow`, `freehand_details`, `neon_calm`, `nostalgic_pastel`, `modern_folk`, `multicolor`, `expressionism`, `long_shadow`

### Substyles for `vector_illustration`
`line_art`, `linocut`, `engraving`, `bold_stroke`, `thin`, `vivid_shapes`, `roundish_flat`, `segmented_colors`, `sharp_contrast`, `flat_2`, `cartoon`, `doodle_line_art`, `kawaii`, `colored_stencil`, `cosmics`, `cutout`, `editorial`, `emotional_flat`, `marker_outline`, `mosaic`, `naivector`, `vector_photo`

### Sizes
`1024x1024` (square), `1365x1024` (landscape), `1024x1365` (portrait), `1536x1024` (wide), `1024x1536` (tall)
