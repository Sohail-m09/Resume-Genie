from pathlib import Path

from resume_generator.tailoring import TailoredResume


TEMPLATE_PATH = Path(__file__).with_name(
    "latex_template.tex"
)


def escape_latex(text: str) -> str:
    """
    Escape characters that have special meaning in LaTeX.
    """

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    return text

def format_skills(skills: list[str]) -> str:
    """
    Format skills into ATS-friendly categorized groups
    without duplicating a skill across categories.
    """

    categories = {
        "Programming Languages": {
            "Python",
            "SQL",
        },

        "Python Libraries": {
            "Pandas",
            "NumPy",
            "Scikit-learn",
        },

        "Machine Learning": {
            "Machine Learning",
            "Linear Regression",
            "Logistic Regression",
            "Decision Trees",
            "Random Forest",
            "K-Means",
            "XGBoost",
            "Model Evaluation",
        },

        "Data Analysis": {
            "Cleaning",
            "EDA",
            "Statistical Analysis",
            "Hypothesis Testing",
        },

        "Data Visualization": {
            "Power BI",
            "Matplotlib",
            "Seaborn",
            "Plotly",
            "Tableau",
        },

        "Databases": {
            "MySQL",
            "PostgreSQL",
            "MongoDB",
        },

        "Version Control": {
            "Git",
            "GitHub",
        },

        "Tools": {
            "Excel",
            "Jupyter Notebook",
            "Google Colab",
            "VS Code",
            "Anaconda",
        },

        "Core Concepts": {
            "Probability",
            "Statistics",
        },
    }

    skill_lookup = {
        skill.lower(): skill
        for skill in skills
    }

    used = set()
    lines = []

    for category, category_skills in categories.items():

        matched = []

        for skill in category_skills:

            original_skill = skill_lookup.get(
                skill.lower()
            )

            if original_skill:
                matched.append(original_skill)
                used.add(original_skill.lower())

        if matched:
            lines.append(
                f"\\textbf{{{escape_latex(category)}:}} "
                f"{escape_latex(', '.join(matched))}"
            )

    # Preserve any skills that do not belong to
    # one of the predefined categories.
    other_skills = [
        skill
        for skill in skills
        if skill.lower() not in used
    ]

    if other_skills:
        lines.append(
            f"\\textbf{{Other:}} "
            f"{escape_latex(', '.join(other_skills))}"
        )

    return "\\\\\n".join(lines)

def format_education(
    education,
) -> str:
    """
    Convert structured education into professional
    resume-style formatting.
    """

    lines = []

    for item in education:

        degree = escape_latex(
            item.degree
        )

        institution = escape_latex(
            item.institution
        )

        year = (
            escape_latex(item.year)
            if item.year
            else ""
        )

        details = (
            escape_latex(item.details)
            if item.details
            else ""
        )

        header = (
            f"\\textbf{{{degree}}}"
        )

        if institution:
            header += (
                f" --- {institution}"
            )

        if year:
            header += (
                f" \\hfill {year}"
            )

        lines.append(header)

        if details:
            lines.append(
                f"\\\\ {details}"
            )

        lines.append(
            "\\vspace{1pt}"
        )

    return "\n".join(lines)




def format_projects(
    projects,
) -> str:
    """
    Convert projects into clean resume-style bullet points.
    """

    sections = []

    for project in projects:

        name = escape_latex(
            project.name
        )

        technologies = escape_latex(
            ", ".join(project.technologies)
        )

        bullets = []

        for bullet in project.bullets:

            bullets.append(
                f"\\item {escape_latex(bullet)}"
            )

        project_block = (
            f"\\textbf{{{name}}}"
            f" \\hfill "
            f"\\textit{{{technologies}}}"
            f"\\\\\n"
            "\\begin{itemize}\n"
            + "\n".join(bullets)
            + "\n\\end{itemize}\n"
            "\\vspace{1pt}"
        )

        sections.append(
            project_block
        )

    return "\n".join(sections)


def format_experience(
    experience,
) -> str:
    """
    Format existing professional experience.

    No experience means no fabricated section.
    """

    if not experience:
        return ""

    lines = []

    for item in experience:

        lines.append(
            f"\\item {escape_latex(str(item))}"
        )

    return (
        "\\section*{Professional Experience}\n"
        "\\begin{itemize}\n"
        + "\n".join(lines)
        + "\n\\end{itemize}"
    )


