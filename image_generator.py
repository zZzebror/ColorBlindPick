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
    
    def edge_highlight(color, factor=2.3):
        """Extreme highlight for edges where light catches"""
        return tuple(min(255, int(c * factor)) for c in color)
    
    def nmm_dark(color):
        """NMM darkest shadow - nearly black for metal"""
        return tuple(int(c * 0.15) for c in color)
    
    def nmm_bright(color):
        """NMM brightest highlight - near white for metal reflection"""
        return tuple(min(255, int(c * 2.8)) for c in color)
    
    # Material assignment based on miniature painting conventions:
    # Armor (dominant) - torso, legs, pauldrons - NMM effect
    # Cloth (secondary) - cape, undergarments, sash
    # Skin (neutral) - face, hands
    # Weapon (accent) - sword, bow, axe - NMM effect
    
    armor = hex_to_rgb(palette['dominant'])
    cloth = hex_to_rgb(palette['secondary'])
    weapon = hex_to_rgb(palette['accent'][0])
    skin = hex_to_rgb(palette['neutral'])
    
    if model_type == 'elf':
        draw_elf(draw, armor, cloth, weapon, skin, shade, highlight, edge_highlight, nmm_dark, nmm_bright)
    elif model_type == 'ork':
        draw_ork(draw, armor, cloth, weapon, skin, shade, highlight, edge_highlight, nmm_dark, nmm_bright)
    else:  # human
        draw_human(draw, armor, cloth, weapon, skin, shade, highlight, edge_highlight, nmm_dark, nmm_bright)
    
    img.save(output_path)
    return output_path

def draw_elf(draw, armor, cloth, weapon, skin, shade, highlight, edge_highlight, nmm_dark, nmm_bright):
    """Tall and lithe elf - dynamic bow-drawing pose"""
    # Head - turned, aiming
    draw.ellipse([240, 80, 290, 140], fill=skin, outline='black', width=2)
    draw.ellipse([244, 85, 275, 120], fill=highlight(skin), outline=None)
    draw.ellipse([278, 110, 286, 136], fill=shade(skin), outline=None)
    
    # Torso - twisted, leaning back with NMM armor
    points = [256, 140, 286, 140, 306, 240, 296, 320, 236, 320, 226, 240]
    draw.polygon(points, fill=armor, outline='black', width=2)
    draw.polygon([260, 145, 282, 145, 295, 240, 260, 240], fill=nmm_bright(armor), outline=None)
    draw.polygon([285, 180, 302, 240, 290, 240], fill=nmm_dark(armor), outline=None)
    draw.line([256, 140, 286, 140], fill=nmm_bright(armor), width=2)
    
    # Left arm - extended forward (bow hand)
    draw.polygon([226, 160, 156, 200, 156, 230, 226, 210], fill=cloth, outline='black', width=2)
    draw.polygon([220, 165, 170, 195, 170, 215, 220, 200], fill=highlight(cloth), outline=None)
    draw.line([226, 160, 156, 200], fill=edge_highlight(cloth), width=2)
    # Hand
    draw.ellipse([136, 200, 166, 240], fill=skin, outline='black', width=2)
    
    # Right arm - pulled back (drawing string)
    draw.polygon([286, 160, 346, 140, 356, 170, 296, 190], fill=cloth, outline='black', width=2)
    draw.polygon([290, 165, 340, 145, 345, 165, 295, 180], fill=highlight(cloth), outline=None)
    # Hand
    draw.ellipse([336, 130, 366, 170], fill=skin, outline='black', width=2)
    
    # Legs - wide stance with NMM armor
    # Front leg bent
    draw.polygon([236, 320, 216, 420, 226, 480, 256, 480, 266, 400], fill=armor, outline='black', width=2)
    draw.polygon([240, 325, 230, 400, 240, 475], fill=nmm_bright(armor), outline=None)
    draw.polygon([250, 380, 262, 400, 258, 475], fill=nmm_dark(armor), outline=None)
    # Back leg extended
    draw.polygon([266, 320, 306, 420, 316, 470, 286, 470, 276, 400], fill=armor, outline='black', width=2)
    draw.polygon([270, 325, 300, 400, 300, 465], fill=nmm_bright(armor), outline=None)
    
    # Cape - flowing
    draw.polygon([226, 150, 186, 170, 176, 340, 226, 320], fill=cloth, outline='black', width=2)
    draw.polygon([220, 160, 190, 175, 190, 320, 220, 310], fill=highlight(cloth), outline=None)
    draw.line([226, 150, 186, 170], fill=edge_highlight(cloth), width=2)
    
    # Bow - held forward with NMM
    draw.arc([120, 180, 180, 300], 270, 90, fill=weapon, width=5)
    draw.line([150, 200, 350, 150], fill=weapon, width=2)  # String
    draw.arc([122, 182, 178, 298], 270, 90, fill=nmm_bright(weapon), width=2)
    
    # Base
    draw.ellipse([186, 480, 326, 505], fill=(100, 80, 60), outline='black', width=2)

