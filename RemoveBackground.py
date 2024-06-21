import cv2
import os
from rembg import remove
from PIL import Image
import numpy as np

def remove_background(input_image_path, output_image_path):
    # 背景を削除
    try:
        input_image = Image.open(input_image_path)
    except IOError:
        print(f"Error: Cannot open {input_image_path}")
        return False

    output_image = remove(input_image)
    output_image.save(output_image_path)
    return True

def apply_mask_to_background(masked_image_path):
    # RGBA画像を読み込み
    rgba_image = cv2.imread(masked_image_path, cv2.IMREAD_UNCHANGED)
    if rgba_image is None:
        print(f"Error: Cannot open {masked_image_path}")
        return None

    # アルファチャネルをマスクとして使用
    alpha_channel = rgba_image[:, :, 3]

    # 白い背景画像を作成
    background = np.ones_like(rgba_image, dtype=np.uint8) * 255
    # マスクを適用
    background_masked = cv2.bitwise_and(background, background, mask=alpha_channel)
    return background_masked

def main():
    input_folder = './images'
    output_folder = './processed_images'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            base_filename = os.path.splitext(filename)[0]  # ファイル名の拡張子を除去
            output_path = os.path.join(output_folder, base_filename + '-remove.png')

            # 背景除去処理
            if remove_background(input_path, output_path):
                # マスク適用処理
                masked_image = apply_mask_to_background(output_path)
                #if masked_image is not None:
                #    output_masked_path = os.path.join(output_folder, filename.replace('.jpg', '-masked.jpg').replace('.png', '-masked.jpg'))
                #    cv2.imwrite(output_masked_path, masked_image)

                    # 画像を表示
                    #cv2.imshow('Masked Image', masked_image)
                    #cv2.waitKey(0)
                    #cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
