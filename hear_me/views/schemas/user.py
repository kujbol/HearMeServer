import colander


class UserRegisterSchema(colander.MappingSchema):
    token = colander.SchemaNode(colander.String())
