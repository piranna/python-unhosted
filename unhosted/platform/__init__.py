def _convertArgs(args):
    result = {}
    for key, value in args.iteritems():
        if len(value) == 1:
            result[key] = value[0]
        else:
            result[key] = value
    return result