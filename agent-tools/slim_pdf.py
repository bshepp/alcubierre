"""Slim a PDF by downsampling and re-encoding embedded images.

Usage: python agent-tools/slim_pdf.py <input.pdf> <output.pdf> [--max-dim 1200] [--quality 60]

For each embedded raster image: decode with PIL, downsample so the longest edge is at
most --max-dim pixels, re-encode as JPEG at --quality, and replace the original stream
in-place.  This typically shrinks research PDFs from ~30 MB to a few MB without
hurting normal-resolution readability.
"""

import sys
import io
import argparse
from pathlib import Path

import pikepdf
from PIL import Image


def slim_pdf(in_path: Path, out_path: Path, max_dim: int, quality: int) -> None:
    pdf = pikepdf.open(str(in_path))
    n_replaced = 0
    n_skipped = 0

    for page_idx, page in enumerate(pdf.pages):
        for img_name, raw_image in list(page.images.items()):
            try:
                pdf_img = pikepdf.PdfImage(raw_image)
                pil_image = pdf_img.as_pil_image()
            except Exception as e:
                n_skipped += 1
                if n_skipped <= 3:
                    print(f"  page {page_idx}: skip {img_name} ({type(e).__name__}: {e})")
                continue

            w, h = pil_image.size
            if max(w, h) <= max_dim and pil_image.mode in ("RGB", "L", "1"):
                # Already small; skip to avoid quality loss.
                continue

            scale = min(1.0, max_dim / max(w, h))
            new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
            resized = pil_image.resize(new_size, Image.LANCZOS) if scale < 1.0 else pil_image

            if resized.mode in ("RGBA", "P", "LA"):
                resized = resized.convert("RGB")
            elif resized.mode == "1":
                # Tiny mono masks; leave alone
                continue

            buf = io.BytesIO()
            resized.save(buf, format="JPEG", quality=quality, optimize=True)
            jpeg_bytes = buf.getvalue()

            # In-place rewrite of the image stream.
            raw_image.write(jpeg_bytes, filter=pikepdf.Name("/DCTDecode"))
            raw_image.Width = resized.width
            raw_image.Height = resized.height
            raw_image.ColorSpace = (
                pikepdf.Name("/DeviceGray") if resized.mode == "L" else pikepdf.Name("/DeviceRGB")
            )
            raw_image.BitsPerComponent = 8
            for k in ("/DecodeParms", "/SMask", "/Mask"):
                if k in raw_image:
                    del raw_image[pikepdf.Name(k)]

            n_replaced += 1
            if n_replaced <= 5 or n_replaced % 25 == 0:
                print(f"  page {page_idx}: {img_name}  {w}x{h} -> {resized.width}x{resized.height}  "
                      f"({len(jpeg_bytes)//1024} KB JPEG)")

    print(f"\nReplaced {n_replaced} images, skipped {n_skipped} (mostly small/monochrome).")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.save(str(out_path), object_stream_mode=pikepdf.ObjectStreamMode.generate,
             linearize=False, compress_streams=True, recompress_flate=True)
    in_size = in_path.stat().st_size / (1024 * 1024)
    out_size = out_path.stat().st_size / (1024 * 1024)
    print(f"\nInput:  {in_size:.1f} MB ({in_path})")
    print(f"Output: {out_size:.1f} MB ({out_path})")
    print(f"Reduction: {100*(1 - out_size/in_size):.1f}%")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--max-dim", type=int, default=1200)
    p.add_argument("--quality", type=int, default=60)
    args = p.parse_args()
    slim_pdf(args.input, args.output, args.max_dim, args.quality)


if __name__ == "__main__":
    main()
