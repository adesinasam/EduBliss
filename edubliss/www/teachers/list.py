import frappe
from frappe import _

no_cache = 1

def get_context(context):

    # login
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)

    context.current_user = frappe.get_doc("User", frappe.session.user)

    # nav
    context.active_route = "teachers"
    context.active_subroute = "teacher_list"

    edubliss_session = frappe.call('edubliss.api.get_edubliss_user_session')
    if edubliss_session:
        context.edublisession = edubliss_session
        company = edubliss_session.school
    else:
        context.edublisession = _("Welcome")  # Assuming welcome is a placeholder message
        company = None

    context.companys = frappe.call('edubliss.api.get_company')
    context.acadyears = frappe.call('edubliss.api.get_academic_year')
    context.acadterms = frappe.call('edubliss.api.get_academic_term')
    context.teachers = frappe.call('edubliss.api.get_teachers', company=company)

    # Count
    if company:
        context.student_count = frappe.db.count('Student', filters={'custom_school': company})
    else:
        context.student_count = frappe.db.count('Student')

    context.course_count = frappe.db.count('LMS Course')
    context.teacher_count = len(frappe.call('edubliss.api.get_teachers', company=company))

    return context