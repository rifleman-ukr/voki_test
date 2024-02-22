from test_utils import wait_until, compare_screen, locate_object_on_screen


def test_game_launch(driver):
    assert wait_until(lambda: compare_screen(driver, 'splash_screen') > 0.9), 'Splashscreen should be displayed'
    assert wait_until(lambda: locate_object_on_screen(driver, 'loading_screen_logo')), \
        'Loading screen should be displayed'
