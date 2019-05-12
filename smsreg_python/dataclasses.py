from smsreg_python.utils import prepare_dict


class Services:
    """List of services"""
    AOL = 'aol'
    GMAIL = 'gmail'
    FACEBOOK = 'facebook'
    MAILRU = 'mailru'
    VK = 'vk'
    CLASSMATES = 'classmates'
    TWITTER = 'twitter'
    MAMBA = 'mamba'
    UBER = 'uber'
    TELEGRAM = 'telegram'
    BADOO = 'badoo'
    DRUGVOKRUG = 'drugvokrug'
    AVITO = 'avito'
    OLX = 'olx'
    STEAM = 'steam'
    FOTOSTRANA = 'fotostrana'
    MICROSOFT = 'microsoft'
    VIBER = 'viber'
    WHATSAPP = 'whatsapp'
    WECHAT = 'wechat'
    SEOSPRINT = 'seosprint'
    INSTAGRAM = 'instagram'
    YAHOO = 'yahoo'
    LINEME = 'lineme'
    KAKAOTALK = 'kakaotalk'
    MEETME = 'meetme'
    TINDER = 'tinder'
    NIMSES = 'nimses'
    YOULA = 'youla'
    _5KA = '5ka'
    OTHER = 'other'


class Countries:
    """List of countries"""
    RU = 'ru'
    UA = 'ua'
    GB = 'gb'
    BG = 'bg'
    PL = 'pl'
    HK = 'hk'
    ALL = 'all'


class Misc:
    """ Other constants"""
    HOURS_3 = '3hours'
    DAY = 'day'
    WEEK = 'week'
    APP = '6170706964'
    AID = '414b5959564b533941493234555a4c37'
    BASE_PARAMS = prepare_dict(APP, AID)


class TransactionStates:
    """ States of transaction """
    # error
    WAIT_15_MINUTES = 'WARNING_WAIT15MIN'
    WARNING_NO_NUMS = 'WARNING_NO_NUMS'

    # initial
    TZ_INPOOL = 'TZ_INPOOL'

    # success
    TZ_NUM_PREPARE = 'TZ_NUM_PREPARE'
    TZ_NUM_WAIT = 'TZ_NUM_WAIT'
    TZ_NUM_ANSWER = 'TZ_NUM_ANSWER'

    # expired state
    TZ_OVER_OK = 'TZ_OVER_OK'
    TZ_OVER_EMPTY = 'TZ_OVER_EMPTY'
    TZ_OVER_NR = 'TZ_OVER_NR'
    TZ_DELETED = 'TZ_DELETED'

    # collection
    GET_STATE_ERRORS = (WAIT_15_MINUTES, WARNING_NO_NUMS)
    GET_STATE_EXPIRED = (TZ_OVER_OK, TZ_OVER_EMPTY, TZ_OVER_NR, TZ_DELETED)
    GET_STATE_SUCCESS = (TZ_INPOOL, TZ_NUM_PREPARE, TZ_NUM_WAIT, TZ_NUM_ANSWER)

