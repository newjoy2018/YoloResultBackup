import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = []
classes = ["truck","excavator","person","bulldozer","compactor roller","wheel loader","dumper","car"]  ##change to your own classes

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_add):
    image_add = os.path.split(image_add)[1]
    image_add = image_add[0:image_add.find('.',1)]

    in_file = open('/home/niuzhuo/YOLOv4/darknet/KITMoMa/xml/' + image_add + '.xml')
    out_file = open('/home/niuzhuo/YOLOv4/darknet/KITMoMa/labels/%s.txt'%(image_add), 'w')

    tree=ET.parse(in_file)
    root = tree.getroot()

    if root.find('size'):
 
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        if w==0:
            print("Wrong! width or height is 0:  "+image_add)
            os.remove("/home/niuzhuo/YOLOv4/darknet/KITMoMa/xml/"+image_add+".xml")
            #os.remove("G:/set/"+image_add+".xml")
            return

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text

            if cls not in classes or int(difficult)==1:
                continue

            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')

            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w,h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    else:
        print("Error! xml need size:  "+image_add)
        #os.remove("G:/set/"+image_add+".jpg")
        os.remove("/home/niuzhuo/YOLOv4/darknet/KITMoMa/xml/"+image_add+".xml")

image_adds = open("/home/niuzhuo/YOLOv4/darknet/KITMoMa/train.txt")
for image_add in image_adds:
    #print(image_add)
    #image_add = image_add.strip()
    #print (image_add)
    convert_annotation(image_add)
