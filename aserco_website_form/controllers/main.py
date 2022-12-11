import werkzeug

from odoo import http, fields, tools
from odoo.http import request
import datetime


class PortalUser(http.Controller):
    @http.route('/online_appointment', type='http', auth='public', website=True)
    def appointment_form(self, **kw):
        values = {}
        services = request.env["calendar.appointment.type"].sudo().search([])
        areas = []
        dates = []
        user_id = request.env.user
        user_partner_id = request.env["res.users"].search([('id', '=', user_id.id)]).partner_id.id
        philipines_id = request.env["res.country"].search([('name', '=', 'Philippines')])
        states = request.env["res.country.state"].search([('country_id', '=', philipines_id.id)])
        values.update({
            'services': services,
            'areas': areas,
            'dates': dates,
            'x_studio_customer_name_1': user_id.partner_id.name,
            'x_studio_contact_no':user_id.partner_id.mobile or user_id.partner_id.phone,
            'states':states,
            'partner_id': user_partner_id
        })
        return http.request.render("aserco_website_form.appointment_form", values)
    '''
       Added Function to Filter the area
    '''

    @http.route('/get_area', type='http', auth='public', website=True)
    def get_area(self, **kw):
        allocated_technician_line_64c6d = request.env['x_allocated_technician_line_64c6d']
        territory = request.env['x_territory']
        allocated_technician_line_64c6d = allocated_technician_line_64c6d.sudo().search(
            [('x_studio_service_type_id', '=', int(kw.get('service_type')))])

        area_list = ["<option value=' '>select...</option>"]
        for tec in allocated_technician_line_64c6d:
            territories = territory.sudo().search(
                [('x_studio_technicians', 'in', tec.x_allocated_technician_id.x_studio_user_id.id)])
            for territory in territories:
                option = "<option value= " + str(territory.id) + ">" + territory.x_name + "</option>"
                if option in area_list:
                    continue
                area_list.append(option)
            option_value = '%s' % ' '.join(map(str, area_list))
        return option_value

    '''
           Added Function to Filter the available dates
        '''

    @http.route('/get_available_dates', type='http', auth='public', website=True)
    def get_available_dates(self, **kw):
        territory = request.env['x_territory']
        allocated_technician_line_64c6d = request.env['x_allocated_technician_line_64c6d']
        allocated_technician_line_64c6d = allocated_technician_line_64c6d.sudo().search(
            [('x_studio_service_type_id', '=', int(kw.get('service_type'))), ('x_studio_time_slot', '=', kw.get('timeslot'))])
        allocated_technician_line_64c6d = allocated_technician_line_64c6d.filtered(lambda tl: tl.x_studio_available_allocation > 0)
        allocated_technician = allocated_technician_line_64c6d.mapped('x_allocated_technician_id')
        territory = territory.sudo().search([('id', '=', int(kw.get('area')))])
        territory_technicians = territory.mapped('x_studio_technicians')
        today = datetime.datetime.now()
        day_thirty = today + datetime.timedelta(days=30)
        allocated_technician = allocated_technician.filtered(lambda al: al.x_studio_user_id in territory_technicians and al.x_studio_date > today.date() and al.x_studio_date <= day_thirty.date())
        allocated_technician = allocated_technician.sorted(key=lambda s: s.x_studio_date)

        available_dates_list = ["<option value=' '>select...</option>"]
        for aloc_tec in allocated_technician:
            option = "<option value="+aloc_tec.x_studio_date.strftime("%Y-%m-%d")+">" + aloc_tec.x_studio_date.strftime("%d-%B-%Y") + "</option>"
            # option = "<option value=" + str(aloc_tec.id) + ">" + aloc_tec.x_studio_date.strftime("%d-%B-%Y") + "</option>"
            if option in available_dates_list:
                continue
            available_dates_list.append(option)
        option_value = '%s' % ' '.join(map(str, available_dates_list))
        return option_value
