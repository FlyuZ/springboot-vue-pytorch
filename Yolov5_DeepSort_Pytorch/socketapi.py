
from track import * 
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import threading
import socket
import os
import json
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
inferencemodel = None


class premodel():
    def __init__(self):
        cfg = get_config()
        cfg.merge_from_file("deep_sort_pytorch/configs/deep_sort.yaml")
        attempt_download("deep_sort_pytorch/deep_sort/deep/checkpoint/ckpt.t7", repo='mikel-brostrom/Yolov5_DeepSort_Pytorch')
        self.deepsort = DeepSort(cfg.DEEPSORT.REID_CKPT,
                            max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE,
                            nms_max_overlap=cfg.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                            max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                            use_cuda=True)
    
        # Initialize
        self.device = select_device('0')
    
        # Load model
        self.model = attempt_load('yolov5/weights/yolov5m.pt', map_location=self.device)  # load FP32 model
        stride = int(self.model.stride.max())  # model stride
        self.imgsz = check_img_size(640, s=stride)  # check img_size
        self.names =self. model.module.names if hasattr(self.model, 'module') else self.model.names  # get class names
        self.model.half()  # to FP16

    def predict(self, img0):
        # Padded resize
        img = letterbox(img0, self.imgsz)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB and HWC to CHW
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.half()   # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        # t1 = time_synchronized()
        pred = self.model(img, augment=False)[0]  #可选

        # Apply NMS
        pred = non_max_suppression(
            pred, classes=[18,])  # 可选
        # t2 = time_synchronized()
                # Process detections
        res = img0
        cnt = 0
        for i, det in enumerate(pred):  # detections per image
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(
                    img.shape[2:], det[:, :4], img0.shape).round()

                xywh_bboxs = []
                confs = []
                cnt +=1

                # Adapt detections to deep sort input format
                for *xyxy, conf, cls in det:
                    # to deep sort format
                    x_c, y_c, bbox_w, bbox_h = xyxy_to_xywh(*xyxy)
                    xywh_obj = [x_c, y_c, bbox_w, bbox_h]
                    xywh_bboxs.append(xywh_obj)
                    confs.append([conf.item()])

                xywhs = torch.Tensor(xywh_bboxs)
                confss = torch.Tensor(confs)

                # pass detections to deepsort
                outputs = self.deepsort.update(xywhs, confss, img0)

                # draw boxes for visualization
                if len(outputs) > 0:
                    bbox_xyxy = outputs[:, :4]
                    identities = outputs[:, -1]
                    res = draw_boxes(img0, bbox_xyxy, identities)

            else:
                self.deepsort.increment_ages()
        return res

class ServerThreading(threading.Thread):
    # words = text2vec.load_lexicon()
    def __init__(self, clientsocket, inferencemodel, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        self.inferencemodel = inferencemodel
        pass

    def run(self):
        print("开启线程.....")
        try:
            # 接受Springboot传来的指令数据
            msg = ''
            while True:
                # 读取recvsize个字节
                rec = self._socket.recv(self._recvsize)
                # 解码
                msg += rec.decode(self._encoding)
                # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕，
                # 所以需要自定义协议标志数据接受完毕
                if msg.strip().endswith('over'):
                    break
            msg = msg.strip('over')
            #调用检测算法，并接收算法返回的视频帧（opencv），将每一帧转化为Image
            #如果传回来的帧就是Image则无需转换，所以上面说包含于
            print(msg)
            vs = cv2.VideoCapture(msg) # 本地视频源 
            while True:
                ret,frame = vs.read()
                if ret == False:
                     break
                else:
                    res = inferencemodel.predict(frame)
                    if len(res) < 1:
                        continue
                    # buffered = BytesIO()
                    # img_base64 = Image.fromarray(res)
                    # img_base64.save(buffered, format="JPEG")
                    # imgbase = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    base64_str = cv2.imencode('.jpg',res)[1].tostring()
                    imgbase = base64.b64encode(base64_str).decode('utf-8')
                    msg = {"images": imgbase, "othermsg":""}
                    self._socket.send(("%s" % json.dumps(msg)).encode(self._encoding))
                    self._socket.send(("\n").encode(self._encoding))
            pass
        except Exception as identifier:
            self._socket.send("500".encode(self._encoding))
            print(identifier)
            pass
        finally:
            self._socket.close()
        print("任务结束.....")
        pass

    def __del__(self):
        pass


def socketapi(inferencemodel):
    # 创建服务器套接字
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名称
    host = socket.gethostname()
    # 设置一个端口
    port = 8888
    # 将套接字与本地主机和端口绑定
    serversocket.bind((host, port))
    # 设置监听最大连接数
    serversocket.listen(5)
    # 获取本地服务器的连接信息
    myaddr = serversocket.getsockname()
    print("服务器地址:%s" % str(myaddr))
    # 循环等待接受客户端信息
    while True:
        # 获取一个客户端连接
        clientsocket, addr = serversocket.accept()
        print("连接地址:%s" % str(addr))
        try:
            t = ServerThreading(clientsocket, inferencemodel)  # 为每一个请求开启一个处理线程
            t.setDaemon(True)
            t.start()
            pass
        except Exception  or KeyboardInterrupt:
            exit()
        if not t.is_alive():
            break
        pass
        
    serversocket.close()
    pass


if __name__ == '__main__':
    inferencemodel = premodel()
    socketapi(inferencemodel)