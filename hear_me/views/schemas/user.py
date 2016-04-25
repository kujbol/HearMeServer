import colander


class UserSchema(colander.MappingSchema):
    _id = colander.SchemaNode(colander.String())
    image_url = colander.SchemaNode(colander.String(), default=None)
    is_active = colander.SchemaNode(colander.String())
