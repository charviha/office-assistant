from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)

OUTPUT_DIR = Path("data/policies")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COMPANY = "NOVATRIX TECHNOLOGIES PVT. LTD."
CLASSIFICATION = "Internal Use"
VERSION = "1.0"
EFFECTIVE_DATE = "01 January 2026"


styles = getSampleStyleSheet()

TITLE = ParagraphStyle(
    "TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=10
)
SUBTITLE = ParagraphStyle(
    "Subtitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, leading=14, alignment=TA_CENTER, spaceAfter=16
)
H1 = ParagraphStyle(
    "H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=13, leading=17, spaceBefore=10, spaceAfter=6
)
H2 = ParagraphStyle(
    "H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=10.5, leading=14, spaceBefore=7, spaceAfter=4
)
BODY = ParagraphStyle(
    "BodyCustom", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.5, leading=14, spaceAfter=6
)
BULLET = ParagraphStyle(
    "BulletCustom", parent=BODY, leftIndent=14, firstLineIndent=-7,
    bulletIndent=5, spaceAfter=3
)
SMALL = ParagraphStyle(
    "SmallCustom", parent=BODY, fontSize=8, leading=11
)
FAQ_Q = ParagraphStyle(
    "FAQQuestion", parent=BODY, fontName="Helvetica-Bold",
    spaceBefore=5, spaceAfter=2
)


def P(text, style=BODY):
    return Paragraph(text, style)


def bullets(items):
    return [P("• " + item, BULLET) for item in items]


def make_table(data, widths=None):
    converted = []
    for row in data:
        converted.append([
            cell if isinstance(cell, Paragraph) else P(str(cell), SMALL)
            for cell in row
        ])

    table = Table(converted, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1F2937")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B8C0CC")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.grey)
    canvas.drawString(18 * mm, 10 * mm,
                     f"{COMPANY} | {CLASSIFICATION}")
    canvas.drawRightString(
        192 * mm, 10 * mm, f"Page {doc.page}"
    )
    canvas.restoreState()


def build_pdf(filename, doc_id, title, owner, story):
    path = OUTPUT_DIR / filename
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=title,
        author=COMPANY,
    )

    header = [
        P(COMPANY, SUBTITLE),
        P(title, TITLE),
        P(f"Document ID: {doc_id} | Version: {VERSION} | Effective: {EFFECTIVE_DATE}", SUBTITLE),
        P(f"Owner: {owner} | Classification: {CLASSIFICATION}", SUBTITLE),
        Spacer(1, 5),
    ]

    doc.build(header + story, onFirstPage=footer, onLaterPages=footer)
    print(f"Created: {path}")


# -------------------------------------------------------------------
# NT-HR-001 — EMPLOYEE HANDBOOK
# -------------------------------------------------------------------

