"""Slim down everything in papers/ that exceeds a size threshold.

Strategy:
- For each *.pdf: downsample embedded JPEGs to <=1200px, re-encode at quality 60.
- For each *.tar.gz that contains many large image files: rebuild a slimmed
  tarball that keeps only LaTeX source / BibTeX / class files. The slim PDF
  retains the figures at the chosen fidelity, so the tarball doesn't need them.

Run from repo root:  python agent-tools/slim_papers.py

Files smaller than --pdf-threshold MB / --tar-threshold MB are left alone.
"""

import argparse
import io
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import pikepdf
from PIL import Image


# Extensions kept inside slimmed tarballs (LaTeX source-only).
TEXT_EXTS = {".tex", ".bib", ".bbl", ".cls", ".sty", ".cfg", ".bst",
             ".clo", ".def", ".fd", ".ltx", ".dtx", ".ins", ".aux",
             ".log", ".json", ".md", ".txt", ".csv", ".rst",
             ".readme", ".gitignore"}
SPECIAL_KEEP_NAMES = {"makefile", "readme", "00readme", "license"}


def slim_pdf(in_path: Path, out_path: Path, max_dim: int, quality: int) -> None:
    pdf = pikepdf.open(str(in_path))
    n_replaced = 0
    n_skipped = 0

    for page in pdf.pages:
        for img_name, raw_image in list(page.images.items()):
            try:
                pdf_img = pikepdf.PdfImage(raw_image)
                pil_image = pdf_img.as_pil_image()
            except Exception:
                n_skipped += 1
                continue

            w, h = pil_image.size
            if max(w, h) <= max_dim and pil_image.mode in ("RGB", "L", "1"):
                continue

            scale = min(1.0, max_dim / max(w, h))
            new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
            resized = pil_image.resize(new_size, Image.LANCZOS) if scale < 1.0 else pil_image

            if resized.mode in ("RGBA", "P", "LA"):
                resized = resized.convert("RGB")
            elif resized.mode == "1":
                continue

            buf = io.BytesIO()
            resized.save(buf, format="JPEG", quality=quality, optimize=True)
            jpeg_bytes = buf.getvalue()

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

    pdf.save(str(out_path), object_stream_mode=pikepdf.ObjectStreamMode.generate,
             linearize=False, compress_streams=True, recompress_flate=True)
    print(f"  {in_path.name}: replaced {n_replaced} images, skipped {n_skipped}")


def slim_tarball(in_path: Path, out_path: Path) -> None:
    """Rebuild tarball keeping only LaTeX source files (no embedded figures)."""
    kept = 0
    dropped = 0
    dropped_bytes = 0

    with tarfile.open(in_path, "r:gz") as src:
        with tarfile.open(out_path, "w:gz") as dst:
            for member in src:
                # Decision: keep text-format LaTeX-style files; drop everything else.
                name = member.name
                lower = name.lower()
                base = Path(name).name.lower()
                ext = Path(name).suffix.lower()
                keep = ext in TEXT_EXTS or any(s in base for s in SPECIAL_KEEP_NAMES)
                if member.isdir():
                    keep = True

                if keep:
                    extracted = src.extractfile(member)
                    if extracted is None:
                        dst.addfile(member)  # symlink/dir
                    else:
                        data = extracted.read()
                        info = tarfile.TarInfo(name=member.name)
                        info.size = len(data)
                        info.mtime = member.mtime
                        info.mode = member.mode
                        info.type = member.type
                        info.uid = member.uid
                        info.gid = member.gid
                        info.uname = member.uname
                        info.gname = member.gname
                        dst.addfile(info, io.BytesIO(data))
                    kept += 1
                else:
                    dropped += 1
                    dropped_bytes += member.size

    print(f"  {in_path.name}: kept {kept} files, dropped {dropped} ({dropped_bytes/(1024*1024):.1f} MB)")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--papers-dir", type=Path, default=Path("papers"))
    p.add_argument("--pdf-threshold-mb", type=float, default=5.0,
                   help="Slim PDFs larger than this many MB.")
    p.add_argument("--tar-threshold-mb", type=float, default=2.0,
                   help="Slim tarballs larger than this many MB.")
    p.add_argument("--max-dim", type=int, default=1200)
    p.add_argument("--quality", type=int, default=60)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    papers_dir = args.papers_dir
    if not papers_dir.is_dir():
        print(f"No such directory: {papers_dir}", file=sys.stderr)
        return 1

    pdf_threshold = args.pdf_threshold_mb * 1024 * 1024
    tar_threshold = args.tar_threshold_mb * 1024 * 1024

    targets = []
    for entry in sorted(papers_dir.iterdir()):
        if not entry.is_file():
            continue
        size = entry.stat().st_size
        if entry.suffix.lower() == ".pdf" and size > pdf_threshold:
            targets.append(("pdf", entry, size))
        elif entry.name.lower().endswith(".tar.gz") and size > tar_threshold:
            targets.append(("tar", entry, size))

    if not targets:
        print("Nothing to slim.")
        return 0

    print(f"Slimming {len(targets)} files in {papers_dir}/:")
    for kind, path, size in targets:
        print(f"  {kind.upper()}  {path.name}  ({size/(1024*1024):.1f} MB)")

    if args.dry_run:
        return 0

    backup_dir = papers_dir / "_originals"
    backup_dir.mkdir(exist_ok=True)
    print(f"\nMoving originals to {backup_dir}/ for safe rollback.\n")

    for kind, path, size in targets:
        backup = backup_dir / path.name
        if not backup.exists():
            shutil.copy2(path, backup)
        tmp_out = path.with_suffix(path.suffix + ".tmp")
        try:
            if kind == "pdf":
                slim_pdf(path, tmp_out, args.max_dim, args.quality)
            else:
                slim_tarball(path, tmp_out)
            tmp_out.replace(path)
            new_size = path.stat().st_size
            print(f"  {path.name}:  {size/(1024*1024):.1f} MB -> {new_size/(1024*1024):.1f} MB"
                  f"   ({100*(1-new_size/size):.1f}% smaller)\n")
        except Exception as e:
            print(f"  ERROR slimming {path.name}: {e}", file=sys.stderr)
            if tmp_out.exists():
                tmp_out.unlink()

    print("Done. Originals preserved in", backup_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
