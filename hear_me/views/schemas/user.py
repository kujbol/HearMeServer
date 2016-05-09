import colander

from hear_me.utils.schema import NullableString, Boolean


class UserSchema(colander.MappingSchema):
    _id = colander.SchemaNode(colander.String())
    image_url = colander.SchemaNode(NullableString())
    is_active = colander.SchemaNode(Boolean())
    email = colander.SchemaNode(colander.String())
