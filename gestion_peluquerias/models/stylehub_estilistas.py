from Odoo import models, fields

class stylehubEstilistas(models.Model):

    _name = "stylehub.estilistas"
    _description = "Estilistas que trabajan en la peluqueria."

    nombre = fields.Char(string="Nombre", required=True)
    activo = fields.Boolean(string="Activo", default=True)
    cita_ids = fields.One2many(
        comodel_name="gestion_peluquerias.cita",
        inverse_name="estilista_id",
        string="Citas"
    )


