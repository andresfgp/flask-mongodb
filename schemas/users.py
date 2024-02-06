# schemas.users.py
from marshmallow import Schema, fields, validates, ValidationError, validate
class AvatarUrlSchema(Schema):
    path = fields.Str(required=False)
    preview = fields.Str(required=False)

class UserSchema(Schema):
    email = fields.Email(required=True, unique=True)
    role = fields.Str(required=False)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    phoneNumber = fields.Str(validate=lambda s: s.isdigit() and len(s) == 10, required=False)
    address = fields.Str(required=False)
    password = fields.Str(required=True, validate=lambda p: len(p) >= 8)
    city = fields.Str(required=False)
    state = fields.Str(required=False)
    country = fields.Str(required=False)
    zipCode = fields.Str(required=False)
    company = fields.Str(required=False)
    avatarUrl =  fields.Nested(AvatarUrlSchema, required=False)
    status = fields.Str(required=False)
    isVerified = fields.Boolean(required=False)

    @validates('role')
    def validate_role(self, value):
        valid_roles = ['admin', 'user']  # Add more roles if needed
        if value not in valid_roles:
            raise ValidationError(f"Invalid role. Allowed roles are: {', '.join(valid_roles)}")

class UserUpdateSchema(UserSchema):
    class Meta:
        strict = True

class UserPatchSchema(UserSchema):
    class Meta:
        partial = True

    # Remove email and password from required fields for updates
    email = fields.Email(required=False, allow_none=True, validate=validate.Length(min=1))
    role = fields.Str(required=False, allow_none=True, validate=validate.Length(min=1))
    firstName = fields.Str(required=False, allow_none=True, validate=validate.Length(min=1))
    lastName = fields.Str(required=False, allow_none=True, validate=validate.Length(min=1))
    phoneNumber = fields.Str(required=False, allow_none=True, validate=[lambda s: s.isdigit() and len(s) == 10, validate.Length(min=1)])
    address = fields.Str(required=False, allow_none=True, validate=validate.Length(min=1))
    password = fields.Str(required=False, allow_none=True, validate=validate.Length(min=8))
    city = fields.Str(required=False, allow_none=True)
    state = fields.Str(required=False, allow_none=True)
    country = fields.Str(required=False, allow_none=True)
    zipCode = fields.Str(required=False, allow_none=True)
    company = fields.Str(required=False, allow_none=True)
    avatarUrl = fields.Nested(AvatarUrlSchema, required=False)
    status = fields.Str(required=False, allow_none=True)
    isVerified = fields.Boolean(required=False, allow_none=True)
