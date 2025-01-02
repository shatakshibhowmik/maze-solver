#final with detecting start and end point in all four direction
import cv2
import numpy as np
import pywt


def preprocess_image(image_path, bin_size=(1, 1), scale_percent=10):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image file '{image_path}' not found or cannot be opened.")

    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    _, binary_img = cv2.threshold(resized, 128, 255, cv2.THRESH_BINARY)
    binary_img = binary_img // 255

    reduced_img = process_image_in_bins(binary_img, bin_size)
    return reduced_img

def process_image_in_bins(binary_img, bin_size):
    rows, cols = binary_img.shape
    bin_rows, bin_cols = bin_size
    reduced_rows = rows // bin_rows
    reduced_cols = cols // bin_cols
    reduced_img = np.zeros((reduced_rows, reduced_cols), dtype=int)

    for i in range(0, reduced_rows * bin_rows, bin_rows):
        for j in range(0, reduced_cols * bin_cols, bin_cols):
            bin_block = binary_img[i:i + bin_rows, j:j + bin_cols]
            compressed_bin = apply_wavelet_compression(bin_block)
            reduced_img[i // bin_rows, j // bin_cols] = 1 if np.mean(compressed_bin) > 0.5 else 0

    return reduced_img

def apply_wavelet_compression(bin_block):
    coeffs2 = pywt.dwt2(bin_block, 'haar')
    LL, (LH, HL, HH) = coeffs2
    return LL