{
  "name": "RealEstate Management",
  "author": "SUDHANSU SEKHAR JENA",
  "license": "LGPL-3",
  "version": "17.0.1.1",
  "sequence": "1",
  "depends": [
    "mail", 
    "web", 
    "portal",
    "website"  # Keep this only if there are frontend (website) dependencies
  ],
  "data": [
    "security/security.xml",                # Security rules first
    "security/ir.model.access.csv",         # Access control next
    "views/website_menus.xml",              # Frontend menus
    "views/real_estate_menu.xml",           # Backend menus
    "views/forms.xml",                      # Form views (if any)
    "views/template.xml",                   # QWeb templates for backend
    "views/real_estate_sale_contracts_views.xml",
    "views/real_estate_bookings_views.xml",
    "views/real_estate_rent_contracts_views.xml",
    "views/real_estate_customers_views.xml",
    "views/real_estate_property_details_views.xml",
    "views/real_estate_connectivity_views.xml",
    "views/real_estate_features_views.xml",
    "views/real_estate_amenities.xml",
    "views/real_estate_property_types_views.xml",
    "views/real_estate_property_views.xml",
    "views/menu_visibility.xml",            # JavaScript-related logic last
  ],
  "assets": {
    "web.assets_backend": [
        "real_estate/static/src/xml/menu_visibility_component.xml",
    ],
    "web.assets_frontend_es6": [
        "real_estate/static/src/js/menu_visibility.js",  # Make sure it's under web.assets_frontend_es6
    ],
  },
  "application": True,                # Makes the module appear in Apps list
  "installable": True                 # Makes the module installable
}
