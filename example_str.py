import cv2
import numpy as np
import pywt

def embed_watermark(host_img, watermark_img, alpha=0.1):
    # 转换为灰度图像
    host = cv2.cvtColor(host_img, cv2.COLOR_BGR2GRAY)
    watermark = cv2.cvtColor(watermark_img, cv2.COLOR_BGR2GRAY)
    
    # 调整水印尺寸匹配宿主图像中频子带
    h, w = host.shape
    wm_h, wm_w = watermark.shape
    watermark = cv2.resize(watermark, (w//2, h//2))
    
    # 小波分解
    coeffs = pywt.dwt2(host, 'haar')
    LL, (LH, HL, HH) = coeffs
    
    # 水印嵌入（修改中频子带）
    for i in range(wm_h):
        for j in range(wm_w):
            if watermark[i,j] % 2 == 0:
                HL[i,j] = HL[i,j] - alpha * abs(HL[i,j])
            else:
                HL[i,j] = HL[i,j] + alpha * abs(HL[i,j])
                
    # 小波重构
    coeffs = (LL, (LH, HL, HH))
    watermarked = pywt.idwt2(coeffs, 'haar')
    return np.uint8(np.clip(watermarked, 0, 255))

def extract_watermark(watermarked_img, original_shape):
    # 转换为灰度图像
    wm_img = cv2.cvtColor(watermarked_img, cv2.COLOR_BGR2GRAY)
    
    # 小波分解
    coeffs = pywt.dwt2(wm_img, 'haar')
    _, (_, (_, _)), (_, (_, _)) = coeffs  # 获取HL子带
    
    # 重构水印
    watermark = np.zeros(original_shape, dtype=np.uint8)
    h, w = original_shape
    wm_h, wm_w = h//2, w//2
    
    for i in range(wm_h):
        for j in range(wm_w):
            if coeffs[1][1][i,j] > 0:
                watermark[2*i, 2*j] = 255
            else:
                watermark[2*i, 2*j] = 0
                
    return watermark

# 示例用法
if __name__ == "__main__":
    # 读取图像
    host = cv2.imread('host.jpg')
    watermark = cv2.imread('watermark.png')
    
    # 嵌入水印
    watermarked = embed_watermark(host, watermark)
    cv2.imwrite('watermarked.jpg', watermarked)
    
    # 提取水印
    extracted = extract_watermark(watermarked, host.shape[:2])
    cv2.imwrite('extracted_watermark.png', extracted)
