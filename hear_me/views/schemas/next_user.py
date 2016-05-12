from colander import MappingSchema, SchemaNode, String, Boolean
from hear_me.utils.schema import NullableString


class MusicSchema(MappingSchema):
    id = SchemaNode(String())
    image_url = SchemaNode(NullableString())


class SquareSchema(MappingSchema):
    energy = MusicSchema()
    sadness = MusicSchema()
    relax = MusicSchema()
    top = MusicSchema()


class NextUserSchema(MappingSchema):
    _id = SchemaNode(String())
    image_url = SchemaNode(NullableString())
    visible_name = SchemaNode(NullableString())

    square = SquareSchema()


class NextUserResultSchema(MappingSchema):
    _id = SchemaNode(String())
    like = SchemaNode(Boolean())
