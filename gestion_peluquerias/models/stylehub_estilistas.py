from odoo import models, fields

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


