#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import copy
import argparse
from typing import List, Any
import cv2
import mediapipe as mp  # type:ignore
from mediapipe.tasks import python  # type:ignore
from mediapipe.tasks.python import vision  # type:ignore
from mediapipe import solutions as mp_solutions
from utils import CvFpsCalc
from utils.download_file import download_file


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--video", type=str, default=None)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument(
        "--model",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help='''
        0:Color sketch
        1:Color ink
        2:Oil painting
        ''',
    )

    args = parser.parse_args()

    return args


def main() -> None:
    # 引数解析
    args: argparse.Namespace = get_args()

    cap_device: int = args.device
    cap_width: int = args.width
    cap_height: int = args.height

    model: int = args.model

    if args.video is not None:
        cap_device = args.video

    model_url: List[str] = [
        'https://storage.googleapis.com/mediapipe-models/face_stylizer/blaze_face_stylizer/float32/latest/face_stylizer_color_sketch.task',
        'https://storage.googleapis.com/mediapipe-models/face_stylizer/blaze_face_stylizer/float32/latest/face_stylizer_color_ink.task',
        'https://storage.googleapis.com/mediapipe-models/face_stylizer/blaze_face_stylizer/float32/latest/face_stylizer_oil_painting.task',
    ]

    # ダウンロードファイル名生成
    model_name: str = model_url[model].split('/')[-1]
    quantize_type: str = model_url[model].split('/')[-3]
    split_name: List[str] = model_name.split('.')
    model_name = split_name[0] + '_' + quantize_type + '.' + split_name[1]

    # 重みファイルダウンロード
    model_path: str = os.path.join('model', model_name)
    if not os.path.exists(model_path):
        download_file(url=model_url[model], save_path=model_path)

    # カメラ準備
    cap: cv2.VideoCapture = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # Face Stylizer生成
    base_options: python.BaseOptions = python.BaseOptions(
        model_asset_path=model_path)
    options: vision.FaceStylizerOptions = vision.FaceStylizerOptions(
        base_options=base_options, )
    stylizer: vision.FaceStylizer = vision.FaceStylizer.create_from_options(
        options)  # type:ignore

    # FPS計測モジュール
    cvFpsCalc: CvFpsCalc = CvFpsCalc(buffer_len=10)

    # 顔検出
    face_detection = mp_solutions.face_detection.FaceDetection(model_selection=0)

    while True:
        display_fps: float = cvFpsCalc.get()

        # カメラキャプチャ
        ret: bool
        frame: Any
        ret, frame = cap.read()
        if not ret:
            break

        # 顔検出
        results_original = face_detection.process(frame)
        
        # 推論実施
#        rgb_frame: mp.Image = mp.Image(
#            image_format=mp.ImageFormat.SRGBA,
#            data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA),
#        )
#        stylized_image = stylizer.stylize(rgb_frame)

        # 元画像の顔検出
        if results_original.detections:
            for detection in results_original.detections:
                bbox_original = detection.location_data.relative_bounding_box
                ih, iw = frame.shape[:2]
                x_original = int(bbox_original.xmin * iw)
                y_original = int(bbox_original.ymin * ih)
                w_original = int(bbox_original.width * iw)
                h_original = int(bbox_original.height * ih)

                # スタイライズ処理
                stylized_image = stylizer.stylize(mp.Image(image_format=mp.ImageFormat.SRGBA, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)))

                # スタイライズされた顔から顔検出する
                results_stylized = face_detection.process(stylized_image.numpy_view())
                if results_stylized.detections:
                    for detection_stylized in results_stylized.detections:
                        ih, iw = stylized_image.numpy_view().shape[:2]
                        bbox_stylized = detection_stylized.location_data.relative_bounding_box
                        x_stylized = int(bbox_stylized.xmin * iw)
                        y_stylized = int(bbox_stylized.ymin * ih)
                        w_stylized = int(bbox_stylized.width * iw)
                        h_stylized = int(bbox_stylized.height * ih)
                        
                        # 比率を計算
                        ratio_w = w_original / w_stylized
                        ratio_h = h_original / h_stylized
                        
                        # 新しい座標を計算
                        x0 = int(x_original - x_stylized * ratio_w)
                        y0 = int(y_original - y_stylized * ratio_h)
                        
                        # サイズを元画像のバウンディングボックスに合わせてリサイズ
                        new_w = int(iw * w_original / w_stylized)
                        new_h = int(ih * h_original / h_stylized)
                        stylized_face_resized = cv2.resize(stylized_image.numpy_view(), (new_w, new_h))
                        stylized_face_resized = cv2.cvtColor(stylized_face_resized, cv2.COLOR_BGR2RGB)

                        # 重ね合わせ
                        frame[y0:y0+new_h, x0:x0+new_w] = stylized_face_resized

        # 後処理
#        if stylized_image is not None:
#            stylized_image = cv2.cvtColor(
#                stylized_image.numpy_view(),
#                cv2.COLOR_BGR2RGB,
#            )

        # 描画
 #       debug_image: Any = copy.deepcopy(frame)
        debug_image = draw_debug(
            frame,
 #           debug_image,
            display_fps,
        )

        # キー処理(ESC：終了)
        key: int = cv2.waitKey(1)
        if key == 27:  # ESC
            break

        # 画面反映
        cv2.imshow('MediaPipe Face Stylization Demo Input', debug_image)
#        if stylized_image is not None:
#            cv2.imshow(
#                'MediaPipe Face Stylization Demo Output',
#                stylized_image,
#            )

    cap.release()
    cv2.destroyAllWindows()


def draw_debug(
    image: Any,
    display_fps: float,
) -> Any:

    # FPS
    cv2.putText(
        image,
        "FPS:" + str(display_fps),
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    return image


if __name__ == '__main__':
    main()
