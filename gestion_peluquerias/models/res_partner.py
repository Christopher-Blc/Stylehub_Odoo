from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    es_cliente_peluqueria = fields.Boolean(
        string="Es cliente de la peluqueria",
        default=False,
    )

    stylehub_num_citas_done = fields.Integer(
        string="Citas finalizadas",
        compute="_compute_stylehub_num_citas_done",
        store=False,
    )

    stylehub_es_vip = fields.Boolean(
        string="VIP",
        compute="_compute_stylehub_es_vip",
        store=False,
    )

    def _compute_stylehub_num_citas_done(self):
        Cita = self.env["stylehub.citas"]
        for partner in self:
            partner.stylehub_num_citas_done = Cita.search_count([
                ("cliente_id", "=", partner.id),
                ("state", "=", "done"),
            ])

    @api.depends("stylehub_num_citas_done")
    def _compute_stylehub_es_vip(self):
        for partner in self:
            partner.stylehub_es_vip = partner.stylehub_num_citas_done > 5
