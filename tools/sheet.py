import sys, traceback, reel3, lessons2
from PIL import Image
keys = sys.argv[1:] or list(lessons2.L)
for key in keys:
    tiles = []
    for i in range(5):
        for tag, fr in (("a", -0.45), ("b", -0.92)):
            try:
                reel3.build(key, (i, fr, tag))
                tiles.append(Image.open(f"v3/still_{key}_{i}{tag}.png").crop((60, 280, 1020, 1000)).resize((480, 360)))
            except Exception:
                print("FAIL", key, i, tag); traceback.print_exc(limit=3); tiles.append(Image.new("RGB", (480, 360), (255, 0, 0)))
    s = Image.new("RGB", (2400, 720))
    for j, im in enumerate(tiles): s.paste(im, ((j // 2) * 480, (j % 2) * 360))
    s.save(f"v3/sheet_{key}.png"); print("sheet", key, flush=True)
