import cv2

def preprocess_for_ocr(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(image_path)
    
    gray =  cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    upscaled = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,interpolation=cv2.INTER_CUBIC
        )
    blurred = cv2.GaussianBlur(upscaled, (3,3), 0)

    thresh = cv2.adaptiveThreshold(
    blurred,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    31,
    15
    )

    
    processed_path = "processed.png"

    cv2.imwrite(processed_path, thresh)

    return processed_path


def preprocess_for_layout(image_path):

    image = cv2.imread(image_path)

    if image is None: 
        raise FileNotFoundError(image_path)

    gray  =  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(
        gray,
        180,
        255,
        cv2.THRESH_BINARY_INV
    )

    return binary