def employee_handbook():
    story = [
        P("1. Purpose", H1),
        P("The Novatrix Technologies Employee Handbook provides a common reference for workplace expectations, employee responsibilities, communication standards, attendance, conduct, confidentiality, and general employment practices."),
        P("2. About Novatrix Technologies", H1),
        P("Novatrix Technologies Pvt. Ltd. is a technology services company delivering software engineering, data analytics, cloud solutions, automation, and technology consulting services. The company operates offices in Bengaluru, Chennai, Hyderabad, and Pune."),
        P("Novatrix aims to maintain a professional, inclusive, collaborative, and technology-driven workplace."),
        P("3. Working Hours", H1),
        P("Standard working hours are 9:30 AM to 6:30 PM, Monday through Friday, unless a team, project, shift, client requirement, or approved work arrangement specifies otherwise."),
        P("Employees are expected to be available during agreed working hours and to communicate planned changes in availability to their manager."),
        P("4. Attendance and Punctuality", H1),
        *bullets([
            "Employees should report to work on time and remain available during scheduled hours.",
            "Unexpected absence or significant delay should be communicated to the reporting manager as soon as reasonably possible.",
            "Attendance requirements may vary for shift-based, customer-facing, or project-specific roles.",
            "Leave and work-from-home requests must follow the applicable company policy."
        ]),
        P("5. Employee Identification", H1),
        P("Every employee is assigned a unique employee ID. Employees must use the assigned ID when accessing employee services, submitting internal requests, or completing company processes where identification is required."),
        P("6. Professional Conduct", H1),
        *bullets([
            "Treat colleagues, customers, vendors, and visitors with respect.",
            "Communicate professionally in person, by email, and through collaboration tools.",
            "Support a collaborative and inclusive working environment.",
            "Follow company policies, procedures, and reasonable management instructions.",
            "Protect company, customer, and employee information.",
            "Use company facilities and equipment responsibly.",
            "Do not engage in harassment, discrimination, intimidation, threats, violence, or other inappropriate workplace behavior."
        ]),
        P("7. Communication", H1),
        P("Employees should use approved company communication channels for business discussions. Important decisions, approvals, and commitments should be documented through appropriate company systems when required."),
        P("8. Confidentiality", H1),
        P("Employees must protect confidential company, customer, financial, technical, employee, and business information. Confidential information must only be shared with authorized people who have a legitimate business need."),
        P("9. Performance and Development", H1),
        P("Employees are expected to understand their responsibilities, participate in performance discussions, complete required training, and work with their managers on professional development goals."),
        P("10. Workplace Responsibilities", H1),
        *bullets([
            "Maintain a safe and professional work environment.",
            "Protect company property and information.",
            "Follow IT, information security, leave, expense, travel, and workplace policies.",
            "Report suspected policy violations or security incidents through the appropriate channel."
        ]),
        P("11. Policy Compliance", H1),
        P("Employees are responsible for understanding policies applicable to their role. Where two policies address the same topic, the more specific applicable policy should be followed. Statutory requirements and approved employment terms take precedence where applicable."),
        P("12. Quick Reference", H1),
        make_table([
            ["Topic", "Reference"],
            ["Standard working hours", "9:30 AM – 6:30 PM, Monday–Friday"],
            ["Employee identification", "Unique employee ID"],
            ["General conduct", "Respectful, professional, collaborative"],
            ["Confidential information", "Share only with authorized persons"],
            ["Security incidents", "Report promptly through the approved channel"],
        ], [55*mm, 115*mm]),
        P("13. Frequently Asked Questions", H1),
        P("Q: What are the standard working hours?", FAQ_Q),
        P("A: 9:30 AM to 6:30 PM, Monday through Friday, unless an approved arrangement or role requirement states otherwise."),
        P("Q: Who should I contact if I am unexpectedly absent?", FAQ_Q),
        P("A: Inform your reporting manager as soon as reasonably possible."),
    ]
    build_pdf("Employee_Handbook.pdf", "NT-HR-001", "Employee Handbook", "Human Resources", story)


# -------------------------------------------------------------------
# NT-HR-002 — LEAVE POLICY
# -------------------------------------------------------------------

def leave_policy():
    story = [
        P("1. Purpose", H1),
        P("This policy explains the leave categories available to eligible employees, basic entitlement, request procedures, approval considerations, and leave balance rules."),
        P("2. Leave Entitlement", H1),
        make_table([
            ["Leave Type", "Annual Entitlement", "Typical Use"],
            ["Casual Leave", "12 days", "Short personal or planned absences"],
            ["Earned Leave", "18 days", "Planned vacation or extended leave"],
            ["Sick Leave", "12 days", "Illness or health-related absence"],
        ], [45*mm, 45*mm, 80*mm]),
        P("3. Casual Leave", H1),
        P("Employees may use up to 12 casual leave days per calendar year, subject to eligibility, approval, and applicable company rules."),
        P("4. Earned Leave", H1),
        P("Employees may use up to 18 earned leave days per calendar year. Planned earned leave should normally be requested at least 2 working days before the intended absence."),
        P("5. Sick Leave", H1),
        P("Employees may use up to 12 sick leave days per calendar year for illness or health-related absence, subject to applicable procedures."),
        P("6. Leave Request and Approval", H1),
        *bullets([
            "Submit the leave request through the approved company process.",
            "Provide the dates and type of leave requested.",
            "Managers consider team availability, project deadlines, business requirements, and operational continuity.",
            "Approval of a leave request is separate from the employee's available leave balance.",
            "An available balance does not automatically guarantee approval."
        ]),
        P("7. Unplanned Absence", H1),
        P("If an employee cannot report to work unexpectedly, the employee should notify the reporting manager as soon as reasonably possible and complete the required leave process afterward."),
        P("8. Half-Day Leave", H1),
        P("Where the leave system supports half-day leave, a half-day is recorded as 0.5 leave day."),
        P("9. Carry Forward", H1),
        P("Unused earned leave may be carried forward according to applicable company rules. Casual and sick leave generally do not carry forward unless specifically approved or required by applicable law."),
        P("10. Example", H1),
        P("An employee has 8 casual leave days, 12 earned leave days, and 10 sick leave days remaining. If the employee plans a five-day vacation, the employee may request five earned leave days, subject to manager approval and business requirements."),
        P("11. Frequently Asked Questions", H1),
        P("Q: How much casual leave is available each year?", FAQ_Q),
        P("A: 12 days per year, subject to eligibility and applicable rules."),
        P("Q: How much earned leave is available each year?", FAQ_Q),
        P("A: 18 days per year."),
        P("Q: Can I take leave simply because I have enough balance?", FAQ_Q),
        P("A: No. Leave balance and leave approval are separate concepts."),
        P("Q: How early should I request planned earned leave?", FAQ_Q),
        P("A: Normally at least 2 working days in advance."),
    ]
    build_pdf("Leave_Policy.pdf", "NT-HR-002", "Leave Policy", "Human Resources", story)


