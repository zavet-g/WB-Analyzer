from apps.utils.enums.base_enum import BaseENUM


class CRONGroupTypeEnum(BaseENUM):
    PARSER_GROUP = 'PARSER_GROUP'
    ML_GROUP = 'ML_GROUP'


class CRONJobNameEnum(BaseENUM):
    # Parsers
    MAIL_LOG_PARSER_JOB = 'MAIL_LOG_PARSER_JOB'

    # ML
    TRAIN_CHECK_SPAM_JOB = 'TRAIN_CHECK_SPAM_JOB'
