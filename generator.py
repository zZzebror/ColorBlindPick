import random
import colorsys
import json

HARMONY_TYPES = ["monochromatic", "analogous", "complementary", "split_complementary", "triadic", "tetradic"]

TECHNIQUES = [
    "Edge highlighting", "Dry brushing", "Glazing", "Wash shading", 
    "Wet blending", "Zenithal highlighting", "Non-metallic metal (NMM)"
]

TIPS = [
    "Avoid pure black shadows - mix purple or brown for richer depth",
    "Use desaturated colors for most of the model, high saturation for focal points",
    "Mix warm highlights with cool shadows for increased realism",
    "Apply the 60/30/10 rule: 60% dominant, 30% secondary, 10% accent",
    "Test your scheme on a spare model or palette first"
]

TRIVIA = [
    "Many award-winning pieces use strong complementary contrasts to guide viewer attention",
    "Analogous color schemes often mimic natural environments like forests or oceans",
    "Limited palettes (3-5 colors) prevent visual clutter on miniatures",
    "Modern competitions show increased use of bright colors including pastels",
    "Weathering effects help miniatures feel realistic and lived-in"
]

def hue_to_rgb(h, s=0.7, v=0.7):
    return colorsys.hsv_to_rgb(h, s, v)

def rgb_to_hex(r, g, b):
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def generate_palette(harmony_type, base_hue=None):
    if base_hue is None:
        base_hue = random.random()
    
    if harmony_type == "monochromatic":
        dominant = rgb_to_hex(*hue_to_rgb(base_hue, 0.7, 0.4))
        secondary = rgb_to_hex(*hue_to_rgb(base_hue, 0.5, 0.7))
        accent = [rgb_to_hex(*hue_to_rgb(base_hue, 0.9, 0.9))]
        
    elif harmony_type == "analogous":
        dominant = rgb_to_hex(*hue_to_rgb(base_hue, 0.75, 0.5))
        secondary = rgb_to_hex(*hue_to_rgb((base_hue + 0.083) % 1, 0.7, 0.7))
        accent = [rgb_to_hex(*hue_to_rgb((base_hue - 0.083) % 1, 0.85, 0.85))]
        
    elif harmony_type == "complementary":
        dominant = rgb_to_hex(*hue_to_rgb(base_hue, 0.75, 0.5))
        secondary = rgb_to_hex(*hue_to_rgb((base_hue + 0.5) % 1, 0.8, 0.7))
        accent = [rgb_to_hex(*hue_to_rgb(base_hue, 0.9, 0.9))]
        
    elif harmony_type == "split_complementary":
        dominant = rgb_to_hex(*hue_to_rgb(base_hue, 0.75, 0.5))
        secondary = rgb_to_hex(*hue_to_rgb((base_hue + 0.45) % 1, 0.75, 0.7))
        accent = [rgb_to_hex(*hue_to_rgb((base_hue + 0.55) % 1, 0.85, 0.85))]
        
    elif harmony_type == "triadic":
        dominant = rgb_to_hex(*hue_to_rgb(base_hue, 0.75, 0.5))
        secondary = rgb_to_hex(*hue_to_rgb((base_hue + 0.333) % 1, 0.75, 0.7))
        accent = [rgb_to_hex(*hue_to_rgb((base_hue + 0.666) % 1, 0.85, 0.85))]
        
    elif harmony_type == "tetradic":
        dominant = rgb_to_hex(*hue_to_rgb(base_hue, 0.75, 0.5))
        secondary = rgb_to_hex(*hue_to_rgb((base_hue + 0.25) % 1, 0.75, 0.7))
        accent = [
            rgb_to_hex(*hue_to_rgb((base_hue + 0.5) % 1, 0.85, 0.85)),
            rgb_to_hex(*hue_to_rgb((base_hue + 0.75) % 1, 0.8, 0.8))
        ]
    
    # Neutral skin tone - desaturated warm brown, high contrast
    neutral = rgb_to_hex(*hue_to_rgb(0.08, 0.4, 0.75))
    
    return {
        "dominant": dominant,
        "secondary": secondary,
        "accent": accent,
        "neutral": neutral
    }

def generate_scheme_name(harmony_type):
    prefixes = ["Ember", "Shadow", "Frost", "Storm", "Mystic", "Ancient", "Radiant", "Void", "Crimson", "Emerald"]
    suffixes = ["Sentinel", "Warrior", "Guardian", "Knight", "Mage", "Hunter", "Champion", "Warden", "Reaver", "Sage"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

def generate_color_theory(harmony_type):
    theories = {
        "monochromatic": "This scheme uses variations of a single hue with different saturations and values. Monochromatic schemes create unity and are excellent for focused, cohesive miniatures.",
        "analogous": "This scheme uses colors adjacent on the color wheel. Analogous palettes create natural harmony and are commonly used for nature-themed or organic models.",
        "complementary": "This scheme uses opposite colors on the color wheel, creating strong visual contrast. Complementary colors help focal points stand out and guide viewer attention.",
        "split_complementary": "This scheme uses a base color and two colors adjacent to its complement. It provides strong contrast while being more subtle than pure complementary schemes.",
        "triadic": "This scheme uses three colors evenly spaced on the color wheel. Triadic palettes offer vibrant contrast while maintaining color balance.",
        "tetradic": "This scheme uses two complementary pairs. It offers rich color variety but requires careful balance to avoid visual chaos."
    }
    return theories.get(harmony_type, "")

def generate_scheme(harmony_type=None):
    if harmony_type is None:
        harmony_type = random.choice(HARMONY_TYPES)
    
    palette = generate_palette(harmony_type)
    
    return {
        "scheme_name": generate_scheme_name(harmony_type),
        "harmony_type": harmony_type,
        "palette": palette,
        "color_theory": generate_color_theory(harmony_type),
        "painting_techniques": random.sample(TECHNIQUES, 3),
        "tips": random.sample(TIPS, 2),
        "trivia": random.choice(TRIVIA),
        "image_prompt": f"A stylized miniature silhouette showing armor in {palette['dominant']}, cloth in {palette['secondary']}, and weapon accents in {', '.join(palette['accent'])}"
    }

if __name__ == "__main__":
    scheme = generate_scheme()
    print(json.dumps(scheme, indent=2))
