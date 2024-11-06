{
    'name': 'My Order Module',
    'summary': 'Module for managing order confirmations and notifications in Odoo eCommerce.',
    'version': '17.0.0',
    'license': 'LGPL-3',
    'category': 'eCommerce',
    'description': """
        My Order Module
        ==================
        This module enhances the Odoo eCommerce functionality by providing features for managing order confirmations and sending notifications to admin users. It includes:
        - Automatic order confirmation
        - Email notifications to admin users
        - Customizable order confirmation modal
    """,
    'depends': ['website', 'website_sale'],  # Ensure 'website' is listed
    'data': [
        'views/website_sale_templates.xml',
        'views/orderConfirmation.xml',
        'data/email_template.xml'
    ],
    'installable': True,
    'auto_install': False,
}
