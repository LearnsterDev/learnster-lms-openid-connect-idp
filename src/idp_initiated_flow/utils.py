def get_bytes_length(n):
    """ref: https://docs.python.org/3/library/stdtypes.html#int.to_bytes"""
    return (n.bit_length() + 7) // 8
