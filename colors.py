
def hex_to_ARGB(hex_color: str, alpha: str = 'FF') -> str:
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]

    if len(hex_color) != 6:
        raise ValueError("HEX must be 6 digits like #RRGGBB")

    flutter_color = f"0x{alpha.upper()}{hex_color.upper()}"
    return f"Color({flutter_color})"
