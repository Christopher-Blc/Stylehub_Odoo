from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StylehubCitas(models.Model):

    _name = "stylehub.citas"
    _description = "Citas de clientes para servicios de peluquería."

    cita = fields.Char(string="Cita", required=True)
    state = fields.Selection(

        [
            ("draft", "Borrador"),
            ("confirmed", "Confirmada"),
            ("done", "Realizada"),
            ("cancelled", "Cancelada"),
        ],
        string="Estado",
        default="draft",
        required=True,
    )

    #relacion con el cliente de la bbdd de odoo , el modelo es res_partner
    cliente_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        required=True
    )

    estilista_id = fields.Many2one(
        string='Estilista',
        comodel_name='stylehub.estilistas',
        required=True,
        domain=[('activo','=',True)]#domain es para que nos liste solo los estilistas activos
    )

    # ojo: estaba en mayuscula y luego lo usabas en depends con minuscula
    inicio_fecha_hora = fields.Datetime(string="Fecha y hora de inicio", required=True)

    fin_fecha_hora = fields.Datetime(string="Fecha y hora de fin", compute="_compute_hora_fin", store=True)

    # Este campo relaciona la cita con las líneas de servicios asociados y nos da los datos de cada servicio en la cita
    linea_servicio_ids = fields.One2many(
        comodel_name="stylehub.citas_linea",
        inverse_name="cita_id",
        string="Servicios",
    )

    duracion_total = fields.Float(
        string='Duración total (horas)',
        compute="_compute_duracion_total",
        store=True
    )

    precio_total = fields.Float(
        string='Precio total',
        compute="_compute_precio_total",
        store=True
    )

    #Calcaula el precio total , cogiendo el subtotal de cada linea de servicio y sumandolo
    @api.depends("linea_servicio_ids.duracion_horas")
    def _compute_duracion_total(self):
        for cita in self:
            cita.duracion_total = sum(cita.linea_servicio_ids.mapped("duracion_horas")) or 0.0

    #igual que el metodo anterior pero para la duracion de lka cita
    @api.depends("linea_servicio_ids.subtotal")
    def _compute_precio_total(self):
        for cita in self:
            cita.precio_total = sum(cita.linea_servicio_ids.mapped("subtotal")) or 0.0#el or es para que no haya errores si no hay servicios

    #calcular la hora de fin sumando la duracion total a la hora de inicio
    @api.depends("inicio_fecha_hora", "duracion_total")
    def _compute_hora_fin(self):
        for cita in self:
            if cita.inicio_fecha_hora:
                cita.fin_fecha_hora = cita.inicio_fecha_hora + timedelta(hours=cita.duracion_total or 0.0)
            else:
                cita.fin_fecha_hora = False

    #acciones para cambiar el estado de la cita
    def action_confirm(self):
        for cita in self:
            if not cita.linea_servicio_ids:
                raise ValidationError("No puedes confirmar una cita sin servicios.")
            cita.state = "confirmed"

    #accion para marcar la cita como realizada que se gastara en un boton 
    def action_done(self):
        for cita in self:
            if cita.state == "cancelled":
                raise ValidationError("No puedes marcar como realizada una cita cancelada.")
            cita.state = "done"

    #accion para cancelar la cita
    def action_cancel(self):
        self.write({"state": "cancelled"})

    #accion para volver a poner la cita en borrador
    def action_set_draft(self):
        self.write({"state": "draft"})

    #validacion para que no se solapen las citas de un mismo estilista
    @api.constrains("estilista_id", "inicio_fecha_hora", "fin_fecha_hora", "state")
    def _check_solape_estilista(self):
        for cita in self:
            #si no hay estilista o fechas no hacemos la comprobacion
            if not cita.estilista_id or not cita.inicio_fecha_hora or not cita.fin_fecha_hora:
                continue
            if cita.state == "cancelled":
                continue
            # buscamos citas del mismo estilista que se solapen en el tiempo
            domain = [
                ("id", "!=", cita.id),
                ("estilista_id", "=", cita.estilista_id.id),
                ("state", "!=", "cancelled"),
                ("inicio_fecha_hora", "<", cita.fin_fecha_hora),
                ("fin_fecha_hora", ">", cita.inicio_fecha_hora),
            ]
            #si encontramos alguna cita que cumple esas condiciones, lanzamos un error
            if self.search_count(domain):
                raise ValidationError("El estilista ya tiene una cita solapada en ese horario.")