from marshmallow import Schema, fields, validates, ValidationError, validate

class UserSchema(Schema):
    email = fields.Email(required=True, unique=True)
    role = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(validate=lambda s: s.isdigit() and len(s) == 10, required=True)
    address = fields.Str(required=True)
    password = fields.Str(required=True, validate=lambda p: len(p) >= 8)

    @validates('role')
    def validate_role(self, value):
        valid_roles = ['admin', 'user']  # Add more roles if needed
        if value not in valid_roles:
            raise ValidationError(f"Invalid role. Allowed roles are: {', '.join(valid_roles)}")

class UserUpdateSchema(UserSchema):
    class Meta:
        # Set the `partial` parameter to True for PUT requests
        strict = True

class UserPatchSchema(UserSchema):
    class Meta:
        # Set the `partial` parameter to True for PATCH requests
        partial = True
    # Remove email and password from required fields for updates
    email = fields.Email(required=False, allow_none=True, validate=validate.Length(min=1))
    role = fields.Str(required=False, allow_none=True, validate=validate.Length(min=1))
    first_name = fields.Str(required=False, allow_none=True, validate=validate.Length(min=1))
    last_name = fields.Str(required=False, allow_none=True, validate=validate.Length(min=1))
    phone_number = fields.Str(required=False, allow_none=True, validate=[lambda s: s.isdigit() and len(s) == 10, validate.Length(min=1)])
    address = fields.Str(required=False, allow_none=True, validate=validate.Length(min=1))
    password = fields.Str(required=False, allow_none=True, validate=validate.Length(min=8))
