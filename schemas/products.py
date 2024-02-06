from marshmallow import Schema, fields, validates, ValidationError, validate

class ImageSchema(Schema):
    path = fields.Str(required=True)
    preview = fields.Str(required=True)

class LabelSchema(Schema):
    enabled = fields.Bool(required=True)
    content = fields.Str(required=True)

class ProductSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    subDescription = fields.Str(required=False)
    images = fields.List(fields.Nested(ImageSchema), required=True)
    code = fields.Str(required=False)
    sku = fields.Str(required=False)
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)
    priceSale = fields.Float(required=True)
    tags = fields.List(fields.Str(), required=True)
    taxes = fields.Float(required=True)
    gender = fields.List(fields.Str(), required=True)
    category = fields.Str(required=True)
    colors = fields.List(fields.Str(), required=False)
    sizes = fields.List(fields.Str(), required=False)
    newLabel = fields.Nested(LabelSchema, required=True)
    saleLabel = fields.Nested(LabelSchema, required=True)

class ProductUpdateSchema(ProductSchema):
    class Meta:
        strict = True

class ProductPatchSchema(ProductSchema):
    class Meta:
        partial = True