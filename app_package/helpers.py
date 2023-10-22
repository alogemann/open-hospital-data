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
    str_field = str(field)
    if '.' in str_field:
        first, last = str_field.split('.')
        first = format_first(first)
        last = format_last(last)
        return first + last
    else:
        field = format_first(str_field)
        return field + '00'
    
"""
def wksht_str(wksht_cd):
    wksht_str = wksht_cd[0]
    if wksht_cd[1] == '0' and wksht_cd[-1] != '0':
        wksht_str = f'{wksht_cd[0]} Part {wksht_cd[-1]}'
    if wksht_cd[1] != '0':
        if wksht_cd[-1] == '0':
            wksht_str = f'{wksht_cd[0]}-{wksht_cd[1]}'
        else:
            wksht_str = f'{wksht_cd[0]}-{wksht_cd[1]} Part {wksht_cd[-1]}'
    return wksht_str
"""
