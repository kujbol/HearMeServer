import colander

from hear_me.utils.schema import NullableString


class UserSchema(colander.MappingSchema):
    _id = colander.SchemaNode(colander.String())
    image_url = colander.SchemaNode(NullableString())
    is_active = colander.SchemaNode(colander.String())
    email = colander.SchemaNode(colander.String())
