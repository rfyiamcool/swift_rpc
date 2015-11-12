#coding:utf-8

REDIS_HOST = '127.0.0.1'
REDIS_PORT  = 6379

RPC_HOST = '127.0.0.1'
RPC_PORT = 8080

SAFE_UA_MODE = True
UA_ALLOW = ['swift_rpc']

SAFE_TOKEN_MODE = False
TOKEN_ALLOW = ['']

REMOTE_IP_MODE = False
REMOTE_ALLOW = ['']

ENCRYPTION_AES= "123xiaorui456789"

LOGCONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s"
        },
        "detail": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] [PID:%(process)d TID:%(thread)d] %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "detail",
            "stream": "ext://sys.stdout"
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'filename': 'debug.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        },

    },

    "loggers": {
        "transmit": {
            "level":"DEBUG",
            "propagate": False,
            "handlers": ["console","file"]
        },
    },

    "root": {
        "level": "INFO",
        "handlers": ["console","file"]
    }
}
