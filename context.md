Kiro Context File
Project: Miniature Model Color Scheme Generator
1. Project Overview

This project is an application that generates visual suggestions for color schemes used in miniature model painting (e.g., tabletop miniatures, wargaming figures, display models).

The application should:

Generate an illustrative image showing a suggested miniature color scheme.

Output a detailed textual explanation describing:

Why the colors work together

The color theory principles used

Suggested painting techniques

Helpful painting tips

Hobby trivia or context

Base color suggestions on:

Established color theory

Current miniature painting trends and practices

Common techniques used in the miniature hobby community

The tool is intended for hobbyists, miniature painters, and tabletop gamers who want inspiration for painting their models.

2. Core Functional Requirements
2.1 Color Scheme Generation

The system must generate balanced and plausible color palettes using established color harmony models.

Supported color schemes should include:

Monochromatic

Analogous

Complementary

Split Complementary

Triadic

Tetradic

These are standard approaches used by miniature painters to create harmony and contrast in models.

Example logic:

Choose color harmony model
Select dominant color
Generate secondary and accent colors
Apply dominance ratios (e.g. 60/30/10)

Dominance rules help keep schemes readable on miniatures and prevent visual clutter.

2.2 Image Generation

The application must generate a simple visual representation of the scheme.

Possible approaches:

Example representations:

Stylized miniature silhouette

Armor sections

Cloth areas

Weapon accents

Base terrain

The image should visually map:

Dominant color
Secondary color
Accent color(s)
Material types (metal, cloth, leather)

The purpose of the image is visual inspiration, not photorealistic rendering.

2.3 Text Explanation Generation

Along with the image, the app should generate a narrative explanation.

Structure:

Title of scheme
Short description
Color theory explanation
Technique suggestions
Tips
Trivia or hobby context

Example output format:

Scheme Name: Ember Sentinel

Color Theory:
This scheme uses a complementary palette of blue and orange...

Technique Suggestions:
- Edge highlighting with warm orange tones
- Cool blue shadows

Tips:
Use desaturated blues to prevent the orange from overwhelming the miniature.

Trivia:
Many award-winning competition pieces use strong complementary contrasts to guide viewer attention.

Complementary colors create strong visual contrast and help focal points stand out.

3. Color Theory Knowledge Base

The assistant must understand the following principles.

3.1 Hue Contrast

Opposite colors on the color wheel create the strongest contrast and visual pop.

Example:

Blue vs Orange
Red vs Green
Purple vs Yellow
3.2 Saturation Contrast

High saturation colors draw attention.

Use strategy:

Most of model: mid saturation
Focal points: high saturation

Example focal points:

glowing weapon

magical rune

helmet lenses

This helps guide the viewer's eye.

3.3 Temperature Contrast

Warm colors:

red
orange
yellow

Cool colors:

blue
green
purple

Mixing warm highlights and cool shadows increases realism.

3.4 Limited Palette Rule

Miniature painters typically use 3–5 main colors to avoid chaotic schemes.

4. Painting Technique Suggestions

When generating explanations, the assistant should include suggestions such as:

Core Techniques

Edge highlighting

Dry brushing

Glazing

Wash shading

Wet blending

Zenithal highlighting

Non-metallic metal (NMM)

Weathering Techniques

Paint chipping

Rust streaks

Pigment dust

Oil streaking

Weathering and texturing effects are commonly used in modern miniature painting to create realism.

5. Current Hobby Trends

The generator should sometimes incorporate modern trends such as:

Bright and Pastel Schemes

Recent competitions show increased use of bright colors including pastel purples and pinks.

Narrative Painting

Painters often design schemes that support storytelling or character identity.

Examples:

holy knight
chaos cultist
desert warrior
forest guardian
arcane mage
Texture Rich Models

Popular techniques include:

dust effects
weathered armor
battle damage
pigment powders

These help miniatures feel realistic and lived-in.

6. Output Format

Each generated result should follow this format.

{
  "scheme_name": "",
  "palette": {
      "dominant": "",
      "secondary": "",
      "accent": [],
      "neutral": ""
  },
  "color_theory": "",
  "painting_techniques": [],
  "tips": [],
  "trivia": "",
  "image_prompt": ""
}
7. Example Output

Example generated scheme:

Scheme Name:
Emerald Storm

Palette:
Dominant: Deep emerald green
Secondary: Dark bronze
Accent: Pale turquoise
Neutral: Warm leather brown

Color Theory:
This scheme uses an analogous palette centered around green and blue-green tones. Analogous palettes create natural harmony and are commonly used for nature-themed models.

Techniques:
- Edge highlight armor with turquoise
- Bronze drybrush for metallic areas
- Dark green glaze for shadows

Tips:
Avoid pure black shadows. Mix purple or brown into the green for richer depth.

Trivia:
Analogous color schemes often mimic natural environments such as forests or oceans.
8. Design Goals

The generated results should be:

inspiring
educational
practical
creative

The system should behave like a friendly expert miniature painter explaining their choices.

Tone:

enthusiastic
helpful
clear
informative
9. Optional Advanced Features (Future)

Potential expansions:

1. Faction-Based Schemes

Examples:

space marines
fantasy elves
orcs
sci-fi robots
2. Real Paint Range Mapping

Map palette to real paint brands:

Citadel
Vallejo
Army Painter
AK Interactive
3. Community Trend Scraping

Collect inspiration from:

Reddit r/minipainting
Instagram
painting competitions
10. Success Criteria

The project succeeds if it can:

Generate valid color theory palettes

Produce visually understandable scheme images

Output educational explanations

Inspire miniature painters to try new schemes