# -------------------------------------------------------------------
# NT-FIN-001 — TRAVEL POLICY
# -------------------------------------------------------------------

def travel_policy():
    story = [
        P("1. Purpose", H1),
        P("This policy establishes requirements for business travel, including approval, transportation, accommodation, meals, customer entertainment, documentation, and submission of travel expenses."),
        P("2. Travel Approval", H1),
        P("Business travel requires manager approval before travel begins. The request should include destination, business purpose, travel dates, estimated expenses, and relevant customer or project details."),
        P("3. Transportation", H1),
        *bullets([
            "Domestic air travel should normally be booked in economy class.",
            "Business class requires exceptional business justification and senior approval.",
            "Rail, public transit, approved taxis, app-based transport, and other reasonable local business transportation may be used when appropriate.",
            "Travel arrangements should balance business needs, cost, safety, and reasonable convenience."
        ]),
        P("4. Hotel Limits", H1),
        make_table([
            ["Employee Level", "Maximum Hotel Rate / Night"],
            ["Associate", "INR 3,000"],
            ["Senior Associate", "INR 4,000"],
            ["Manager", "INR 5,000"],
            ["Senior Manager", "INR 6,000"],
        ], [80*mm, 90*mm]),
        P("5. International Travel", H1),
        P("International business travel requires manager approval and relevant business leadership approval before booking."),
        P("6. Meals", H1),
        P("Employees may claim reasonable business meals incurred during approved business travel, subject to applicable expense limits and documentation requirements."),
        P("7. Customer Entertainment", H1),
        P("Customer entertainment requires prior approval. The business purpose, participants, and expected cost should be documented when requesting approval."),
        P("8. Travel Expense Submission", H1),
        P("Travel expenses should normally be submitted within 15 days after the trip. Receipts or supporting documentation must be provided where required."),
        P("9. Non-Reimbursable Travel Expenses", H1),
        *bullets([
            "Personal shopping",
            "Unrelated entertainment",
            "Expenses for family members",
            "Alcohol",
            "Fines or penalties",
            "Personal upgrades",
            "Personal travel extensions"
        ]),
        P("10. Example", H1),
        P("A Senior Associate stays at a hotel costing INR 3,800 per night. The standard Senior Associate limit is INR 4,000 per night, so the hotel rate is within the stated limit, subject to normal approval and documentation requirements."),
        P("11. Frequently Asked Questions", H1),
        P("Q: What is the hotel limit for a Manager?", FAQ_Q),
        P("A: INR 5,000 per night."),
        P("Q: Can I book business class for domestic travel?", FAQ_Q),
        P("A: Domestic travel should normally be economy class. Business class requires exceptional justification and senior approval."),
        P("Q: When should travel expenses normally be submitted?", FAQ_Q),
        P("A: Within 15 days after the trip."),
    ]
    build_pdf("Travel_Policy.pdf", "NT-FIN-001", "Business Travel Policy", "Finance", story)


# -------------------------------------------------------------------
# NT-FIN-002 — REIMBURSEMENT POLICY
# -------------------------------------------------------------------

