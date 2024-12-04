def url_maker_from_string(value: str):
    from re import findall

    pattern = r'[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی۰۱۲۳۴۵۶۷۸۹0123456789a-zA-Z]+'
    return '-'.join(findall(pattern, value))
