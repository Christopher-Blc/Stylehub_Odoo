from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    #para separar clientes StyleHub de otros contactos , osea solo salen los que tengan ese bool == true
    es_cliente_peluqueria = fields.Boolean(
        string="Es cliente de la peluqueria",
        default=False,
    )

    # VIP lo pide el enunciado, pero lo calcularemos cuando existan citas realizadas
    # stylehub_es_vip = fields.Boolean(string="VIP", compute="_compute_stylehub_es_vip", store=False)