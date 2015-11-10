from .models import SignalData


def add_signal_save(instance, **kwargs):
    number = getattr(instance, 'id', 'None')
    name_class = kwargs['sender']
    name_model = name_class.__name__

    if kwargs['created'] and name_model != 'SignalData':
        entry = SignalData(message="Create row with id " + str(number) +
                                   " in " + name_model)
        entry.save()
    elif not kwargs['created'] and name_model != 'SignalData':
        entry = SignalData(message="Update row with id " + str(number) +
                                   " in " + name_model)
        entry.save()


def add_signal_delete(instance, **kwargs):
    number = getattr(instance, 'id', 'None')
    name_class = kwargs['sender']
    name_model = name_class.__name__

    if name_model != 'SignalData':
        entry = SignalData(message="Delete row with id " + str(number) +
                                   " in " + name_model)
        entry.save()
