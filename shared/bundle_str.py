# bundle_


def len_euckr(s: str):
    return len(s.encode('euc_kr'))


def byte_euckr(s: str):
    return s.encode('euc_kr')


def cut_by_bytelen(s: str, length: int):
    return s.encode('euc_kr')[:length].decode('euc_kr')


def i2fs(i: int) -> str:
    return format(i, ',')


def fs2i(s: str) -> int:
    try:
        return int(s.replace(',', ''))
    except:
        print('---------- [EXCEPTION] invalid literal for int() with base 10: return None ----------')
        return None
