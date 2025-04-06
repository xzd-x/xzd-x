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



### 各种攻击后的效果

|攻击方式|攻击后的图片|提取的水印|




### 嵌入图片

参考 [代码](/example_str.py)


嵌入：
```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)
# read original image
bwm1.read_img('pic/ori_img.jpg')
# read watermark
bwm1.read_wm('pic/watermark.png')
# embed
bwm1.embed('output/embedded.png')
```

提取：
```python
bwm1 = WaterMark(password_wm=1, password_img=1)
# notice that wm_shape is necessary
bwm1.extract(filename='output/embedded.png', wm_shape=(128, 128), out_wm_name='output/extracted.png', )
```

|攻击方式|攻击后的图片|提取的水印|
|--|--|--|
|旋转攻击45度|![旋转攻击](docs/旋转攻击.jpg)|![](docs/旋转攻击_提取水印.png)|
|随机截图|![截屏攻击](docs/截屏攻击2_还原.jpg)|![](docs/旋转攻击_提取水印.png)|
|多遮挡| ![多遮挡攻击](docs/多遮挡攻击.jpg) |![多遮挡_提取水印](docs/多遮挡攻击_提取水印.png)|



### 隐水印还可以是二进制数据

参考 [代码](/example_bit.py)


作为 demo， 如果要嵌入是如下长度为6的二进制数据
```python
wm = [True, False, True, True, True, False]
```

嵌入水印

```python
# 除了嵌入图片，也可以嵌入比特类数据
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_ori_img('pic/ori_img.jpg')
bwm1.read_wm([True, False, True, True, True, False], mode='bit')
bwm1.embed('output/打上水印的图.png')
```

解水印：（注意设定水印形状 `wm_shape`）
```python
bwm1 = WaterMark(password_img=1, password_wm=1, wm_shape=6)
wm_extract = bwm1.extract('output/打上水印的图.png', mode='bit')
print(wm_extract)
```

解出的水印是一个0～1之间的实数，方便用户自行卡阈值。如果水印信息量远小于图片可容纳量，偏差极小。


