# -*- coding: utf-8 -*-
#############################################################################
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'Open HRMS Core',
    'version': '19.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'summary': (
        'Open HRMS Odoo 19 core bundle for HR dashboard, employees, '
        'attendance, time off, expenses, recruitment, and reminders'
    ),
    'description': (
        'Open HRMS main module for Odoo 19 with dashboard, employees, documents, '
        'resignation, reminders, recruitment, attendance, time off, timesheets, '
        'expenses, and HR configuration helpers. Payroll-specific community '
        'addons are intentionally excluded for Enterprise payroll compatibility.'
    ),
    'author': 'Cybrosys Techno solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'live_test_url': 'https://hrms.easyinstance.com/web/login?redirect=/odoo/employees',
    'website': "https://www.openhrms.com",
    'depends': [
        'hr',
        'hr_gamification',
        'hr_employee_updation',
        'hr_recruitment',
        'hr_attendance',
        'hr_holidays',
        'hr_expense',
        'hr_leave_request_aliasing',
        'hr_timesheet',
        'oh_employee_creation_from_user',
        'oh_employee_documents_expiry',
        'hr_reward_warning',
        'hrms_dashboard',
        'hr_reminder'
    ],
    'data': [
        'views/menu_arrangement_view.xml',
        'views/hr_config_view.xml',
        'views/ir_ui_menu_views.xml',
        'views/hr_employee_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ohrms_core/static/src/css/menu_order_alphabets.css',
            'web/static/lib/jquery/jquery.js',
            'ohrms_core/static/src/js/appMenu.js',
            'ohrms_core/static/src/xml/link_view.xml',
            'ohrms_core/static/templates/side_bar.xml',
        ],
    },
    "external_dependencies": {"python": ["pandas"]},
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
