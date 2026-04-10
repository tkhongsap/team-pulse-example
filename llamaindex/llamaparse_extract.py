#!/usr/bin/env python3
"""Extract content from documents using LlamaParse.

Supports PDF, DOCX, PPTX, XLSX, HTML, and more.

Usage:
    python llamaparse_extract.py document.pdf
    python llamaparse_extract.py report.docx
    python llamaparse_extract.py docs/ -f text -o results/
    python llamaparse_extract.py paper.pdf --tier agentic_plus -v
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from llama_parse import LlamaParse

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "output"
TIERS = ("agentic", "agentic_plus", "cost_effective", "fast")
VENDOR_MODELS = (
    "openai-gpt4o",
    "openai-gpt-4o-mini",
    "openai-gpt-4-1-nano",
    "openai-gpt-4-1-mini",
    "openai-gpt-4-1",
    "anthropic-sonnet-3.7",
    "anthropic-sonnet-4.0",
    "anthropic-sonnet-4.5",
    "anthropic-haiku-4.5",
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
)


def get_api_key(override: str | None = None) -> str:
    if override:
        return override
    load_dotenv()
    load_dotenv(SCRIPT_DIR.parent / ".env")
    key = os.getenv("LLAMA_CLOUD_API_KEY", "")
    if not key:
        sys.exit("LLAMA_CLOUD_API_KEY not found. Set it in .env or pass --api-key.")
    return key


SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
    ".html", ".htm", ".txt", ".rtf", ".odt", ".epub",
}


def find_documents(paths: list[str]) -> list[Path]:
    result = []
    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            result.append(path)
        elif path.is_dir():
            result.extend(
                sorted(f for f in path.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS)
            )
        else:
            sys.exit(f"Not a supported document file or directory: {p}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract PDFs using LlamaParse.")
    parser.add_argument("input", nargs="+", help="Document file(s) or directory (PDF, DOCX, etc.)")
    parser.add_argument("-f", "--format", choices=("markdown", "text"), default="markdown")
    parser.add_argument("-o", "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--tier", choices=TIERS, default="agentic")
    parser.add_argument("--model", choices=VENDOR_MODELS, default=None,
                        help="Vendor multimodal model (overrides tier default)")
    parser.add_argument("--api-key", help="Override LLAMA_CLOUD_API_KEY env var")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    files = find_documents(args.input)
    if not files:
        sys.exit("No supported document files found.")

    result_type = "text" if args.format == "text" else "markdown"
    ext = ".txt" if args.format == "text" else ".md"
    args.output_dir.mkdir(parents=True, exist_ok=True)

    parse_kwargs = dict(api_key=api_key, result_type=result_type, tier=args.tier)
    if args.model:
        parse_kwargs["use_vendor_multimodal_model"] = True
        parse_kwargs["vendor_multimodal_model_name"] = args.model
    llama = LlamaParse(**parse_kwargs)
    failed = 0

    for i, pdf in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {pdf.name}")
        if args.verbose:
            model_info = f", model={args.model}" if args.model else ""
            print(f"  tier={args.tier}, format={result_type}{model_info}")
        try:
            docs = llama.load_data(str(pdf))
            if not docs:
                raise RuntimeError("No content extracted")
            content = "\n\n".join(doc.text for doc in docs)

            out_path = args.output_dir / f"{pdf.stem}{ext}"
            counter = 1
            while out_path.exists():
                out_path = args.output_dir / f"{pdf.stem}_{counter}{ext}"
                counter += 1

            out_path.write_text(content, encoding="utf-8")
            print(f"  -> {out_path} ({len(content)} chars)")
        except Exception as e:
            print(f"  FAILED: {e}", file=sys.stderr)
            failed += 1

    print(f"\nDone: {len(files) - failed} succeeded, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
