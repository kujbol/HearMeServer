from colander import (
    DateTime,
    MappingSchema,
    SchemaNode,
    SequenceSchema
)

from hear_me.utils.schema import NullableString


class MessageSchema(MappingSchema):
    text = SchemaNode(NullableString())
    send_date = SchemaNode(DateTime())
    sender = SchemaNode(NullableString())


class MessageSequenceSchema(SequenceSchema):
    messages = MessageSchema()


class MessagesSchema(MappingSchema):
    messages = MessageSequenceSchema()
