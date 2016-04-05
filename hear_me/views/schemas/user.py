import colander


class UserPersonalDataSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    surname = colander.SchemaNode(colander.String())
    email = colander.SchemaNode(
        colander.String(), validator=colander.Email()
    )
    username = colander.SchemaNode(colander.String())


class UserRegisterSchema(UserPersonalDataSchema):
    password = colander.SchemaNode(
        colander.String(), validator=colander.Length(8)
    )


class UserSchema(UserPersonalDataSchema):
    pass
