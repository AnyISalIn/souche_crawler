from dateutil import parser


parse_func = {
    'driver_mile': lambda x: float(x.strip('万公里')),
    'first_register': parser.parse,
}


def parse_field(data):
    ret = {}
    for key, val in data.items():
        if key in parse_func:
            ret[key] = parse_func[key](val)
        else:
            ret[key] = val
    return ret
