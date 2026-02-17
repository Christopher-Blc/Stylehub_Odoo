from odoo import models, fields, api

class stylehubEstilistas(models.Model):

    _name = "stylehub.estilistas"
    _description = "Estilistas que trabajan en la peluqueria."
    _rec_name = "nombre"#para que salga el nombre en vez del stylehub.estilistas 1 

    nombre = fields.Char(string="Nombre", required=True)
    activo = fields.Boolean(string="Activo", default=True)
    # permite ver las citas del estilista desde su formulario
    cita_ids = fields.One2many(
        comodel_name="stylehub.citas",
        inverse_name="estilista_id",
        string="Citas"
    )
    citas_realizadas = fields.Integer(string="Citas Realizadas", compute="_compute_citas_realizadas")
    imagen = fields.Image(string="Imagen")

    @api.depends("cita_ids")
    def _compute_citas_realizadas(self):
        Cita = self.env["stylehub.citas"]
        for partner in self:
            partner.citas_realizadas = Cita.search_count([
                ("estilista_id", "=", partner.id),
                ("state", "=", "done"),
            ])
