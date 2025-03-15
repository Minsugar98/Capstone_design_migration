import cv2
import numpy as np
from config import AppConfig
input_file_path = AppConfig.FILE_PATHS['upload']
output_file_path = AppConfig.FILE_PATHS['output']

def detect_and_draw_circles(input_file_path, output_file_path):
    margin = 10
    val = 15   # 밝기 조절할때 사용 깨끗한 이미지는 15


    # 이미지 불러오기
    input_img = cv2.imread(input_file_path, cv2.IMREAD_COLOR)
    #cv2.imshow("0",input_img)
    #input_img = cv2.resize(input_img, dsize=(130, 80), interpolation=cv2.INTER_AREA)
    #cv2.imshow("1",input_img)
    # 밝기 조절
    array = np.full(input_img.shape, (val, val, val), dtype=np.uint8)
    sub = cv2.subtract(input_img, array)

    # 그레이스케일 변환
    gray = cv2.cvtColor(sub, cv2.COLOR_RGB2GRAY)
    #cv2.imshow("2",gray)

    # 이진화 처리
    out = gray.copy()
    #out = 255-out
    #cv2.imshow("3",out)
    t, threshold_img = cv2.threshold(out, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #threshold_img = cv2.adaptiveThreshold(out, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5)
    #threshold_img = cv2.adaptiveThreshold(out, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 5)

    #cv2.imshow("4",threshold_img)
    cv2.imwrite('thre_img.png', threshold_img)



    v, h = threshold_img.shape
    measure_img = np.ones((v + margin * 2, h + margin * 2), dtype=np.uint8) * 255
    measure_img[margin:v + margin, margin:h + margin] = threshold_img.copy()
    #measure_img = cv2.resize(measure_img, (measure_img.shape[1] * 2, measure_img.shape[0] * 2))
    #cv2.imshow("5",measure_img)

    # Blob 검출기 생성
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 5.0 * 5.0
    params.maxArea = 20.0 * 20.0
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(measure_img)
    detected_img = cv2.drawKeypoints(measure_img, keypoints, np.array([]), (0, 0, 255),
                                     cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #cv2.imshow("test",detected_img)


    # 원 그리기
    x=[]
    y=[]
    center = []

    for keyPoint in keypoints:
        x_1 = keyPoint.pt[0]
        y_1 = keyPoint.pt[1]
        x.append(int(x_1))
        y.append(int(y_1))
        center.append((int(x_1), int(y_1)))

    h, w = measure_img.shape
    result_img = np.ones((h,w), dtype=np.uint8) * 255

    j = 0
    while j < len(center):
        result_img = cv2.circle(result_img, center[j], 5, (0, 0, 0), -1)
        j = j +1

    result_img2 = cv2.resize(result_img,(w,h))

    # 이미지 출력
    #cv2.imshow("detected circles",result_img2)
    cv2.imwrite(output_file_path, result_img2)
    
    
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
detect_and_draw_circles(input_file_path, output_file_path)
