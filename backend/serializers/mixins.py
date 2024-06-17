class ItemHandedOutSerializationMixin:
    """
    Mixin for serializers that have a 'handed_out' field that is populated with
    the pretty user name if the item is handed out and False otherwise.
    """
    def get_handed_out(self, obj):
        try:
            return obj.itembinding.user.get_pretty_name()
        except Exception:
            return False
