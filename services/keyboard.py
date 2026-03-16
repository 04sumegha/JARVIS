import screen_brightness_control as sbc

def increase_brightness(amount=10):
    current = sbc.get_brightness()[0]
    new_level = min(100, current + amount)
    sbc.set_brightness(new_level)
    return new_level


def decrease_brightness(amount=10):
    current = sbc.get_brightness()[0]
    new_level = max(0, current - amount)
    sbc.set_brightness(new_level)
    return new_level