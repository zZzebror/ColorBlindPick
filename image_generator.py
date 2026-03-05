import requests
from PIL import Image
from io import BytesIO
import time

def generate_scheme_image(scheme, output_path="scheme.png"):
    palette = scheme['palette']
    
    # Build prompt for miniature model
    prompt = f"""tabletop miniature figure, fantasy warrior, {palette['dominant']} armor, {palette['secondary']} cloth cape, {palette['accent'][0]} weapon, painted miniature, studio photo, white background"""
    
    # Try multiple free APIs
    apis = [
        {
            "url": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
            "headers": {},
            "payload": {"inputs": prompt}
        },
        {
            "url": f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=512&height=512",
            "method": "GET"
        }
    ]
    
    for api in apis:
        try:
            if api.get("method") == "GET":
                response = requests.get(api["url"], timeout=30)
            else:
                response = requests.post(api["url"], headers=api.get("headers", {}), json=api.get("payload"), timeout=30)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.save(output_path)
                return output_path
        except Exception as e:
            continue
    
    # Fallback: create simple visualization
    return create_fallback_image(scheme, output_path)

def generate_all_models(scheme):
    """Generate three different model types with consistent material placement"""
    paths = []
    for model_type in ['elf', 'ork', 'human']:
        path = f"scheme_{model_type}.png"
        create_model_image(scheme, model_type, path)
        paths.append(path)
    return paths

def create_model_image(scheme, model_type, output_path):
    from PIL import ImageDraw
    
    width, height = 512, 512
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    palette = scheme['palette']
    
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    def shade(color, factor=0.4):
        return tuple(int(c * factor) for c in color)
    
    def highlight(color, factor=1.7):
        return tuple(min(255, int(c * factor)) for c in color)
    
    # Material assignment based on miniature painting conventions:
    # Armor (dominant) - torso, legs, pauldrons
    # Cloth (secondary) - cape, undergarments, sash
    # Skin (neutral) - face, hands
    # Weapon (accent) - sword, bow, axe
    
    armor = hex_to_rgb(palette['dominant'])
    cloth = hex_to_rgb(palette['secondary'])
    weapon = hex_to_rgb(palette['accent'][0])
    skin = hex_to_rgb(palette['neutral'])
    
    if model_type == 'elf':
        draw_elf(draw, armor, cloth, weapon, skin, shade, highlight)
    elif model_type == 'ork':
        draw_ork(draw, armor, cloth, weapon, skin, shade, highlight)
    else:  # human
        draw_human(draw, armor, cloth, weapon, skin, shade, highlight)
    
    img.save(output_path)
    return output_path

def draw_elf(draw, armor, cloth, weapon, skin, shade, highlight):
    """Tall and lithe elf - light armor, flowing cloth"""
    # Head/face - skin
    draw.ellipse([226, 60, 286, 140], fill=skin, outline='black', width=2)
    draw.ellipse([230, 65, 266, 110], fill=highlight(skin), outline=None)
    draw.ellipse([270, 100, 282, 136], fill=shade(skin), outline=None)
    
    # Torso - light armor
    draw.rectangle([216, 140, 296, 320], fill=armor, outline='black', width=2)
    draw.rectangle([220, 145, 256, 315], fill=highlight(armor), outline=None)
    draw.rectangle([270, 145, 292, 315], fill=shade(armor), outline=None)
    
    # Arms - cloth sleeves
    draw.rectangle([186, 160, 216, 300], fill=cloth, outline='black', width=2)
    draw.rectangle([296, 160, 326, 300], fill=cloth, outline='black', width=2)
    draw.rectangle([190, 165, 210, 295], fill=highlight(cloth), outline=None)
    
    # Hands - skin
    draw.ellipse([186, 290, 216, 320], fill=skin, outline='black', width=2)
    draw.ellipse([296, 290, 326, 320], fill=skin, outline='black', width=2)
    
    # Legs - light armor
    draw.rectangle([226, 320, 251, 480], fill=armor, outline='black', width=2)
    draw.rectangle([261, 320, 286, 480], fill=armor, outline='black', width=2)
    draw.rectangle([230, 325, 245, 475], fill=highlight(armor), outline=None)
    draw.rectangle([265, 325, 280, 475], fill=highlight(armor), outline=None)
    
    # Cape - cloth
    draw.polygon([216, 150, 176, 170, 176, 360, 216, 320], fill=cloth, outline='black', width=2)
    draw.polygon([216, 160, 190, 175, 190, 340, 216, 310], fill=highlight(cloth), outline=None)
    
    # Weapon - bow
    draw.arc([330, 180, 370, 280], 270, 90, fill=weapon, width=4)
    draw.line([350, 200, 350, 260], fill=weapon, width=2)
    
    # Base - neutral
    draw.ellipse([196, 480, 316, 505], fill=(100, 80, 60), outline='black', width=2)

