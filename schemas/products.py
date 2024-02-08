from marshmallow import Schema, fields, validates, ValidationError, validate

class ImageSchema(Schema):
    path = fields.Str(required=True)
    preview = fields.Str(required=True)

class LabelSchema(Schema):
    enabled = fields.Bool(required=True)
    content = fields.Str(required=True)

class ProductSchema(Schema):
    # Details
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    subDescription = fields.Str(required=False)
    images = fields.List(fields.Str(required=True))
    # Properties
    # code = fields.Str(required=False)
    # sku = fields.Str(required=False)
    # quantity = fields.Integer(required=False)
    # tags = fields.List(fields.Str(), required=False)
    # gender = fields.List(fields.Str(), required=False)
    # colors = fields.List(fields.Str(), required=False)
    # sizes = fields.List(fields.Str(), required=False)
    # newLabel = fields.Nested(LabelSchema, required=False)
    # saleLabel = fields.Nested(LabelSchema, required=False)
    # category = fields.Str(required=False)
    # Pricing
    price = fields.Float(required=True)
    priceSale = fields.Float(required=True)
    taxes = fields.Float(required=True)
    # Other
    publish = fields.Boolean(required=False)

class ProductUpdateSchema(ProductSchema):
    class Meta:
        strict = True

class ProductPatchSchema(ProductSchema):
    class Meta:
        partial = True

    # Remove required fields for updates    
    # Details
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    subDescription = fields.Str(required=False)
    images = fields.List(fields.Str(required=False))
    # Properties
    # code = fields.Str(required=False)
    # sku = fields.Str(required=False)
    # quantity = fields.Integer(required=False)
    # tags = fields.List(fields.Str(), required=False)
    # gender = fields.List(fields.Str(), required=False)
    # colors = fields.List(fields.Str(), required=False)
    # sizes = fields.List(fields.Str(), required=False)
    # newLabel = fields.Nested(LabelSchema, required=False)
    # saleLabel = fields.Nested(LabelSchema, required=False)
    # category = fields.Str   (required=False)
    # Pricing
    price = fields.Float(required=False)
    priceSale = fields.Float(required=False)
    taxes = fields.Float(required=False)
    # Other
    publish = fields.Boolean(required=False)