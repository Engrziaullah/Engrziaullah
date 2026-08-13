"""Stage 1: crop, preprocess, segment, dither. Saves diagnostic PNGs + .npy dot arrays."""
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from scipy import ndimage
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source.jpg")
GRID_W, GRID_H = 300, 340


def load_and_crop():
    im = Image.open(SRC).convert("RGB")
    w, h = im.size
    target_aspect = GRID_W / GRID_H  # width/height
    new_w = int(round(h * target_aspect))
    if new_w <= w:
        left = (w - new_w) // 2
        im = im.crop((left, 0, left + new_w, h))
    else:
        new_h = int(round(w / target_aspect))
        top = (h - new_h) // 2
        im = im.crop((0, top, w, top + new_h))
    return im


def sample_background_color(im):
    # Only the top strip is guaranteed background in a head+shoulders crop -
    # bottom corners are inside the suit shoulders, not background.
    w, h = im.size
    strip = im.crop((0, 0, w, int(h * 0.08)))
    px = np.array(strip).reshape(-1, 3)
    return np.median(px, axis=0)


def segment_foreground(rgb_arr, bg_color, thresh=30):
    dist = np.linalg.norm(rgb_arr.astype(float) - bg_color[None, None, :], axis=2)
    fg = dist > thresh
    fg = ndimage.binary_closing(fg, structure=np.ones((5, 5)), iterations=2)
    fg = ndimage.binary_fill_holes(fg)
    labeled, n = ndimage.label(fg)
    if n > 0:
        sizes = ndimage.sum(fg, labeled, range(1, n + 1))
        biggest = int(np.argmax(sizes)) + 1
        fg = labeled == biggest
    return fg


def preprocess_gray(im):
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    g = ImageEnhance.Contrast(g).enhance(1.3)
    g = g.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    return g


def floyd_steinberg_serpentine(gray_arr, mask=None):
    """gray_arr: float HxW in 0..255. mask: bool HxW or None.
    Returns bool HxW: True = ink/dot. Error never diffuses into or out of masked-off cells."""
    h, w = gray_arr.shape
    buf = gray_arr.astype(np.float64).copy()
    if mask is not None:
        buf[~mask] = 255.0  # background forced to "pure white" -> never triggers ink, contributes zero error
    out = np.zeros((h, w), dtype=bool)
    for y in range(h):
        serp = y % 2 == 1
        xs = range(w - 1, -1, -1) if serp else range(w)
        dx = -1 if serp else 1
        for x in xs:
            if mask is not None and not mask[y, x]:
                continue
            old = buf[y, x]
            new = 255.0 if old >= 128.0 else 0.0
            out[y, x] = new == 0.0
            err = old - new
            for ny, nx, frac in ((y, x + dx, 7 / 16), (y + 1, x - dx, 3 / 16), (y + 1, x, 5 / 16), (y + 1, x + dx, 1 / 16)):
                if 0 <= ny < h and 0 <= nx < w:
                    if mask is None or mask[ny, nx]:
                        buf[ny, nx] += err * frac
    if mask is not None:
        out &= mask
    return out


def main():
    im = load_and_crop()
    print("cropped size", im.size)
    im.save(os.path.join(HERE, "diag_00_cropped.png"))

    bg = sample_background_color(im)
    print("background color estimate", bg)

    rgb_arr = np.array(im)
    fg_mask = segment_foreground(rgb_arr, bg)
    print("foreground coverage", fg_mask.mean())
    Image.fromarray((fg_mask * 255).astype(np.uint8)).save(os.path.join(HERE, "diag_01_mask.png"))

    gray = preprocess_gray(im)
    gray.save(os.path.join(HERE, "diag_02_gray.png"))
    gray_small = gray.resize((GRID_W, GRID_H), Image.LANCZOS)
    gray_small.save(os.path.join(HERE, "diag_03_gray_small.png"))
    mask_small = np.array(
        Image.fromarray((fg_mask * 255).astype(np.uint8)).resize((GRID_W, GRID_H), Image.NEAREST)
    ) > 127
    print("foreground coverage (grid res)", mask_small.mean())

    gray_arr = np.array(gray_small).astype(np.float64)

    # LIGHT mode: keep background, ink = dark pixels.
    # A brightening gamma (<1) on the ink-decision input keeps ink to genuinely dark
    # regions only -- without it, dot count runs ~2x too dense (see banner/README notes).
    LIGHT_GAMMA = 0.20
    light_input = 255.0 * ((gray_arr / 255.0) ** LIGHT_GAMMA)
    dots_light = floyd_steinberg_serpentine(light_input, mask=None)
    print("light dots:", dots_light.sum(), f"{dots_light.mean()*100:.1f}% density")

    # DARK mode: invert (ink = bright/lit pixels), masked to foreground only.
    # Contrast-stretch within the mask first (principled, though empirically a near
    # no-op on this photo), then the same kind of brightening gamma.
    DARK_GAMMA = 0.19  # dot count plateaus ~24-26k below this; lower breaks midtone skin into a black void
    inverted = 255.0 - gray_arr
    fg_vals = inverted[mask_small]
    lo, hi = np.percentile(fg_vals, 1), np.percentile(fg_vals, 99)
    stretched = np.clip((inverted - lo) / (hi - lo) * 255.0, 0, 255)
    dark_input = 255.0 * ((stretched / 255.0) ** DARK_GAMMA)
    dots_dark = floyd_steinberg_serpentine(dark_input, mask=mask_small)
    print("dark dots:", dots_dark.sum(), f"{dots_dark.mean()*100:.1f}% density (of full grid)")
    if mask_small.sum() > 0:
        print("dark dots as % of foreground area:", dots_dark.sum() / mask_small.sum() * 100)

    Image.fromarray((~dots_light * 255).astype(np.uint8)).resize((900, 1020), Image.NEAREST).save(
        os.path.join(HERE, "diag_04_dither_light.png")
    )
    Image.fromarray((dots_dark * 255).astype(np.uint8)).resize((900, 1020), Image.NEAREST).save(
        os.path.join(HERE, "diag_05_dither_dark.png")
    )

    np.save(os.path.join(HERE, "dots_light.npy"), dots_light)
    np.save(os.path.join(HERE, "dots_dark.npy"), dots_dark)
    np.save(os.path.join(HERE, "mask.npy"), mask_small)


if __name__ == "__main__":
    main()