def draw_ork(draw, armor, cloth, weapon, skin, shade, highlight, edge_highlight, nmm_dark, nmm_bright):
    """Burly ork - aggressive charging pose with raised axe"""
    # Head - forward, roaring
    draw.rectangle([226, 100, 306, 180], fill=skin, outline='black', width=2)
    draw.rectangle([230, 105, 276, 175], fill=highlight(skin), outline=None)
    draw.rectangle([285, 105, 302, 175], fill=shade(skin), outline=None)
    
    # Torso - leaning forward, charging with NMM armor
    points = [186, 180, 346, 180, 356, 280, 336, 360, 196, 360, 176, 280]
    draw.polygon(points, fill=armor, outline='black', width=2)
    draw.polygon([190, 185, 276, 185, 286, 280, 276, 355], fill=nmm_bright(armor), outline=None)
    draw.polygon([300, 185, 352, 185, 352, 280, 332, 355], fill=nmm_dark(armor), outline=None)
    draw.line([186, 180, 346, 180], fill=nmm_bright(armor), width=3)
    draw.line([186, 180, 176, 280], fill=nmm_bright(armor), width=2)
    draw.line([276, 185, 276, 355], fill=nmm_bright(armor), width=2)
    
    # Left arm - raised high with axe
    draw.polygon([186, 200, 156, 100, 176, 80, 206, 180], fill=skin, outline='black', width=2)
    draw.polygon([190, 190, 165, 110, 175, 95, 200, 175], fill=highlight(skin), outline=None)
    draw.polygon([180, 150, 160, 100, 165, 95], fill=shade(skin), outline=None)
    
    # Right arm - extended forward, pointing
    draw.polygon([346, 220, 416, 260, 416, 290, 346, 250], fill=skin, outline='black', width=2)
    draw.polygon([350, 225, 410, 265, 410, 280, 350, 245], fill=highlight(skin), outline=None)
    
    # Cloth belt/sash
    draw.rectangle([186, 300, 346, 330], fill=cloth, outline='black', width=2)
    draw.line([186, 300, 346, 300], fill=edge_highlight(cloth), width=2)
    
    # Legs - wide power stance with NMM armor
    # Front leg bent, weight forward
    draw.polygon([196, 360, 176, 450, 186, 490, 226, 490, 246, 440], fill=armor, outline='black', width=2)
    draw.polygon([200, 365, 190, 440, 200, 485], fill=nmm_bright(armor), outline=None)
    draw.polygon([220, 420, 242, 440, 238, 485], fill=nmm_dark(armor), outline=None)
    draw.line([196, 360, 246, 360], fill=nmm_bright(armor), width=2)
    
    # Back leg extended
    draw.polygon([286, 360, 316, 450, 326, 480, 296, 480, 276, 440], fill=armor, outline='black', width=2)
    draw.polygon([290, 365, 310, 440, 310, 475], fill=nmm_bright(armor), outline=None)
    draw.polygon([305, 420, 322, 450, 318, 475], fill=nmm_dark(armor), outline=None)
    draw.line([286, 360, 316, 360], fill=nmm_bright(armor), width=2)
    
    # Weapon - massive axe raised overhead with NMM
    draw.rectangle([146, 60, 166, 120], fill=weapon, outline='black', width=3)
    draw.rectangle([148, 65, 153, 115], fill=nmm_bright(weapon), outline=None)
    draw.rectangle([158, 65, 164, 115], fill=nmm_dark(weapon), outline=None)
    # Axe head
    draw.polygon([126, 40, 186, 40, 186, 80, 146, 70, 126, 80], fill=weapon, outline='black', width=2)
    draw.polygon([130, 45, 170, 45, 170, 70, 150, 65], fill=nmm_bright(weapon), outline=None)
    draw.line([126, 40, 186, 40], fill=nmm_bright(weapon), width=3)
    
    # Base
    draw.ellipse([156, 480, 366, 510], fill=(100, 80, 60), outline='black', width=2)

