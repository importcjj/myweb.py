# -*- coding: utf-8 -*-

Codes = \
    {100: '100 Continue',
     101: '101 Switching Protocols',
     102: '102 Processing',
     200: '200 OK',
     201: '201 Created',
     202: '202 Accepted',
     203: '203 Non-Authoritative Information',
     204: '204 No Content',
     205: '205 Reset Content',
     206: '206 Partial Content',
     207: '207 Multi Status',
     226: '226 IM Used',
     300: '300 Multiple Choices',
     301: '301 Moved Permanently',
     302: '302 Found',
     303: '303 See Other',
     304: '304 Not Modified',
     305: '305 Use Proxy',
     306: '306 (Unused)',
     307: '307 Temporary Redirect',
     400: '400 Bad Request',
     401: '401 Unauthorized',
     402: '402 Payment Required',
     403: '403 Forbidden',
     404: '404 Not Found',
     405: '405 Method Not Allowed',
     406: '406 Not Acceptable',
     407: '407 Proxy Authentication Required',
     408: '408 Request Timeout',
     409: '409 Conflict',
     410: '410 Gone',
     411: '411 Length Required',
     412: '412 Precondition Failed',
     413: '413 Request Entity Too Large',
     414: '414 Request-URI Too Long',
     415: '415 Unsupported Media Type',
     416: '416 Requested Range Not Satisfiable',
     417: '417 Expectation Failed',
     422: '422, Unprocessable Entity',
     423: '423 Locked',
     424: '424 Failed Dependency',
     426: '426 Upgrade Required',
     500: '500 Internal Server Error',
     501: '501 Not Implemented',
     502: '502 Bad Gateway',
     503: '503 Service Unavailable',
     504: '504 Gateway Timeout',
     505: '505 HTTP Version Not Supported',
     507: '507 Insufficient Storage',
     510: '510 Not Extended'}


class HttpStatus(object):
    CONTINUE = Codes[100]
    SWITCHING_PROTOCOLS = Codes[101]
    PROCESSING = Codes[102]
    OK = Codes[200]
    CREATED = Codes[201]
    ACCEPTED = Codes[202]
    NON_AUTHORITATIVE_INFORMATION = Codes[203]
    NO_CONTENT = Codes[204]
    RESET_CONTENT = Codes[205]
    PARTIAL_CONTENT = Codes[206]
    MULTI_STATUS = Codes[207]
    IM_USED = Codes[226]
    MULTIPLE_CHOICES = Codes[300]
    MOVED_PERMANENTLY = Codes[301]
    FOUND = Codes[302]
    SEE_OTHER = Codes[303]
    NOT_MODIFIED = Codes[304]
    USE_PROXY = Codes[305]
    TEMPORARY_REDIRECT = Codes[307]
    BAD_REQUEST = Codes[400]
    UNAUTHORIZED = Codes[401]
    PAYMENT_REQUIRED = Codes[402]
    FORBIDDEN = Codes[403]
    NOT_FOUND = Codes[404]
    METHOD_NOT_ALLOWED = Codes[405]
    NOT_ACCEPTABLE = Codes[406]
    PROXY_AUTHENTICATION_REQUIRED = Codes[407]
    REQUEST_TIMEOUT = Codes[408]
    CONFLICT = Codes[409]
    GONE = Codes[410]
    LENGTH_REQUIRED = Codes[411]
    PRECONDITION_FAILED = Codes[412]
    REQUEST_ENTITY_TOO_LARGE = Codes[413]
    REQUEST_URI_TOO_LONG = Codes[414]
    UNSUPPORTED_MEDIA_TYPE = Codes[415]
    REQUESTED_RANGE_NOT_SATISFIABLE = Codes[416]
    EXPECTATION_FAILED = Codes[417]
    UNPROCESSABLE_ENTITY = Codes[422]
    LOCKED = Codes[423]
    FAILED_DEPENDENCY = Codes[424]
    UPGRADE_REQUIRED = Codes[426]
    INTERNAL_SERVER_ERROR = Codes[500]
    NOT_IMPLEMENTED = Codes[501]
    BAD_GATEWAY = Codes[502]
    SERVICE_UNAVAILABLE = Codes[503]
    GATEWAY_TIMEOUT = Codes[504]
    HTTP_VERSION_NOT_SUPPORTED = Codes[505]
    INSUFFICIENT_STORAGE = Codes[507]
    NOT_EXTENDED = Codes[510]

    def __getitem__(self, code):
        if code in Codes:
            return Codes[code]
        raise ValueError('There is no status code {}.'.format(code))

http_status = HttpStatus()
