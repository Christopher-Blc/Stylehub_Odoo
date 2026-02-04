from odoo import fields, models, api
from odoo.exceptions import ValidationError

class StylehubServicios(models.Model):

    _name = "stylehub.servicios"
    _description = "Servicios para la peluqueria como corte caballero etc , incluyendo el precio y la duracion."
    _rec_name = "nombre"#para que salga el nombre en vez del stylehub.servicios 1

    nombre = fields.Char(string="Nombre", required=True)
    precio_base = fields.Float(string="Precio base", required=True)
    #se usa en el modelo de citas linea para guardar la duracion de cada servicio
    duracion_horas = fields.Float(string="Duracion (horas)", default=0.5, required=True)
    image_1920 = fields.Image(string="Imagen")
    # para ocultar el servicio sin tener que borrarlo
    activo = fields.Boolean(string="Activo", default=True)


    # validaciones basicas para que no haya valores raros
    @api.constrains("precio_base", "duracion_horas")
    def _check_valores(self):
        for servicio in self:
            if servicio.precio_base < 0:
                raise ValidationError("El precio base no puede ser negativo.")
            if servicio.duracion_horas <= 0:
                raise ValidationError("La duracion tiene que ser mayor que 0.")
            