def draw_ork(draw, armor, cloth, weapon, skin, shade, highlight):
    """Burly ork - medium armor, exposed skin, practical cloth"""
    # Head/face - skin (green-ish tint)
    draw.rectangle([206, 80, 306, 160], fill=skin, outline='black', width=2)
    draw.rectangle([210, 85, 256, 155], fill=highlight(skin), outline=None)
    draw.rectangle([270, 85, 302, 155], fill=shade(skin), outline=None)
    
    # Torso - armor plates
    draw.rectangle([166, 160, 346, 340], fill=armor, outline='black', width=2)
    draw.rectangle([170, 165, 256, 335], fill=highlight(armor), outline=None)
    draw.rectangle([280, 165, 342, 335], fill=shade(armor), outline=None)
    
    # Left arm - exposed skin
    draw.rectangle([116, 180, 166, 320], fill=skin, outline='black', width=2)
    draw.rectangle([120, 185, 150, 315], fill=highlight(skin), outline=None)
    draw.rectangle([155, 185, 162, 315], fill=shade(skin), outline=None)
    
    # Right arm - exposed skin
    draw.rectangle([346, 180, 396, 320], fill=skin, outline='black', width=2)
    draw.rectangle([350, 185, 380, 315], fill=highlight(skin), outline=None)
    
    # Cloth belt/sash
    draw.rectangle([166, 280, 346, 310], fill=cloth, outline='black', width=2)
    
    # Legs - armor
    draw.rectangle([186, 340, 246, 460], fill=armor, outline='black', width=2)
    draw.rectangle([266, 340, 326, 460], fill=armor, outline='black', width=2)
    draw.rectangle([190, 345, 220, 455], fill=highlight(armor), outline=None)
    draw.rectangle([270, 345, 300, 455], fill=highlight(armor), outline=None)
    
    # Weapon - large axe
    draw.rectangle([396, 200, 416, 300], fill=weapon, outline='black', width=3)
    draw.rectangle([398, 205, 403, 295], fill=highlight(weapon, 2.2), outline=None)
    draw.rectangle([408, 205, 414, 295], fill=shade(weapon, 0.3), outline=None)
    draw.polygon([396, 180, 446, 180, 446, 220, 396, 200], fill=weapon, outline='black', width=2)
    
    # Base
    draw.ellipse([146, 460, 366, 495], fill=(100, 80, 60), outline='black', width=2)

def draw_human(draw, armor, cloth, weapon, skin, shade, highlight):
    """Heavily armored human knight - maximum armor coverage"""
    # Helmet - armor (face mostly covered)
    draw.rectangle([211, 70, 301, 150], fill=armor, outline='black', width=2)
    draw.rectangle([215, 75, 256, 145], fill=highlight(armor, 2.0), outline=None)
    draw.rectangle([275, 75, 297, 145], fill=shade(armor, 0.3), outline=None)
    
    # Visor slit - hint of skin
    draw.rectangle([231, 100, 281, 110], fill=shade(skin, 0.3), outline=None)
    
    # Torso - heavy plate armor
    draw.rectangle([181, 150, 331, 340], fill=armor, outline='black', width=2)
    draw.rectangle([185, 155, 256, 335], fill=highlight(armor, 2.0), outline=None)
    draw.rectangle([280, 155, 327, 335], fill=shade(armor, 0.3), outline=None)
    draw.line([256, 160, 256, 330], fill=shade(armor, 0.25), width=3)
    
    # Pauldrons - armor
    draw.ellipse([151, 150, 211, 200], fill=armor, outline='black', width=2)
    draw.ellipse([301, 150, 361, 200], fill=armor, outline='black', width=2)
    draw.ellipse([155, 155, 195, 185], fill=highlight(armor, 2.0), outline=None)
    
    # Arms - armored
    draw.rectangle([141, 200, 181, 320], fill=armor, outline='black', width=2)
    draw.rectangle([331, 200, 371, 320], fill=armor, outline='black', width=2)
    draw.rectangle([145, 205, 165, 315], fill=highlight(armor, 2.0), outline=None)
    
    # Gauntlets - armor (hands covered)
    draw.rectangle([141, 310, 181, 340], fill=armor, outline='black', width=2)
    draw.rectangle([331, 310, 371, 340], fill=armor, outline='black', width=2)
    
    # Legs - heavy armor
    draw.rectangle([196, 340, 251, 470], fill=armor, outline='black', width=2)
    draw.rectangle([261, 340, 316, 470], fill=armor, outline='black', width=2)
    draw.rectangle([200, 345, 225, 465], fill=highlight(armor, 2.0), outline=None)
    draw.rectangle([265, 345, 290, 465], fill=highlight(armor, 2.0), outline=None)
    
    # Shield - cloth heraldry on armor base
    draw.ellipse([101, 220, 161, 320], fill=armor, outline='black', width=3)
    draw.ellipse([115, 240, 147, 300], fill=cloth, outline=None)
    
    # Sword - weapon
    draw.rectangle([371, 200, 386, 360], fill=weapon, outline='black', width=2)
    draw.rectangle([373, 205, 378, 355], fill=highlight(weapon, 2.2), outline=None)
    draw.polygon([361, 190, 396, 190, 378, 200], fill=weapon, outline='black', width=2)
    
    # Cape - cloth
    draw.polygon([181, 170, 131, 190, 131, 380, 181, 340], fill=cloth, outline='black', width=2)
    draw.polygon([181, 180, 145, 195, 145, 360, 181, 330], fill=highlight(cloth), outline=None)
    draw.polygon([155, 210, 135, 220, 135, 370, 155, 360], fill=shade(cloth), outline=None)
    
    # Base
    draw.ellipse([156, 470, 356, 500], fill=(100, 80, 60), outline='black', width=2)

def create_fallback_image(scheme, output_path):
    """Legacy single image - now creates human by default"""
    return create_model_image(scheme, 'human', output_path)
