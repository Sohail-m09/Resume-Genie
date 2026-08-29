from pathlib import Path
import shutil
import subprocess


def build_pdf(
    latex_source: str,
    output_directory: str = "data/output",
    filename: str = "tailored_resume",
) -> Path:
    """
    Write LaTeX source to disk and compile it into a PDF.
    """

    output_path = Path(output_directory)
    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    tex_path = output_path / f"{filename}.tex"

    tex_path.write_text(
        latex_source,
        encoding="utf-8",
    )

    pdflatex = shutil.which("pdflatex")

    if pdflatex is None:
        raise RuntimeError(
            "pdflatex was not found. "
            "Install MiKTeX or TeX Live and make sure "
            "pdflatex is available on PATH."
        )

    result = subprocess.run(
        [
            pdflatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={output_path}",
            str(tex_path),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "LaTeX compilation failed.\n\n"
            + result.stdout
            + "\n"
            + result.stderr
        )

    pdf_path = output_path / f"{filename}.pdf"

    if not pdf_path.exists():
        raise RuntimeError(
            "LaTeX compilation completed, "
            "but the expected PDF was not created."
        )

    return pdf_path