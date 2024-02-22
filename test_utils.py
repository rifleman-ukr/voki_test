import logging
import time
from statistics import mean, StatisticsError

import cv2
import numpy

from image_utils import take_screenshot, get_normalized_image_hist

logging.basicConfig(level='INFO')


def wait_until(condition, timeout=5, period=0.25, *args, **kwargs):
    wait_timeout = time.time() + timeout
    while time.time() < wait_timeout:
        if condition(*args, **kwargs):
            return True
        time.sleep(period)
    return False


def compare_screen(driver, sample):
    sample_image = get_normalized_image_hist(cv2.imread(f'samples/{sample}.png',
                                                        flags=cv2.IMREAD_COLOR))
    screen_image = get_normalized_image_hist(cv2.imdecode(numpy.frombuffer(take_screenshot(driver), dtype=numpy.uint8),
                                                          flags=cv2.IMREAD_COLOR))
    hist_score = cv2.compareHist(sample_image, screen_image, cv2.HISTCMP_CORREL)
    logging.info(f'Comparing {sample} with current screen score is {hist_score}')
    return hist_score


def locate_object_on_screen(driver, sample):
    try:
        screen_img = cv2.imdecode(numpy.frombuffer(take_screenshot(driver), dtype=numpy.uint8), flags=cv2.IMREAD_COLOR)
        sample_img = cv2.imread(f'samples/{sample}.png', flags=cv2.IMREAD_COLOR)
        h, w = sample_img.shape[:-1]
        matched_template = numpy.where(cv2.matchTemplate(screen_img, sample_img, cv2.TM_CCOEFF_NORMED) >= .8)[::-1]
        top_left = (mean(matched_template[0]), mean(matched_template[1]))
        top_right = (mean(matched_template[0]) + w, mean(matched_template[1]))
        bottom_left = (mean(matched_template[0]), mean(matched_template[1]) + h)
        bottom_right = (mean(matched_template[0]) + w, mean(matched_template[1]) + h)
        middle = (mean((top_left[0], top_right[0])), mean((bottom_left[1], bottom_right[1])))
        logging.info(f'Object {sample} found at {middle}')
        return {'top_left': top_left,
                'top_right': top_right,
                'bottom_left': bottom_left,
                'bottom_right': bottom_right,
                'middle': middle}
    except StatisticsError:
        return None
