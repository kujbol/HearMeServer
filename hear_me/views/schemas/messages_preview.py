from colander import MappingSchema, String, SchemaNode, Integer, SequenceSchema

from hear_me.utils.schema import NullableString


class MessagePreview(MappingSchema):
    _id = SchemaNode(String())
    image_url = SchemaNode(NullableString())
    display_name = SchemaNode(String())
    last_message = SchemaNode(NullableString())


class MessagesPreviewList(SequenceSchema):
    conversation_preview = MessagePreview()


class MessagesPreview(MappingSchema):
    conversations_preview = MessagesPreviewList()
