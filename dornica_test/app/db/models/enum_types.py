import enum


class GenderEnum(enum.Enum):
    MAIL = 'MAIL'
    FEMAIL = 'FEMAIL'
    NOT_SPECIFIED = 'NOT_SPECIFIED'


class ListingTypeEnum(enum.Enum):
    HOUSE = 'HOUSE'
    APARTMENT = 'APARTMENT'
