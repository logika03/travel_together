from djchoices import ChoiceItem, DjangoChoices


class Transport(DjangoChoices):
    LEGS = ChoiceItem('legs', 'ноги')
    CAR = ChoiceItem('car', 'автомобиль')
    BUS = ChoiceItem('bus', 'автобус')
    TRAIN = ChoiceItem('train', 'поезд')
    PLANE = ChoiceItem('plane', 'самолет')
    HITCHHIKING = ChoiceItem('hitchhiking', 'автостоп')
