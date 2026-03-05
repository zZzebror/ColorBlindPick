from generator import generate_scheme, HARMONY_TYPES
from image_generator import generate_all_models
import sys

def display_scheme(scheme):
    print("\n" + "="*60)
    print(f"🎨 {scheme['scheme_name']}")
    print(f"   ({scheme['harmony_type'].replace('_', ' ').title()})")
    print("="*60)
    
    print("\n📦 COLOR PALETTE:")
    print(f"  Dominant:  {scheme['palette']['dominant']}")
    print(f"  Secondary: {scheme['palette']['secondary']}")
    for i, accent in enumerate(scheme['palette']['accent'], 1):
        print(f"  Accent {i}:   {accent}")
    print(f"  Neutral:   {scheme['palette']['neutral']}")
    
    print("\n🎓 COLOR THEORY:")
    print(f"  {scheme['color_theory']}")
    
    print("\n🖌️  PAINTING TECHNIQUES:")
    for tech in scheme['painting_techniques']:
        print(f"  • {tech}")
    
    print("\n💡 TIPS:")
    for tip in scheme['tips']:
        print(f"  • {tip}")
    
    print("\n📚 TRIVIA:")
    print(f"  {scheme['trivia']}")
    
    print("\n🖼️  IMAGE PROMPT:")
    print(f"  {scheme['image_prompt']}")
    print("\n" + "="*60 + "\n")

def main():
    if len(sys.argv) > 1:
        harmony = sys.argv[1].lower()
        if harmony not in HARMONY_TYPES:
            print(f"Invalid harmony type. Choose from: {', '.join(HARMONY_TYPES)}")
            sys.exit(1)
        scheme = generate_scheme(harmony)
    else:
        scheme = generate_scheme()
    
    display_scheme(scheme)
    
    # Generate images for all three model types
    print("🎨 Generating miniature images...")
    image_paths = generate_all_models(scheme)
    for path in image_paths:
        print(f"✅ {path}")
    print()

if __name__ == "__main__":
    main()
