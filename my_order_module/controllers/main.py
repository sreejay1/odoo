# from odoo import http
# from odoo.http import request
# import logging

# _logger = logging.getLogger(__name__)

# # class MyOrderController(http.Controller):
# #     @http.route('/shop/orderconfirmede', type='http', auth='public', website=True)
# #     def order_placed(self, **kwargs):
# #         return "Order confirmation page is accessible."
# class MyOrderController(http.Controller):

#     @http.route('/shop/orderconfirmed', type='http', auth="public", website=True)
#     def order_placed(self, **kwargs):
#         try:
#             # Get the current website
#             website = request.env['website'].get_current_website()

#             # Get the current order
#             order = website.sale_get_order()

#             # Check if order is found
#             if not order:
#                 return request.redirect('/shop/payment')  # Redirect if order not found

#             # Mark the order as confirmed
#             order.sudo().action_confirm()

#             # Send email to admin using the email template
#             template_id = request.env.ref('my_order_module.email_template_order')
#             if template_id:
#                 # Ensure that the order is passed as the context object
#                 template_id.sudo().send_mail(order.id, force_send=True)

#             # Clear the session after order is confirmed
#             request.website.sale_reset()

#             # Render the order confirmation modal view and pass the order to the template
#             return request.render('my_order_module.order_confirmation_modal', {
#                 'sale_order': order,
#                 'website': website,
#             })

#         except Exception as e:
#             _logger.error("Error in order_placed: %s", str(e))
#             return request.render('my_order_module.order_confirmation_modal', {
#                 'sale_order': None,
#                 'website': website,
#             })

import logging
from odoo import http, models, fields
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    admin_emails = fields.Char(compute='_compute_admin_emails')

    def _compute_admin_emails(self):
        admin_users = self.env['res.users'].search([('groups_id', '=', self.env.ref('base.group_system').id)])
        self.admin_emails = ','.join(user.partner_id.email for user in admin_users if user.partner_id.email)


class MyOrderController(http.Controller):
    @http.route('/shop/orderconfirmed', type='http', auth="public", website=True)
    def order_placed(self, **kwargs):
        try:
            # Get the current website
            website = request.env['website'].get_current_website()

            # Get the current order
            order = website.sale_get_order()

            # Check if order is found
            if not order:
                return request.redirect('/shop/payment')  # Redirect if order not found

            # Mark the order as confirmed
            order.sudo().action_confirm()

            # Log order details for debugging
            _logger.info("Order ID: %s", order.id)
            _logger.info("Order Amount Total: %s", order.amount_total)
            _logger.info("Order Name: %s", order.name)
            _logger.info("Shipping Address: %s", order.partner_shipping_id.contact_address)

            # Send email to all admin users using the email template
            template_id = request.env.ref('my_order_module.email_template_order')
            if template_id:
                _logger.info("Email template found: %s", template_id.id)

                # Pass `admin_emails` directly to the email template
                order.sudo().admin_emails = order.admin_emails  # Make sure admin_emails is populated
                mail_id = template_id.sudo().send_mail(order.id, force_send=True)
                
                if mail_id:
                    _logger.info("Email sent successfully. Mail ID: %s", mail_id)
                else:
                    _logger.error("Email sending failed.")
            else:
                _logger.error("Email template not found.")

            # Clear the session after order is confirmed
            request.website.sale_reset()

            # Render the order confirmation modal view and pass the order to the template
            response = request.render('my_order_module.order_confirmation_modal', {
                'sale_order': order,
                'website': website,
            })

            # Add CORS headers to the response
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, DELETE, PUT'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

            return response

        except Exception as e:
            _logger.error("Error in order_placed: %s", str(e))
            response = request.render('my_order_module.order_confirmation_modal', {
                'sale_order': None,
                'website': website,
            })

            # Add CORS headers to the response
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, DELETE, PUT'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

            return response

