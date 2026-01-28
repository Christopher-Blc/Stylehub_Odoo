from odoo import models, fields, api

#este modelo hace falta para guardar los servicios individuales de cada cita ya que si se utiliza servicios 
#con un many2many no se pueden guardar datos adicionales como el precio o la duracion de cada servicio en la cita
class CitasLinea(models.Model):
    _name = "stylehub.citas_linea"
    _description = "Linea de servicios de una cita"
    _order = "sequence, id"

    #para cambiar el orden de los servicios en la lista
    sequence = fields.Integer(string="Orden", default=10)

    cita_id = fields.Many2one(
        comodel_name="stylehub.citas",
        string="Cita",
        required=True,
        ondelete="cascade",
    )

    servicio_id = fields.Many2one(
        comodel_name="stylehub.servicios",
        string="Servicio",
        required=True,
        domain=[("activo", "=", True)],
    )


    # guardamos los datos de la lista individual de servicios
    duracion_horas = fields.Float(string="Duracion (horas)", default=0.0)
    precio_unitario = fields.Float(string="Precio", default=0.0)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)


    @api.depends("precio_unitario")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.precio_unitario or 0.0

    #cuando se cambia el servicio , se actualiza el precio y la duracion automaticamente
    @api.onchange("servicio_id")
    def _onchange_servicio_id(self):
        for line in self:
            if line.servicio_id:
                line.precio_unitario = line.servicio_id.precio_base
                line.duracion_horas = line.servicio_id.duracion_horas
