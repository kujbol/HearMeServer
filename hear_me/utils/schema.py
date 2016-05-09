import colander


class Boolean(colander.Boolean):
    def serialize(self, node, appstruct):
        result = super(Boolean, self).serialize(node, appstruct)
        if result is not colander.null:
            result = bool(result)
        return result


class Integer(colander.Integer):
    def serialize(self, node, appstruct):
        result = super(Integer, self).serialize(node, appstruct)
        if result is not colander.null:
            result = int(result)
        return result


class NullableString(colander.String):
    def serialize(self, node, appstruct):
        result = super(NullableString, self).serialize(node, appstruct)
        if result is colander.null:
            result = None
        return result