def reimbursement_policy():
    story = [
        P("1. Purpose", H1),
        P("This policy defines eligible employee reimbursements, documentation requirements, approval flow, expense limits, and non-reimbursable expenses."),
        P("2. Eligible Expenses", H1),
        *bullets([
            "Approved business travel",
            "Customer meetings",
            "Approved business meals",
            "Office supplies",
            "Approved professional subscriptions",
            "Business communication",
            "Other expenses specifically approved for business use"
        ]),
        P("3. Employee Responsibility", H1),
        *bullets([
            "The expense must have a legitimate business purpose.",
            "The amount should be reasonable.",
            "Required receipts and supporting documents must be retained.",
            "The claim must be submitted within the applicable deadline.",
            "Required manager or department approvals must be obtained."
        ]),
        P("4. Submission Deadline", H1),
        P("Reimbursement claims should normally be submitted within 15 days of the expense or applicable business event."),
        P("5. Receipt Information", H1),
        P("Where a receipt is required, it should clearly show the vendor, date, amount, and description or nature of the expense."),
        P("6. Approval Flow", H1),
        P("The standard approval sequence is Reporting Manager → Department Head → Finance, subject to the expense type and company workflow."),
        P("7. Standard Limits", H1),
        make_table([
            ["Expense Category", "Standard Limit"],
            ["Business meal", "INR 1,000 per person"],
            ["Local business transportation", "INR 1,500 per day"],
            ["Office supplies", "INR 5,000 per purchase"],
            ["Professional subscription", "Prior approval required"],
        ], [80*mm, 90*mm]),
        P("8. Non-Reimbursable Expenses", H1),
        *bullets([
            "Personal purchases",
            "Personal entertainment",
            "Fines and penalties",
            "Unauthorized subscriptions",
            "Expenses for family members",
            "Personal travel",
            "Unapproved upgrades"
        ]),
        P("9. Duplicate Claims", H1),
        P("Employees must not submit the same expense more than once or claim an expense that has already been reimbursed through another process."),
        P("10. Finance Review", H1),
        P("Finance reviews claims for completeness, eligibility, documentation, approval, and compliance with applicable limits."),
        P("11. Example", H1),
        P("An employee purchases approved office supplies costing INR 3,500. The standard office-supply limit is INR 5,000 per purchase. The expense may be reimbursable if it is business-related, authorized, properly documented, and submitted within the required period."),
        P("12. Frequently Asked Questions", H1),
        P("Q: What is the business meal limit?", FAQ_Q),
        P("A: INR 1,000 per person."),
        P("Q: What is the office supplies limit?", FAQ_Q),
        P("A: INR 5,000 per purchase."),
        P("Q: How long do I have to submit a reimbursement claim?", FAQ_Q),
        P("A: Normally 15 days from the expense or applicable business event."),
    ]
    build_pdf("Reimbursement_Policy.pdf", "NT-FIN-002", "Employee Reimbursement Policy", "Finance", story)


# -------------------------------------------------------------------
# NT-HR-003 — WORK FROM HOME
# -------------------------------------------------------------------

def wfh_policy():
    story = [
        P("1. Purpose", H1),
        P("This policy defines the conditions under which eligible employees may work from home and the responsibilities that apply during remote work."),
        P("2. WFH Allowance", H1),
        P("Eligible employees may work from home for up to 8 days per calendar month, subject to manager approval and business requirements."),
        P("The 8-day limit is a maximum allowance and is not an automatic entitlement."),
        P("3. Eligibility", H1),
        *bullets([
            "Role and job responsibilities",
            "Team and project requirements",
            "Manager approval",
            "Business continuity needs",
            "Operational or customer requirements"
        ]),
        P("4. Approval", H1),
        P("Employees should obtain approval before working from home. Managers may require office presence when business, project, collaboration, customer, or operational needs require it."),
        P("5. Working Hours", H1),
        P("The standard working hours remain 9:30 AM to 6:30 PM, Monday through Friday, unless another approved schedule applies."),
        P("6. Employee Responsibilities", H1),
        *bullets([
            "Attend required meetings.",
            "Remain reachable through approved communication channels.",
            "Maintain a suitable workspace.",
            "Complete assigned work and meet agreed deadlines.",
            "Protect company information and equipment."
        ]),
        P("7. Security Requirements", H1),
        *bullets([
            "Use approved company devices and systems.",
            "Protect passwords and authentication credentials.",
            "Do not share company devices with unauthorized people.",
            "Use approved systems for company information.",
            "Follow the IT and Information Security Policies."
        ]),
        P("8. WFH and Leave", H1),
        P("The same day cannot be recorded as both leave and work from home."),
        P("9. Example", H1),
        P("If an employee has already used 6 WFH days in a month, the employee may request up to 2 additional WFH days, subject to approval and business requirements."),
        P("10. Frequently Asked Questions", H1),
        P("Q: What is the maximum number of WFH days per month?", FAQ_Q),
        P("A: Up to 8 days for eligible employees, subject to approval."),
        P("Q: Is 8 days an automatic entitlement?", FAQ_Q),
        P("A: No. It is a maximum allowance subject to eligibility, approval, and business needs."),
        P("Q: Can the same day be marked as both leave and WFH?", FAQ_Q),
        P("A: No."),
    ]
    build_pdf("Work_From_Home_Policy.pdf", "NT-HR-003", "Work From Home Policy", "Human Resources", story)


