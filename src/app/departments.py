from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class DepartmentInfo:
    email: str
    description: str
    keywords: list[str]
    exclusions: list[str]

    def to_prompt_text(self, dept_name: str) -> str:
        keywords_str = ", ".join(self.keywords)
        exclusions_str = "\n    - ".join(self.exclusions)
        return (
            f"[{dept_name}]\n"
            f"  Email: {self.email}\n"
            f"  Responsibilities: {self.description}\n"
            f"  Keywords: {keywords_str}\n"
            f"  DO NOT ROUTE HERE (Exclusions):\n"
            f"    - {exclusions_str}"
        )


class Department(str, Enum):
    HELP_DESK = "HELP_DESK"
    IT = "IT"
    KADRY = "KADRY"
    HR = "HR"
    OTHER = "OTHER"

    @property
    def info(self) -> DepartmentInfo:
        return _DEPARTMENT_REGISTRY[self]

    @classmethod
    def to_prompt_description(cls) -> str:
        return "\n\n".join(
            _DEPARTMENT_REGISTRY[dept].to_prompt_text(dept.value)
            for dept in cls
        )


_DEPARTMENT_REGISTRY = {
    Department.HELP_DESK: DepartmentInfo(
        email="help-desk@example.com",
        description="Physical computer hardware, workstation peripherals, and desk equipment.",
        keywords=[
            "monitors", "mouse", "keyboards", "cables", "adapters", "HDMI", "USB-C",
            "headset crackling", "broken laptop ports/screens", "hardware spares"
        ],
        exclusions=[
            "Software errors, VPN, logins, or cyber threats -> Route to IT.",
            "Lost personal items in the office (umbrellas, jackets, keys) -> Route to OTHER."
        ],
    ),
    Department.IT: DepartmentInfo(
        email="it@example.com",
        description="Digital infrastructure, access permissions, internal software, and IT security.",
        keywords=[
            "login errors", "database access", "VPN disconnection", "GitLab/GitHub repos",
            "CI/CD pipelines", "Docker containers", "passwords",
            "suspicious emails", "phishing reports", "malicious zip/file verification"
        ],
        exclusions=[
            "Physical hardware damage, keyboards, broken monitors -> Route to HELP_DESK."
        ],
    ),
    Department.KADRY: DepartmentInfo(
        email="kadry@example.com",
        description="Official payroll, labor law administration, taxes, and formal employment records.",
        keywords=[
            "salary deductions/calculations", "statutory paid vacation days balance",
            "sick leave (L4) payroll impact", "annual tax forms (PIT-11)",
            "employment and income certificates for bank loans",
            "updating residential/contract address in personnel records"
        ],
        exclusions=[
            "Voluntary perks, gym/sport cards, medical insurance (for employee or children) -> Route to HR.",
            "Performance appraisals, employee reviews, referrals, or training budgets -> Route to HR."
        ],
    ),
    Department.HR: DepartmentInfo(
        email="human-resources@example.com",
        description="Employee benefits, wellness, talent development, culture, and recruitment.",
        keywords=[
            "gym cards / sports packages (for employee, child, or spouse)",
            "corporate private medical insurance policies",
            "language courses co-funding", "industry certification funding",
            "employee referral program and candidate CVs",
            "annual or periodic performance reviews and appraisals"
        ],
        exclusions=[
            "Base salary, payslips, official tax forms (PIT), statutory leave days balance -> Route to KADRY.",
            "Formal sick leave (L4) payroll inquiries, contract updates -> Route to KADRY."
        ],
    ),
    Department.OTHER: DepartmentInfo(
        email="other@example.com",
        description="Everyday office community life, social banter, and non-operational requests.",
        keywords=[
            "lunch/pizza orders", "after-work board games or drinks",
            "lost & found personal belongings (e.g. umbrella in kitchen)",
            "kudos, thank-you notes, company compliments", "cold sales spam"
        ],
        exclusions=[
            "Reporting a suspicious email or phishing threat -> Route to IT.",
            "Hardware issues or desk adapters -> Route to HELP_DESK."
        ],
    ),
}