def format_certifications(
    certifications,
) -> str:
    """
    Convert certifications into LaTeX.
    """

    if not certifications:
        return ""

    lines = []

    for certification in certifications:

        lines.append(
            f"\\item {escape_latex(str(certification))}"
        )

    return (
        "\\section*{Certifications}\n"
        "\\begin{itemize}[itemsep=0pt, topsep=1pt]\n"
        + "\n".join(lines)
        + "\n\\end{itemize}"
    )


def extract_personal_information(
    resume,
) -> dict:
    """
    Extract contact information from the original resume.

    Personal information is preserved from the original
    structured resume and is not regenerated by the LLM.
    """

    data = (
        resume.personal_information.model_dump()
    )

    def first_value(*keys):
        for key in keys:
            value = data.get(key)

            if value:
                return str(value)

        return ""

    return {
        "name": first_value(
            "name",
            "full_name",
        ),

        "email": first_value(
            "email",
            "mail",
        ),

        "phone": first_value(
            "phone",
            "phone_number",
        ),

        "location": first_value(
            "location",
            "address",
        ),

        "linkedin": first_value(
            "linkedin",
            "linkedin_url",
        ),

        "github": first_value(
            "github",
            "github_url",
        ),

        "portfolio": first_value(
            "portfolio",
            "portfolio_url",
        ),
    }


def build_contact_line(
    resume,
) -> str:
    """
    Build a clean clickable contact line from
    the original resume information.
    """

    contact = extract_personal_information(
        resume
    )

    first_line_values = []

    if contact["email"]:
        first_line_values.append(
            rf"\href{{mailto:{contact['email']}}}{{{escape_latex(contact['email'])}}}"
        )

    if contact["phone"]:
        first_line_values.append(
            escape_latex(contact["phone"])
        )

    if contact["location"]:
        first_line_values.append(
            escape_latex(contact["location"])
        )

    contact_line = r" \quad | \quad ".join(
        first_line_values
    )

    links = []

    if contact["linkedin"]:
        linkedin_url = contact["linkedin"]

        if not linkedin_url.startswith(
            ("http://", "https://")
        ):
            linkedin_url = (
                "https://" + linkedin_url
            )

        links.append(
            rf"\href{{{linkedin_url}}}{{{escape_latex(contact['linkedin'])}}}"
        )

    if contact["github"]:
        github_url = contact["github"]

        if not github_url.startswith(
            ("http://", "https://")
        ):
            github_url = (
                "https://" + github_url
            )

        links.append(
            rf"\href{{{github_url}}}{{{escape_latex(contact['github'])}}}"
        )

    if links:
        if contact_line:
            contact_line += r" \\ "

        contact_line += (
            r" \quad | \quad ".join(links)
        )

    return contact_line




def build_sections(
    tailored_resume: TailoredResume,
) -> str:
    """
    Build resume sections according to the
    section_order stored in the tailored resume.
    """

    sections = []

    for section in tailored_resume.section_order:

        if section == "summary":
            sections.append(
                "\\section*{Professional Summary}\n\n"
                + escape_latex(tailored_resume.summary)
            )

        elif section == "skills":
            sections.append(
                "\\section*{Technical Skills}\n\n"
                + format_skills(tailored_resume.skills)
            )

        elif section == "education":
            if tailored_resume.education:
                sections.append(
                    "\\section*{Education}\n\n"
                    + format_education(
                        tailored_resume.education
                    )
                )

        elif section == "projects":
            if tailored_resume.projects:
                sections.append(
                    "\\section*{Projects}\n\n"
                    + format_projects(
                        tailored_resume.projects
                    )
                )

        elif section == "experience":
            if tailored_resume.experience:
                sections.append(
                    format_experience(
                        tailored_resume.experience
                    )
                )

        elif section == "certifications":
            if tailored_resume.certifications:
                sections.append(
                    format_certifications(
                        tailored_resume.certifications
                    )
                )

    return "\n\n".join(sections)


def generate_latex(
    tailored_resume: TailoredResume,
    original_resume,
) -> str:
    """
    Generate LaTeX source from the validated
    tailored structured resume.

    Section order is controlled by tailored_resume.section_order.
    """

    template = TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    personal_information = (
        extract_personal_information(
            original_resume
        )
    )

    latex = template.replace(
        "{{NAME}}",
        escape_latex(
            personal_information["name"]
        ),
    )

    latex = latex.replace(
        "{{CONTACT_LINE}}",
        build_contact_line(
            original_resume
        ),
    )

    sections = build_sections(
        tailored_resume
    )

    latex = latex.replace(
        "{{SECTIONS}}",
        sections,
    )

    return latex