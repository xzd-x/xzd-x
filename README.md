# 基于小波变换的盲水印算法设计

# 安装
```bash
pip install blind-watermark
```

或者安装最新开发版本
```bach
git clone git@github.com:guofei9987/blind_watermark.git
cd blind_watermark
pip install .
```

# 如何使用


## Python 中使用


参考 [代码](/example_str.py)


嵌入水印
```python
import cv2
from dwt_watermark import embed_watermark

host = cv2.imread('host.jpg')       # 宿主图像
watermark = cv2.imread('wm.png')    # 水印图像（黑白）

watermarked = embed_watermark(host, watermark, alpha=0.1)
cv2.imwrite('watermarked.jpg', watermarked)
```

提取水印
```python
from dwt_watermark import extract_watermark

extracted = extract_watermark('watermarked.jpg', (768, 1024))  # 替换为实际尺寸
cv2.imwrite('extracted_wm.png', extracted)
```



### 运行实例

```python
python example_str.py
```





