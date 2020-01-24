_rom_val = [
    1000, 900, 500, 400,
    100, 90, 50, 40,
    10, 9, 5, 4,
    1
]
_rom_syb = [
    "M", "CM", "D", "CD",
    "C", "XC", "L", "XL",
    "X", "IX", "V", "IV",
    "I"
]
def int_to_roman(num):
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // _rom_val[i]):
            roman_num += _rom_syb[i]
            num -= _rom_val[i]
        i += 1
    return roman_num

questions = {
    'wild': "What would you like to change the color to? ",
    'call wild': "The last player played a Draw Four Wild. Would you like to call? "
}