# -------------------------------------------------------------------
# NT-IT-001 — IT ACCEPTABLE USE
# -------------------------------------------------------------------

def it_policy():
    story = [
        P("1. Purpose", H1),
        P("This policy establishes acceptable use requirements for Novatrix Technologies information technology resources, company devices, software, credentials, data, and network services."),
        P("2. Company Devices", H1),
        P("Company IT assets may include laptops, desktops, monitors, mobile phones, headsets, and other equipment assigned for business use."),
        P("Device assignment is based on role, business requirements, security requirements, and operational needs."),
        P("3. Lost or Stolen Devices", H1),
        P("Lost or stolen company devices must be reported to the IT Helpdesk immediately. Employees should provide relevant information about when and where the device was lost or stolen."),
        P("4. Software", H1),
        *bullets([
            "Only authorized software may be installed on company devices.",
            "Employees must not install unlicensed or unauthorized software.",
            "Software required for business work should be obtained through approved channels.",
            "Employees should not disable security controls to install or run software."
        ]),
        P("5. Passwords and Authentication", H1),
        *bullets([
            "Passwords must be kept confidential.",
            "Employees should use strong passwords and follow company authentication requirements.",
            "Passwords must not be shared with colleagues or external parties.",
            "Credentials must not be stored in publicly accessible locations.",
            "Multi-factor authentication must be used where required."
        ]),
        P("6. Company Data", H1),
        P("Company data should be stored, processed, and shared only through approved systems and services."),
        P("7. Personal Use", H1),
        P("Limited personal use of company IT resources may be permitted when it does not interfere with work, create security risks, violate policy, consume excessive resources, or involve illegal activity."),
        P("8. Removable Storage", H1),
        P("Removable storage should be used only for legitimate business purposes and must comply with applicable security controls."),
        P("9. Returning IT Assets", H1),
        P("Employees must return company devices and other IT assets when employment ends, equipment is replaced, a role changes, IT requests return, or the asset is no longer required."),
        P("10. Example", H1),
        P("If an employee loses a company laptop while traveling, the employee must immediately contact the IT Helpdesk and follow the incident-reporting process."),
        P("11. Frequently Asked Questions", H1),
        P("Q: Can I install any software I want?", FAQ_Q),
        P("A: No. Software installed on company devices must be authorized and appropriately licensed."),
        P("Q: What should I do if my company laptop is stolen?", FAQ_Q),
        P("A: Report it to the IT Helpdesk immediately and follow the security incident process."),
    ]
    build_pdf("IT_Acceptable_Use_Policy.pdf", "NT-IT-001", "IT Acceptable Use Policy", "Information Technology", story)


# -------------------------------------------------------------------
# NT-SEC-001 — INFORMATION SECURITY
# -------------------------------------------------------------------

def security_policy():
    story = [
        P("1. Purpose", H1),
        P("This policy defines basic information security responsibilities for employees who access Novatrix Technologies systems, data, devices, and services."),
        P("2. Confidential Information", H1),
        *bullets([
            "Customer information",
            "Source code",
            "Business plans",
            "Financial information",
            "Employee information",
            "Credentials",
            "Product designs",
            "Internal reports",
            "Contracts"
        ]),
        P("3. Passwords and MFA", H1),
        P("Employees must keep passwords confidential and use multi-factor authentication where required. Credentials must never be shared with unauthorized people."),
        P("4. Phishing Awareness", H1),
        P("Employees should be cautious of unexpected emails, links, attachments, login requests, password-reset messages, payment requests, and other suspicious communications."),
        P("5. Access to Confidential Data", H1),
        P("Confidential information may only be accessed or shared by authorized individuals with a legitimate business need."),
        P("6. Remote Work Security", H1),
        *bullets([
            "Use approved company devices.",
            "Protect the physical workspace from unauthorized viewing.",
            "Avoid discussing confidential information where unauthorized people may hear it.",
            "Use approved systems and authentication controls."
        ]),
        P("7. Security Incidents", H1),
        P("Examples of security incidents include lost laptops, stolen devices, accidental data sharing, suspicious emails, unauthorized account access, malware, and exposed credentials."),
        P("Employees must report suspected incidents promptly. Prompt reporting is more important than attempting to independently investigate or resolve the issue."),
        P("8. Public Wi-Fi", H1),
        P("Employees should avoid accessing sensitive company systems over public Wi-Fi unless approved security controls are active."),
        P("9. Clean Desk", H1),
        P("Employees should avoid leaving confidential documents, passwords, devices, or other sensitive information exposed in shared or public areas."),
        P("10. Example", H1),
        P("If an employee accidentally sends confidential information to the wrong external email address, the employee should report the incident immediately rather than attempting to resolve it independently."),
        P("11. Frequently Asked Questions", H1),
        P("Q: What should I do if I receive a suspicious password-reset email?", FAQ_Q),
        P("A: Treat it as potentially suspicious and report it through the approved security incident-reporting channel."),
        P("Q: What if I accidentally send confidential data to the wrong person?", FAQ_Q),
        P("A: Report the incident immediately. Prompt reporting is more important than independent resolution."),
    ]
    build_pdf("Information_Security_Policy.pdf", "NT-SEC-001", "Information Security Policy", "Information Security", story)


