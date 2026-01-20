from odoo import fields, models, api

class StylehubServicios(models.Model):

    _name = "stylehub.servicios"
    _description = "Servicios para la peluqueria como corte caballero etc , incluyendo el precio y la duracion."

    nombre = fields.Char(string = "Title" , required = True)
    precio_base = fields.Float(string='Precio base', required = True)
    duracion = fields.Float(string='Duracion',default= 0.5 , required = True) 
    image_1920 = fields.Image(string="Imagen") 
    
    

    
    

    
