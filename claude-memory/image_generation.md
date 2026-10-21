# Image Generation Recipe (Recraft AI)

## Winning Formula
- **API**: Recraft AI (`https://external.api.recraft.ai/v1/images/generations`)
- **API Key**: stored in `recraft.txt` in project root
- **Style**: `icon` (simplest output — 2-3 paths, ~2KB SVG)
- **Color control**: Use `controls.colors` to force exact brand palette
- **Output format**: SVG (vector_illustration/icon styles always return SVG)
- **Save as**: `.svg` extension (NOT .png/.webp — those corrupt SVG files)
- **Flutter**: Use `SvgPicture.asset()` from `flutter_svg` (already in project)

## Brand Color Palette for `controls.colors`
```json
"controls": {
  "colors": [
    {"rgb": [17, 50, 55]},      // #113237 — dark teal (primary shapes)
    {"rgb": [219, 240, 237]},    // #DBF0ED — mint (backgrounds/circles)
    {"rgb": [255, 159, 138]},    // #FF9F8A — coral pink (warm accent, optional)
    {"rgb": [51, 148, 153]}      // #339499 — primary teal (optional)
  ]
}
```
Use 2 colors for ultra-minimal, 3-4 for images needing accent.

## API Call Template
```bash
curl -s "https://external.api.recraft.ai/v1/images/generations" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "...",
    "style": "icon",
    "size": "1024x1024",
    "n": 1,
    "response_format": "url",
    "controls": {
      "colors": [
        {"rgb": [17, 50, 55]},
        {"rgb": [219, 240, 237]}
      ]
    }
  }'
```

## Key Learnings
- `vector_illustration` style also returns SVG but more complex (20+ colors, many paths)
- `digital_illustration` returns WebP raster — not what we want
- `icon` style produces the simplest SVGs (~2KB, 2-3 paths)
- Claude's Read tool CANNOT preview SVG files (only jpeg/png/gif/webp)
- On Windows: no Cairo/ImageMagick/Inkscape available for SVG→PNG conversion
- Recraft ignores color hints in prompts — MUST use `controls.colors` API parameter

## Output Directory
```
mindsync-frontend/mindsync_app/assets/generated/
```

## Naming Convention
```
empty_[context].svg     — empty state illustrations
badge_[name].svg        — gamification badges
gamification_[name].svg — gamification illustrations
decor_[name].svg        — decorative accents
```

## Style Match
Matches OnBoarding images: flat silhouettes, solid fills, 2-3 colors, minimal shapes, maximum negative space.