def draw_human(draw, armor, cloth, weapon, skin, shade, highlight, edge_highlight, nmm_dark, nmm_bright):
    """Heavily armored human knight - heroic sword-raised defensive stance with NMM"""
    # Helmet - angled, battle-ready with NMM
    draw.polygon([221, 90, 291, 90, 301, 110, 301, 160, 211, 160, 211, 110], fill=armor, outline='black', width=2)
    draw.polygon([225, 95, 276, 95, 286, 110, 286, 155], fill=nmm_bright(armor), outline=None)
    draw.polygon([285, 95, 297, 110, 297, 155], fill=nmm_dark(armor), outline=None)
    draw.line([221, 90, 291, 90], fill=nmm_bright(armor), width=3)
    draw.line([221, 90, 211, 160], fill=nmm_bright(armor), width=2)
    
    # Visor slit
    draw.rectangle([231, 120, 281, 130], fill=nmm_dark(armor), outline=None)
    
    # Torso - turned, shield forward with NMM heavy plate
    points = [191, 160, 321, 160, 331, 240, 321, 340, 201, 340, 181, 240]
    draw.polygon(points, fill=armor, outline='black', width=2)
    draw.polygon([195, 165, 276, 165, 286, 240, 276, 335], fill=nmm_bright(armor), outline=None)
    draw.polygon([295, 165, 327, 165, 327, 240, 317, 335], fill=nmm_dark(armor), outline=None)
    draw.line([191, 160, 321, 160], fill=nmm_bright(armor), width=3)
    draw.line([191, 160, 181, 240], fill=nmm_bright(armor), width=2)
    draw.line([276, 165, 276, 335], fill=nmm_bright(armor), width=2)
    
    # Pauldrons - large, protective with NMM
    draw.ellipse([151, 160, 221, 220], fill=armor, outline='black', width=2)
    draw.ellipse([291, 160, 361, 220], fill=armor, outline='black', width=2)
    draw.ellipse([155, 165, 205, 205], fill=nmm_bright(armor), outline=None)
    draw.ellipse([295, 165, 345, 205], fill=nmm_bright(armor), outline=None)
    draw.ellipse([185, 185, 217, 216], fill=nmm_dark(armor), outline=None)
    draw.arc([151, 160, 221, 220], 180, 0, fill=nmm_bright(armor), width=3)
    draw.arc([291, 160, 361, 220], 180, 0, fill=nmm_bright(armor), width=3)
    
    # Left arm - shield raised with NMM
    draw.polygon([151, 210, 111, 240, 111, 270, 151, 250], fill=armor, outline='black', width=2)
    draw.polygon([145, 215, 120, 240, 120, 260, 145, 245], fill=nmm_bright(armor), outline=None)
    draw.line([151, 210, 111, 240], fill=nmm_bright(armor), width=2)
    
    # Shield - large, defensive
    draw.ellipse([71, 220, 141, 340], fill=armor, outline='black', width=3)
    draw.ellipse([85, 240, 127, 320], fill=cloth, outline=None)
    draw.arc([71, 220, 141, 340], 90, 270, fill=nmm_bright(armor), width=3)
    draw.ellipse([80, 235, 110, 275], fill=nmm_bright(armor), outline=None)
    
    # Right arm - sword raised high with NMM
    draw.polygon([321, 180, 361, 100, 381, 110, 341, 190], fill=armor, outline='black', width=2)
    draw.polygon([325, 185, 365, 110, 375, 115, 335, 185], fill=nmm_bright(armor), outline=None)
    draw.polygon([355, 130, 377, 110, 372, 115], fill=nmm_dark(armor), outline=None)
    draw.line([321, 180, 361, 100], fill=nmm_bright(armor), width=2)
    
    # Gauntlet
    draw.rectangle([351, 90, 381, 120], fill=armor, outline='black', width=2)
    draw.rectangle([355, 93, 370, 117], fill=nmm_bright(armor), outline=None)
    
    # Legs - wide defensive stance with NMM
    # Front leg bent
    draw.polygon([201, 340, 181, 440, 191, 490, 231, 490, 251, 430], fill=armor, outline='black', width=2)
    draw.polygon([205, 345, 195, 430, 205, 485], fill=nmm_bright(armor), outline=None)
    draw.polygon([225, 410, 247, 430, 243, 485], fill=nmm_dark(armor), outline=None)
    draw.line([201, 340, 251, 340], fill=nmm_bright(armor), width=3)
    
    # Back leg straight
    draw.polygon([271, 340, 301, 440, 311, 480, 281, 480, 261, 430], fill=armor, outline='black', width=2)
    draw.polygon([275, 345, 295, 430, 295, 475], fill=nmm_bright(armor), outline=None)
    draw.polygon([295, 410, 307, 440, 303, 475], fill=nmm_dark(armor), outline=None)
    draw.line([271, 340, 301, 340], fill=nmm_bright(armor), width=3)
    
    # Sword - raised triumphantly with NMM
    draw.rectangle([371, 50, 386, 110], fill=weapon, outline='black', width=2)
    draw.rectangle([373, 55, 378, 105], fill=nmm_bright(weapon), outline=None)
    draw.rectangle([380, 55, 384, 105], fill=nmm_dark(weapon), outline=None)
    # Crossguard and pommel
    draw.polygon([361, 40, 396, 40, 396, 55, 361, 55], fill=weapon, outline='black', width=2)
    draw.line([361, 40, 396, 40], fill=nmm_bright(weapon), width=2)
    draw.line([371, 50, 371, 110], fill=nmm_bright(weapon), width=2)
    
    # Cape - flowing dramatically
    draw.polygon([191, 180, 141, 200, 131, 380, 181, 340], fill=cloth, outline='black', width=2)
    draw.polygon([185, 190, 150, 205, 145, 360, 175, 335], fill=highlight(cloth), outline=None)
    draw.polygon([160, 220, 140, 230, 140, 370, 160, 360], fill=shade(cloth), outline=None)
    draw.line([191, 180, 141, 200], fill=edge_highlight(cloth), width=2)
    
    # Base
    draw.ellipse([156, 480, 346, 510], fill=(100, 80, 60), outline='black', width=2)

def create_fallback_image(scheme, output_path):
    """Legacy single image - now creates human by default"""
    return create_model_image(scheme, 'human', output_path)