# -------------------------------------------------------------------
# NT-HR-004 — ONBOARDING GUIDE
# -------------------------------------------------------------------

def onboarding_guide():
    story = [
        P("1. Purpose", H1),
        P("This guide provides a practical overview of the employee onboarding process at Novatrix Technologies, from pre-joining activities through the first month."),
        P("2. Before Joining", H1),
        *bullets([
            "Complete employment documentation.",
            "Complete required identity and address verification.",
            "Provide banking and tax documentation.",
            "Provide emergency contact information.",
            "Complete required declarations and forms."
        ]),
        P("3. First Day", H1),
        *bullets([
            "Attend HR orientation.",
            "Activate employee identification and required accounts.",
            "Complete IT setup and receive assigned equipment.",
            "Attend the initial security briefing.",
            "Meet the reporting manager.",
            "Meet the immediate team."
        ]),
        P("4. Employee ID", H1),
        P("Every employee receives a unique employee ID. The ID is used for internal processes and employee services."),
        P("5. IT Setup", H1),
        P("Depending on role requirements, IT setup may include a laptop, company email, collaboration tools, VPN or approved remote-access services, and required business software."),
        P("6. Security Training", H1),
        *bullets([
            "Password and authentication practices",
            "Phishing awareness",
            "Confidential information handling",
            "Device security",
            "Security incident reporting",
            "Remote-work security"
        ]),
        P("7. Manager Introduction", H1),
        P("The reporting manager should explain the employee's responsibilities, current projects, team processes, communication expectations, and initial objectives."),
        P("8. First Week", H1),
        *bullets([
            "Complete mandatory training.",
            "Understand role responsibilities.",
            "Learn required business tools.",
            "Review relevant company policies.",
            "Meet key team members and stakeholders.",
            "Discuss initial goals."
        ]),
        P("9. First Month", H1),
        P("During the first month, employees should become familiar with team processes, assigned projects, company systems, applicable policies, and performance expectations."),
        P("10. IT Asset Responsibility", H1),
        P("Employees are responsible for protecting assigned IT equipment and reporting loss, theft, damage, or security concerns promptly."),
        P("11. Policies to Review", H1),
        *bullets([
            "Employee Handbook",
            "Leave Policy",
            "IT Acceptable Use Policy",
            "Information Security Policy",
            "Work From Home Policy"
        ]),
        P("12. Example", H1),
        P("A newly hired Data Analyst may receive a company laptop, email account, collaboration tools, access to approved analytics systems, and role-specific software after the required approvals and security controls are completed."),
        P("13. Frequently Asked Questions", H1),
        P("Q: What should I complete before joining?", FAQ_Q),
        P("A: Required employment documents, verification information, banking and tax details, emergency contact information, and declarations."),
        P("Q: Who explains my initial responsibilities?", FAQ_Q),
        P("A: The reporting manager should explain responsibilities, projects, team processes, communication expectations, and initial objectives."),
    ]
    build_pdf("Employee_Onboarding_Guide.pdf", "NT-HR-004", "Employee Onboarding Guide", "Human Resources", story)


# -------------------------------------------------------------------
# NT-ADM-001 — OFFICE GUIDELINES
# -------------------------------------------------------------------

