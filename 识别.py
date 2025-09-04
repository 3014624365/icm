import cv2 as cv
import numpy as np
import time

# 常量定义
THRESHOLD_AREA_MIN = 100  # 最小有效区域阈值
THRESHOLD_BINARY = 70  # 二值化阈值
THRESHOLD_STATE = 0.25  # 状态判断阈值比例
THRESHOLD_IMG_STATE = 70  # 像素状态阈值
KERNEL_SIZE = (3, 3)  # 形态学操作核大小
NUM_SAMPLES = 10  # 视频采样帧数


def preprocess_image(img):
    """图像预处理流程：灰度化->中值滤波->二值化->边缘检测->闭运算"""
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred = cv.medianBlur(gray, 5)
    _, binary = cv.threshold(blurred, THRESHOLD_BINARY, 255, cv.THRESH_BINARY)
    edges = cv.Canny(binary, 100, 200)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, KERNEL_SIZE)
    closed = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)
    return closed


def find_chessboard(img):
    """在图像中寻找最大轮廓对应的棋盘区域"""
    processed = preprocess_image(img)
    contours, _ = cv.findContours(processed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    max_area = 0
    best_rect = None
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        area = w * h
        if area > max_area and area >= THRESHOLD_AREA_MIN:
            max_area = area
            best_rect = (x, y, x + w, y + h)

    if best_rect:
        cv.rectangle(img, best_rect[:2], best_rect[2:], (0, 255, 0), 2)
    return img, max_area, best_rect


def analyze_region(image, x1, y1, x2, y2):
    """分析指定区域的状态"""
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

    # 区域有效性检查
    if (x1 >= x2) or (y1 >= y2) or \
            (x1 < 0) or (y1 < 0) or \
            (x2 > image.shape[1]) or (y2 > image.shape[0]):
        return 0, image

    # 区域处理
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    roi = gray[y1:y2, x1:x2]
    mask = roi < THRESHOLD_IMG_STATE
    ratio = np.sum(mask) / (roi.size + 1e-6)  # 防止除以零

    # 可视化标记
    color = (0, 0, 255) if ratio > THRESHOLD_STATE else (255, 0, 0)
    cv.rectangle(image, (x1, y1), (x2, y2), color, 1)
    return int(ratio > THRESHOLD_STATE), image


def get_chess_state(frame, rect):
    """获取棋盘3x3状态矩阵"""
    x_start, y_start, x_end, y_end = rect
    cell_w = (x_end - x_start) / 3
    cell_h = (y_end - y_start) / 3

    state = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            x1 = x_start + j * cell_w
            y1 = y_start + i * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h
            state[i, j], frame = analyze_region(frame, x1, y1, x2, y2)

    cv.imshow("Chess Analysis", frame)
    cv.waitKey(1)
    return state


def stable_rectangle_detection(video):
    """稳定矩形区域检测：多帧采样+异常值过滤"""
    samples = []
    for _ in range(NUM_SAMPLES):
        ret, frame = video.read()
        if not ret: continue

        _, _, rect = find_chessboard(frame.copy())
        if rect:
            samples.append(rect)
            cv.imshow("Processing", frame)
            if cv.waitKey(1) == ord('q'):
                break

    if not samples:
        return None, None

    # 使用中位数代替平均值提高鲁棒性
    return tuple(np.median(samples, axis=0).astype(int)), frame


def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible")
        return

    try:
        while True:
            rect, frame = stable_rectangle_detection(cap)
            if not rect:
                print("Chessboard not detected")
                time.sleep(1)
                continue

            state_matrix = get_chess_state(frame, rect)
            print("Current State:\n", state_matrix)

            if cv.waitKey(1) == ord('q'):
                break
    finally:
        cap.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()