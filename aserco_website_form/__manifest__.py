# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Aserco Website Form",
    "summary": """
        Use computed field as domain""",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": "",
    "website": "",
    "depends": ["web"],
    "data": [
        'views/template.xml',
    ],
    "assets": {
        "web.assets_backend": [
        ],
        "web.assets_frontend": [
            "/aserco_website_form/static/src/js/appointment.js",
        ],
    },
    "installable": True,
}
