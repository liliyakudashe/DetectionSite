"""
Обработчик результатов детекции объектов на изображении.

Этот код выполняет следующие действия:
1. Подготавливает размеры целевых объектов.
2. Обрабатывает результаты детекции объектов, применяя пороговое значение 0.9.
3. Преобразует изображение в матрицу numpy.
4. Создает пустой список для обнаруженных объектов.
5. Обрабатывает каждый обнаруженный объект, добавляя его в список и рисуя на изображении рамку и подпись.
6. Сохраняет обработанное изображение в формате JPEG.
7. Создает запись обнаруженных объектов в базе данных Django.

Атрибуты:
    outputs (torch.Tensor): Результаты модели детекции объектов.
    image (PIL.Image): Исходное изображение для обработки.
    image_feed (ImageFeed): Объект модели ImageFeed, представляющий собой связанное изображение в базе данных.
    model (object): Обученная модель для детекции объектов.

Возвращает:
    bool: True, если обработка завершилась успешно, в противном случае False.

Исключения:
    ImageFeed.DoesNotExist: В случае, если объект ImageFeed не найден в базе данных.
"""

import cv2
import numpy as np
from django.core.files.base import ContentFile
from .models import ImageFeed, DetectedObject, DetectionHistory
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image

VOC_LABELS = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle",
    "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant",
    "sheep", "sofa", "train", "tvmonitor"
]


def process_image(image_feed_id):
    try:
        image_feed = ImageFeed.objects.get(id=image_feed_id)
        image_path = image_feed.image.path

        model_path = 'object_detection/mobilenet_iter_73000.caffemodel'
        config_path = 'object_detection/mobilenet_ssd_deploy.prototxt'
        net = cv2.dnn.readNetFromCaffe(config_path, model_path)

        img = cv2.imread(image_path)
        if img is None:
            print("Failed to load image")
            return False

        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 0.007843, (300, 300), 127.5)

        net.setInput(blob)
        detections = net.forward()

        detected_objects = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.6:
                class_id = int(detections[0, 0, i, 1])
                class_label = VOC_LABELS[class_id]
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = f"{class_label}: {confidence:.2f}"
                cv2.putText(img, label, (startX+5, startY + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                detected_object = DetectedObject.objects.create(
                    image_feed=image_feed,
                    object_type=class_label,
                    location=f"{startX},{startY},{endX},{endY}",
                    confidence=float(confidence)
                )
                detected_objects.append(detected_object)

        result, encoded_img = cv2.imencode('.jpg', img)
        if result:
            content = ContentFile(encoded_img.tobytes(), f'processed_{image_feed.image.name}')
            image_feed.processed_image.save(content.name, content, save=True)

        DetectionHistory.objects.create(
            user=image_feed.user,
            image=image_feed.image,
            processed_image=image_feed.processed_image,
            detected_objects=', '.join([obj.object_type for obj in detected_objects])
        )

        return True

    except ImageFeed.DoesNotExist:
        print("ImageFeed not found.")
        return False


def process_image_detect_other_model(image_feed_id):
    """Модель совершает классификацию изображения, рисует контуры на найденных объектах, сохраняет новое изображение,
    добавляет в базу данных, https://huggingface.co/facebook/detr-resnet-50"""
    try:
        image_feed = ImageFeed.objects.get(id=image_feed_id)
        image_path = image_feed.image.path
        image = Image.open(image_path)

        processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
        model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

        img_with_objects = np.array(image)

        detected_objects = []

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            object_label = model.config.id2label[label.item()]

            start_x, start_y, end_x, end_y = [int(coord) for coord in box]
            cv2.rectangle(img_with_objects, (start_x, start_y), (end_x, end_y), (255, 0, 255), 2)
            cv2.putText(img_with_objects, object_label, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 0, 255), 2)

            detected_object = DetectedObject.objects.create(
                image_feed=image_feed,
                object_type=model.config.id2label[label.item()],
                location=f"{start_x},{start_y},{end_x},{end_y}",
                confidence=float(round(score.item(), 3))
            )
            detected_objects.append(detected_object)

        rgb_image = cv2.cvtColor(img_with_objects, cv2.COLOR_BGR2RGB)

        result, encoded_img = cv2.imencode('.jpg', rgb_image)
        if result:
            content = ContentFile(encoded_img.tobytes(), f'processed_{image_feed.image.name}')
            image_feed.processed_image.save(content.name, content, save=True)

        DetectionHistory.objects.create(
            user=image_feed.user,
            image=image_feed.image,
            processed_image=image_feed.processed_image,
            detected_objects=', '.join([obj.object_type for obj in detected_objects])
        )

        return True
    except ImageFeed.DoesNotExist:
        print("ImageFeed not found.")
        return False
