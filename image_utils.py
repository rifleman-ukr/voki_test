import base64

import cv2


def take_screenshot(driver, save=False, file_name='tmp'):
    raw_screenshot = base64.b64decode(driver.get_screenshot_as_base64())
    if save:
        with open(f'{file_name}.png', 'wb') as screenshot:
            screenshot.write(raw_screenshot)
            screenshot.close()
    return raw_screenshot


def get_normalized_image_hist(source):
    hist = cv2.calcHist([source], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    return hist
