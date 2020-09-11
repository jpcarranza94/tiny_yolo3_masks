import json
num = 1801

from os import listdir

annotation_list = listdir('medical_mask/annotations')
image_list = listdir('medical_mask/images')
final_string = ""
text_file = open("train.txt", "w")

dict = {'hijab_niqab': 2, 'mask_colorful': 1, 'mask_surgical': 1, 'face_no_mask': 0, 'face_with_mask_incorrect': 2, 'face_with_mask': 1, 'face_other_covering': 2, 'scarf_bandana':2, 'balaclava_ski_mask':2, 'face_shield':4, 'other': 3, 'gas_mask':1, 'turban':3, 'helmet':3, 'sunglasses':3, 'hair_net':3, 'hat': 3, 'goggles':3, 'hood':3, 'eyeglasses':3}

for i in range(0, len(annotation_list)):
	annotation_path = 'medical_mask/annotations/' + annotation_list[i]
	#print(annotation_path)
	with open(annotation_path) as f:
		data = json.load(f)	
	image_path = 'medical_mask/images/' + image_list[i] + " "

	str_to_add = image_path
	annotations_in_i = data.get('Annotations')
	#print(annotations_in_i)

	for j in range(0,len(annotations_in_i)):
		annotations = annotations_in_i[j]
		#print(annotations)
		for k in range(0,4):
			coord = annotations.get('BoundingBox')[k]
			str_to_add += str(coord) + ","
		class_data = annotations.get('classname')
		if j+1 < len(annotations_in_i):
			str_to_add += str(dict.get(class_data)) + " "
		else: 
			str_to_add += str(dict.get(class_data)) + "\n"
		print(str_to_add)

	final_string += str_to_add

text_file.write(final_string)
text_file.close()




 

