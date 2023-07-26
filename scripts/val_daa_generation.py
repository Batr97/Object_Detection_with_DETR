from pycocotools.coco import COCO
import requests
import os
import json


# Извлекаем категории из датасета MS-COCO и сохраняем по 5 изображений каждой категории
def save_imgs(inst_path, save_path):
    coco = COCO(inst_path)
    cats = coco.loadCats(coco.getCatIds())
    nms = [cat['name'] for cat in cats]
    
    for cat in nms:
        catIds = coco.getCatIds(catNms=[cat])
        imgIds = coco.getImgIds(catIds=catIds)
        images = coco.loadImgs(imgIds)
        # Сохраним изображения
        for im in images[:5]:
            img_data = requests.get(im['coco_url']).content
            with open(save_path + im['file_name'], 'wb') as handler:
                handler.write(img_data)


def open_files(path):
    _, _, files = next(os.walk(path))
    return files


# Теперь изменим файл аннотации в соответствии со скаченными изображениями
def change_ann_file(annotations_file, images_dir, updated_annotations_file):
    downloaded_images = open_files(images_dir)

    with open(annotations_file, 'r') as f:
        coco_data = json.load(f)

    filtered_images = [image for image in coco_data['images'] if image['file_name'] in downloaded_images]
    filtered_image_ids = {image['id'] for image in filtered_images}
    filtered_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] in filtered_image_ids]

    coco_data['images'] = filtered_images
    coco_data['annotations'] = filtered_annotations
    with open(updated_annotations_file, 'w') as f:
        json.dump(coco_data, f)


# Загрузим картинки по аннотации
load_dataset = False
if load_dataset:
    inst_path = 'annotations_trainval/annotations/'
    save_path = 'data'
    save_imgs(os.path.join(inst_path, 'instances_train2017.json'), os.path.join(save_path, 'train'))
    save_imgs(os.path.join(inst_path, 'instances_val2017.json'), os.path.join(save_path, 'validation'))

# Обновили файлы аннотации с префиксом _filterd
change_ann_file(os.path.join(inst_path, 'instances_train2017.json'), os.path.join(save_path, 'train'), os.path.join('annotations_trainval', 'instances_train2017_filtered.json'))
change_ann_file(os.path.join(inst_path, 'instances_val2017.json'), os.path.join(save_path, 'validation'), os.path.join('annotations_trainval', 'instances_val2017_filtered.json'))