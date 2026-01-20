from Odoo import models, fields

class StylehubCitas(models.Model):
    
    _name = "stylehub.citas"
    _description = "Citas de clientes para servicios de peluquería."

    
    cliente_id = fields.One2many(
        string='field_name',
        comodel_name='model.name',
        inverse_name='inverse_field',
    )
    estilista_id = fields.Many2one(
        string='Estilista',
        comodel_name='stylehub.estilistas',
        required=True,
    )
