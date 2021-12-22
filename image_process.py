import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
    
# img = cv2.imread(r'C:\\Users\\27466\\Desktop\\RECENT\\yolov5-streamlit-by-xdt-master\\yolov5-streamlit-by-xdt-master\\data\\images\\3.jpg', cv2.IMREAD_GRAYSCALE)#GRAYSCALE

def imageGray(uploaded_file):
    img = cv2.imread(uploaded_file, cv2.IMREAD_GRAYSCALE)
    #线性变换
    a = 1.6
    O = float(a) * img
    O[O>255] = 255 #大于255要截断为255
        
    #数据类型的转换
    O = np.round(O)
    O = O.astype(np.uint8)
    im = Image.fromarray(O)
    return im
    
# #显示原图与变换后的图的效果
# cv2.imshow("img", img)
# cv2.imshow("O", O)
# cv2.waitKey(0)
# cv2.destroyAllWindows()