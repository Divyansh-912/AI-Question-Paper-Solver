import cv2
import os



def split_image(image_path, boundary):
    upload_dir = os.path.dirname(image_path)

    image =cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(image_path)

    left_image = image[:, :boundary]

    right_image = image[: , boundary:]


    filename = os.path.splitext(os.path.basename(image_path))[0]

    left_path = os.path.join(upload_dir, f"{filename}_left.png")

    right_path = os.path.join(upload_dir, f"{filename}_right.png")
    

    cv2.imwrite(left_path, left_image)
    cv2.imwrite(right_path, right_image)

    return left_path,right_path