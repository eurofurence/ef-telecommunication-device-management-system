from rest_framework import serializers


class ObjectWithIdExistsValidator:
    """
    Validator that checks if an object of type model with the given ID exists in the database.
    """

    def __init__(self, model):
        self.model = model

    def __call__(self, value):
        if not self.model.objects.filter(pk=value).exists():
            message = f'No {self.model.__name__} with ID {value} exists.'
            raise serializers.ValidationError(message)
