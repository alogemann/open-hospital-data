def format_first(first):
    if len(first) == 1:
        return '00' + first
    elif len(first) == 2:
        return '0' + first
    else:
        return first

def format_last(last):
    if len(last) == 1:
        return last + '0'
    else:
        return last

def format_field(field):
    if '.' in field:
        first, last = field.split('.')
        first = format_first(first)
        last = format_last(last)
        return first + last
    else:
        field = format_first(field)
        return field + '00'