{
    'name': 'Conformità CONAI',
    'version': '19.0.1.0.1',
    'summary': 'Contributo ambientale CONAI automatico sulle fatture clienti',
    'description': """
        Gestisce il contributo ambientale CONAI (Consorzio Nazionale Imballaggi)
        per le aziende italiane. Funzionalità:
        - Tassonomia completa di materiali e fasce (Plastica, Carta, Acciaio, Alluminio, Vetro, Legno)
        - Tariffe con decorrenza per data (più periodi)
        - Supporto per materiali compositi per prodotto
        - Gestione delle esenzioni a livello di partner
        - Generazione automatica delle righe CONAI sulle fatture clienti (solo partner italiani)
    """,
    'author': 'DigitalForce',
    'website': 'https://www.digitalforce.it',
    'license': 'OPL-1',
    'category': 'Accounting/Accounting',
    'depends': ['account', 'product', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'data/conai_material_data.xml',
        'data/conai_band_data.xml',
        'data/conai_rate_data.xml',
        'data/conai_product_data.xml',
        'data/conai_field_translations.xml',
        'views/conai_material_views.xml',
        'views/conai_band_views.xml',
        'views/conai_rate_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'views/conai_menu.xml',
        'wizard/conai_setup_wizard_views.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
