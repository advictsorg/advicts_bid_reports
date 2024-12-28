# -*- coding: utf-8 -*-
{
    'name': "Advicts Bid Reports",
 
    'summary': """  Advicts Bid Reports""",

    'description': """
        Advicts Bid Reports
    """, 
    'author': "OmarFalih@advicts",
    'website': "https://www.advicts.com", 
    'version': '17.0.1.0',
 
     "depends": [
        "sale","account","purchase","purchase_requisition"
    ], 
    'data': [
            'reports/purchase_order_line_report_templates.xml',
            'views/bid_comparison_report_menu.xml',
            'data/report_paperformat.xml',
        ], 
    'assets': { 
    },
}