def office_guidelines():
    story = [
        P("1. Purpose", H1),
        P("These guidelines establish common expectations for using Novatrix Technologies offices, shared facilities, meeting rooms, access systems, and common areas."),
        P("2. Office Locations", H1),
        make_table([
            ["City", "Office"],
            ["Bengaluru", "Novatrix Campus, Whitefield"],
            ["Chennai", "Novatrix Campus, OMR"],
            ["Hyderabad", "Novatrix Campus, Hitech City"],
            ["Pune", "Novatrix Campus, Hinjewadi"],
        ], [55*mm, 115*mm]),
        P("3. Office Hours", H1),
        P("Standard office hours are 9:30 AM to 6:30 PM, Monday through Friday, unless another schedule applies to the employee's role."),
        P("4. Access Cards", H1),
        P("Employees must use assigned access cards for controlled areas and must not allow unauthorized people to enter restricted areas using their credentials or access card."),
        P("5. Meeting Rooms", H1),
        *bullets([
            "Book meeting rooms through the approved reservation system.",
            "Cancel unused reservations when possible.",
            "Do not unnecessarily block rooms for long periods.",
            "Leave meeting rooms clean and ready for the next group."
        ]),
        P("6. Cafeteria and Common Areas", H1),
        P("Employees should maintain cleanliness in cafeterias, kitchens, lounges, and other shared areas. Waste should be disposed of in designated locations."),
        P("7. Workspace", H1),
        P("Employees should maintain a clean and organized workspace and avoid leaving confidential documents or equipment unattended in shared areas."),
        P("8. Visitors", H1),
        P("Visitors must follow the office visitor-registration and access procedures. Employees hosting visitors are responsible for following applicable visitor requirements."),
        P("9. Parking", H1),
        P("Employees should use designated parking areas and follow building or campus parking rules."),
        P("10. Workplace Conduct", H1),
        *bullets([
            "Respect colleagues and visitors.",
            "Avoid excessive noise in shared work areas.",
            "Keep shared spaces clean.",
            "Follow safety instructions.",
            "Respect meeting-room reservations.",
            "Follow access-control requirements."
        ]),
        P("11. Emergencies", H1),
        P("During emergencies, employees should follow instructions from building administration, security personnel, and emergency response teams."),
        P("12. Example", H1),
        P("If an employee finishes a meeting early, the employee should release the meeting-room reservation when the reservation system allows it so another team can use the room."),
        P("13. Frequently Asked Questions", H1),
        P("Q: Can I allow a visitor to enter a controlled area using my access card?", FAQ_Q),
        P("A: No. Visitors must follow the approved registration and access procedure."),
        P("Q: What should I do when I finish using a meeting room early?", FAQ_Q),
        P("A: Cancel or release the reservation when the system supports it."),
    ]
    build_pdf("Office_Guidelines.pdf", "NT-ADM-001", "Office Guidelines", "Administration & Facilities", story)


# -------------------------------------------------------------------
# NT-FIN-003 — EXPENSE POLICY
# -------------------------------------------------------------------

def expense_policy():
    story = [
        P("1. Purpose", H1),
        P("This policy defines what qualifies as a business expense, standard limits, documentation requirements, approval requirements, and prohibited expenses."),
        P("2. Business Expense Definition", H1),
        P("A business expense must have a legitimate business purpose and must be reasonable, authorized, appropriately documented, and incurred for company business."),
        P("3. Expense Categories", H1),
        *bullets([
            "Travel",
            "Hotel",
            "Food",
            "Transportation",
            "Office Supplies",
            "Training",
            "Professional Subscription"
        ]),
        P("4. Standard Limits", H1),
        make_table([
            ["Category", "Limit / Requirement"],
            ["Business meals", "INR 1,000 per person"],
            ["Office supplies", "INR 5,000 per purchase"],
            ["Professional subscriptions", "Prior approval required"],
            ["Travel and hotel", "Subject to Travel Policy"],
        ], [80*mm, 90*mm]),
        P("5. Documentation", H1),
        P("Expense documentation should identify the vendor, date, amount, and nature of the expense. Additional supporting information may be required depending on the category."),
        P("6. Submission Deadline", H1),
        P("Expenses should normally be submitted within 15 days of the expense date."),
        P("7. Approval", H1),
        P("The standard approval flow is Reporting Manager → Department Head → Finance, subject to the expense type and applicable workflow."),
        P("8. Prohibited Expenses", H1),
        *bullets([
            "Personal purchases",
            "Personal entertainment",
            "Alcohol",
            "Fines and penalties",
            "Unauthorized software",
            "Personal subscriptions",
            "Family expenses",
            "Personal travel"
        ]),
        P("9. Duplicate Expenses", H1),
        P("Employees must not submit duplicate expenses or claim the same expense through multiple reimbursement processes."),
        P("10. Example", H1),
        P("An employee attends a customer meeting involving three participants and incurs a business meal expense of INR 3,200. The applicable per-person limit and participant count should be checked against the expense documentation and approval requirements before reimbursement."),
        P("11. Frequently Asked Questions", H1),
        P("Q: What is the standard business meal limit?", FAQ_Q),
        P("A: INR 1,000 per person."),
        P("Q: Do professional subscriptions require approval?", FAQ_Q),
        P("A: Yes. Prior approval is required."),
        P("Q: How quickly should expenses be submitted?", FAQ_Q),
        P("A: Normally within 15 days of the expense date."),
    ]
    build_pdf("Expense_Policy.pdf", "NT-FIN-003", "Expense Policy", "Finance", story)


