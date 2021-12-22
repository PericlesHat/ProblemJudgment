#!/usr/bin/env python
# coding: utf-8
# In[1]:

import os
from PIL import Image
import numpy as np
import paddle

from .utils.model import Model
from .utils.data import process
from .utils.decoder import ctc_greedy_decoder

with open('crnn/work/dataset/vocabulary.txt', 'r', encoding='utf-8') as f:
    vocabulary = f.readlines()

vocabulary = [v.replace('\n', '') for v in vocabulary]

save_model = 'crnn/models/'
model = Model(vocabulary, image_height=32)
model.set_state_dict(paddle.load(os.path.join(save_model, 'model.pdparams')))
model.eval()


# 输入图片路径
def infer(image):
    data = process(image, img_height=32)
    data = data[np.newaxis, :]
    data = paddle.to_tensor(data, dtype='float32')
    # 执行识别
    out = model(data)
    out = paddle.transpose(out, perm=[1, 0, 2])
    out = paddle.nn.functional.softmax(out)[0]
    # 解码获取识别结果
    out_string = ctc_greedy_decoder(out, vocabulary)

    return out_string
    #print('预测结果：%s' % out_string)


# if __name__ == '__main__':
#     image_path = 'work/dataset/images/5_116_6.1-4.9=1.2.jpg'
#     #display(Image.open(image_path))
#     infer(image_path)
