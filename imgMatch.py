import base64
import numpy as np
import cv2

def read_img(img):
    """
    读取base64编码的图片, 返回opencv格式的图片
    """
    img = base64.b64decode(img)
    img = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


def sobel_edge(image):
    """
    高斯滤波后, Sobel算子边缘检测
    """
    image = cv2.GaussianBlur(image, (1, 1), 0)
    image_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    abs_x = cv2.convertScaleAbs(image_x)
    image_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    abs_y = cv2.convertScaleAbs(image_y)
    dst = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    # 保存图片
    # cv2.imwrite("test_edge.png", dst)
    return np.asarray(dst, dtype=np.uint8)


def get_edge(img):
    """
    获取图片边缘的坐标
    """
    rr = np.where(img[:, :] != 0)
    x_min = min(rr[1])
    y_min = min(rr[0])
    x_max = max(rr[1])
    y_max = max(rr[0])

    return {
        'x': [x_min, x_max],
        'y': [y_min, y_max]
    }


def match(bg_base64, slide_base64, canvas_width):
    """
    在bg中匹配slide 返回匹配的左侧x坐标,还要处理图片实际大小和canvas大小不一致的问题
    """
    bg_img = read_img(bg_base64)
    sd_img = read_img(slide_base64)
    width = bg_img.shape[1]
    bg = sobel_edge(bg_img)
    sd = sobel_edge(sd_img)
    edge = get_edge(sd)
    bg_image = bg[edge['y'][0]:edge['y'][1], :]
    sd_image = sd[edge['y'][0]:edge['y'][1], edge['x'][0]:edge['x'][1]]
    res = cv2.matchTemplate(bg_image, sd_image, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return min_loc[0] * canvas_width / width



    