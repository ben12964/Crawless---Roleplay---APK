from pathlib import Path
from PIL import Image
import re
root = Path('decoded')
icon = Image.open('crawless_icon.png').convert('RGBA')
# Replace launcher resources at the dimensions expected by the decoded APK.
for folder in root.glob('res/mipmap-*'):
    if not folder.is_dir():
        continue
    for name in ('ic_launcher.webp', 'ic_launcher_round.webp', 'ic_launcher_foreground.webp', 'ic_launcher.png', 'ic_launcher_round.png', 'ic_launcher_foreground.png'):
        target = folder / name
        if target.exists():
            with Image.open(target) as old:
                size = old.size
            # Keep the icon resource's original dimensions and format.
            out = icon.resize(size, Image.Resampling.LANCZOS)
            if target.suffix.lower() == '.webp':
                out.save(target, 'WEBP', quality=92, method=6)
            else:
                out.save(target, 'PNG', optimize=True)
# Change common Android app-label string, if present.
for strings in root.glob('res/values*/strings.xml'):
    text = strings.read_text(encoding='utf-8')
    text2 = re.sub(r'(<string\s+name="app_name"[^>]*>).*?(</string>)', r'\1Crawless Roleplay\2', text, count=1, flags=re.S)
    if text2 != text:
        strings.write_text(text2, encoding='utf-8')
print('Launcher resources replaced; app_name updated if present.')
