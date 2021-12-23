from io import StringIO
from pathlib import Path
import streamlit as st
import time
from detect import detect
import os
import sys
import argparse
from PIL import Image
from image_process import imageGray
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# def result_read(txt_path,image):
#     with open(txt_path + '.txt', 'a') as f:
#         lines = f.readlines()
#         # line: cls_label *xywh conf
#         for line_str in lines:
#             line_list = line_str.split()
#
#             # 单个算式
#             img_single_formula = image[line_list[1]:line_list[3], line_list[2]:line_list[4]]
#
#             opt.source = f'data/images/{uploaded_file.name}'
#
#             # 算式预测
#             position = line_list

def get_subdirs(b='.'):
    '''
        Returns all sub-directories in a specific Path
    '''
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    return max(get_subdirs(os.path.join('runs', 'detect')), key=os.path.getmtime)


if __name__ == '__main__':
    st.title('Problem Judgment App')
    st.caption('')
    st.caption('A elementary school math formula recognition & judgement, based on YOLOv5 and CRNN.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str,
                        default='weights/yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str,
                        default='data/images', help='source')
    parser.add_argument('--img-size', type=int, default=640,
                        help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float,
                        default=0.70, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float,
                        default=0.15, help='IOU threshold for NMS')
    parser.add_argument('--device', default='',
                        help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true',
                        help='display results')
    parser.add_argument('--save-txt', action='store_true',
                        help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true',
                        help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true',
                        help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int,
                        help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true',
                        help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true',
                        help='augmented inference')
    parser.add_argument('--update', action='store_true',
                        help='update all models')
    parser.add_argument('--project', default='runs/detect',
                        help='save results to project/name')
    parser.add_argument('--name', default='exp',
                        help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true',
                        help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    print(opt)

    # 保存结果
    #opt.save_txt = True
    opt.save_conf = True
    # source = ("图片检测", "视频检测")
    # source_index = st.sidebar.selectbox("选择输入", range(
    #     len(source)), format_func=lambda x: source[x])

    uploaded_file = st.sidebar.file_uploader(
        "上传图片", type=['png', 'jpeg', 'jpg'])
    if uploaded_file is not None:
        is_valid = True
        with st.spinner(text='资源加载中...'):
            st.sidebar.image(uploaded_file)
            picture = Image.open(uploaded_file)
            picture = picture.save(f'data/images/{uploaded_file.name}')
            # graycontrast
            # im_gray = imageGray(f'data/images/{uploaded_file.name}')
            # im_gray.save(f'data/images/{uploaded_file.name}')

            opt.source = f'data/images/{uploaded_file.name}'
    else:
        is_valid = False


    
    col1, col2 = st.columns(2)
    with col1:
        
        if is_valid:
            print('valid')
            if st.button('开始检测'):

                count, wrong = detect(opt)

                with st.spinner(text='Preparing Images'):
                    detect_folder = str(Path(f'{get_detection_folder()}'))
                    
                    st.image(os.path.join(detect_folder, uploaded_file.name))

                    correct_rate = (1 - (wrong / count)) * 100
                    correct_rate = str(round(correct_rate, 2)) + "%"

                    # 正确率
                    with col2:
                        y = np.array([count - wrong, wrong])
                        fig, ax = plt.subplots()

                        ax.pie(y,
                                labels=['Correct','Wrong'], # 设置饼图标签
                                colors=["#65a479", "#d5695d"], # 设置饼图颜色
                                explode=(0, 0.2), # 第二部分突出显示，值越大，距离中心越远
                                autopct='%d%%', # 格式化输出百分比
                            )
                        st.pyplot(fig)
                        st.subheader("")
                        st.subheader("本页已识别答题数：" + str(count))
                        st.subheader("正确率：" + correct_rate)
                        st.subheader("错答数量：" + str(wrong))
                        st.caption("由于模型质量原因，以上结果仅供参考")

                    st.balloons()