# -------------------------------------------------------------------
# NT-HR-005 — BENEFITS GUIDE
# -------------------------------------------------------------------

def benefits_guide():
    story = [
        P("1. Purpose", H1),
        P("This guide provides an overview of employee benefits available at Novatrix Technologies. Actual eligibility and benefit terms depend on the employee's employment status, location, applicable plan, provider terms, and law."),
        P("2. Health Insurance", H1),
        P("Eligible full-time employees may receive health insurance coverage. Depending on the applicable plan, coverage may include employees and eligible dependents, hospitalization, selected procedures, and other covered services."),
        P("Enrollment must be completed within the period communicated by Human Resources or the insurance provider."),
        P("3. Wellness Programs", H1),
        *bullets([
            "Health-awareness activities",
            "Fitness initiatives",
            "Wellness sessions",
            "Employee assistance resources"
        ]),
        P("4. Learning and Development", H1),
        *bullets([
            "Technical training",
            "Professional certifications",
            "Workshops",
            "Leadership development",
            "Role-related skill courses"
        ]),
        P("5. Certification Support", H1),
        P("Employees may be eligible for support toward approved professional certifications, subject to the applicable learning and development process and approval requirements."),
        P("6. Employee Assistance", H1),
        P("Employees may have access to assistance resources communicated through Human Resources or approved benefit providers."),
        P("7. Parental Benefits", H1),
        P("Parental benefits are provided according to applicable company policy, employment terms, and applicable law."),
        P("8. Retirement and Statutory Benefits", H1),
        P("Retirement and statutory benefits are administered according to applicable employment terms, local regulations, and statutory requirements."),
        P("9. Benefit Eligibility", H1),
        *bullets([
            "Employment type",
            "Joining date",
            "Work location",
            "Employee grade or level",
            "Applicable regulations",
            "Insurance or benefit-provider terms"
        ]),
        P("10. Benefit Changes", H1),
        P("Benefit plans, providers, coverage, eligibility conditions, and program details may change. Human Resources will communicate material changes through approved company channels."),
        P("11. Example", H1),
        P("If an employee needs information about whether a particular medical procedure is covered, the employee should review the applicable benefit plan or contact Human Resources. The actual insurance plan and provider terms take precedence over this summary."),
        P("12. Important Note", H1),
        P("This guide is a general summary. Actual plan documents, statutory requirements, employment terms, and provider conditions take precedence where applicable."),
        P("13. Frequently Asked Questions", H1),
        P("Q: Are all employees automatically eligible for every benefit?", FAQ_Q),
        P("A: No. Eligibility depends on employment type, joining date, location, grade, regulations, and applicable provider or plan terms."),
        P("Q: Where can I confirm health-insurance coverage?", FAQ_Q),
        P("A: Review the applicable plan documents or contact Human Resources."),
    ]
    build_pdf("Benefits_Guide.pdf", "NT-HR-005", "Employee Benefits Guide", "Human Resources", story)


# -------------------------------------------------------------------
# CREATE ALL DOCUMENTS
# -------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Creating {COMPANY} policy documents...")
    employee_handbook()
    leave_policy()
    travel_policy()
    reimbursement_policy()
    wfh_policy()
    it_policy()
    security_policy()
    onboarding_guide()
    office_guidelines()
    expense_policy()
    benefits_guide()

    print("\nAll policy documents created successfully.")
    print(f"Output folder: {OUTPUT_DIR.resolve()}")
