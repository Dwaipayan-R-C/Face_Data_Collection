import pymongo
from bson.json_util import dumps
import json
import sys
import ast



class door():

    def __init__(self):
        pass

    def mainfuc(self):
        json_dict = sys.argv[1]
        # json_dict = "G:/PRACTICE/SOLIDWORKS/faceData.json"
        f = open(json_dict,)
        
        # json_dict = sys.argv[1]
        # print(type(json_dict))
        final_json = json.load(f)
        # final_dictionary  = ast.literal_eval(json_dict)
        # final_dictionary  = json.loads(json_dict)
        # print(final_json)
        
        
        
        
    #     # DB Connection
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["FNP"]
        # myCol = mydb["Door_Data"]

        mycol_new = mydb["door_data_py"]
        mycol_new.drop()

    #     _data = []
    #     main_dict = {}

        # for data in final_json:
        #     _data.append(data)
    #     # for data in myCol.find():
    #     #     _data.append(data)

    # for panel_data in _data:
        for body_inside_key, body_inside_val in final_json.items():
        # for body_inside_key, body_inside_val in panel_data.items():
            face_count = 0
            if body_inside_key != "_id":
                body_name = body_inside_key
                face_dict = []
                face_main_dict = {}
                for face_inside_key, face_inside_val in body_inside_val.items():
                    face_name = face_inside_key
                    # if face_inside_val['Point 1']['_v']['x'] == face_inside_val['Point 2']['_v']['x'] and face_inside_val['Point 2']['_v']['x'] == face_inside_val['Point 3']['_v']['x']:
                    if face_inside_val['Point 1']['x'] == face_inside_val['Point 2']['x'] and face_inside_val['Point 2']['x'] == face_inside_val['Point 3']['x']:
                        axis_val = "x"
                    elif face_inside_val['Point 1']['y'] == face_inside_val['Point 2']['y'] and face_inside_val['Point 2']['y'] == face_inside_val['Point 3']['y']:
                    # elif face_inside_val['Point 1']['_v']['y'] == face_inside_val['Point 2']['_v']['y'] and face_inside_val['Point 2']['_v']['y'] == face_inside_val['Point 3']['_v']['y']:
                        axis_val = "y"
                    elif face_inside_val['Point 1']['z'] == face_inside_val['Point 2']['z'] and face_inside_val['Point 2']['z'] == face_inside_val['Point 3']['z']:
                    # elif face_inside_val['Point 1']['_v']['z'] == face_inside_val['Point 2']['_v']['z'] and face_inside_val['Point 2']['_v']['z'] == face_inside_val['Point 3']['_v']['z']:
                        axis_val = "z"
                    face_count = face_count + 1
                    area_val = self.area_function(
                        face_inside_val, axis_val)
                    points  ={}
                    for points_inside_key,points_inside_val in face_inside_val.items():
                        if points_inside_key!= "persistentId":
                            points.update({points_inside_key:points_inside_val})
                                
                    face_dict.append(
                        {'faceName': face_name, 'areaValue': area_val, 'points': points, "Axis": axis_val,'persistenId': face_inside_val['persistentId']})

                face_in_body = face_count
                # face_main_dict.update({'bodyName':body_inside_key,'facesInBodies':face_in_body,'faceInBodies':face_dict})

                main_dict = {'bodyName': body_inside_key, "facesInBodies": face_in_body,
                             "faceDetails": face_dict, }
                mycol_new = mydb["door_data_py"]
                mycol_new.insert_one(main_dict)

        cursor = mycol_new.find({})

        json_file = "G:/PRACTICE/python packages/fnp.json"

        with open(json_file, 'w') as file:
            file.write('[')
            for document in cursor:
                file.write(dumps(document))
                file.write(',')
            file.write(']')
        print("DONE")



    def area_function(self, face_inside_val, axis_val):
        if axis_val == 'z':
            if face_inside_val['Point 1']['x'] != face_inside_val['Point 2']['x']:
                distance1 = self.distance(
                    face_inside_val['Point 1']['x'], face_inside_val['Point 2']['x'])
            else:
                distance1 = self.distance(
                    face_inside_val['Point 2']['x'], face_inside_val['Point 3']['x'])
            if face_inside_val['Point 1']['y'] != face_inside_val['Point 2']['y']:
                distance2 = self.distance(
                    face_inside_val['Point 1']['y'], face_inside_val['Point 2']['y'])
            else:
                distance2 = self.distance(
                    face_inside_val['Point 2']['y'], face_inside_val['Point 3']['y'])

        elif axis_val == 'x':
            if face_inside_val['Point 1']['y'] != face_inside_val['Point 2']['y']:
                distance1 = self.distance(
                    face_inside_val['Point 1']['y'], face_inside_val['Point 2']['y'])
            else:
                distance1 = self.distance(
                    face_inside_val['Point 2']['y'], face_inside_val['Point 3']['y'])
            if face_inside_val['Point 1']['z'] != face_inside_val['Point 2']['z']:
                distance2 = self.distance(
                    face_inside_val['Point 1']['z'], face_inside_val['Point 2']['z'])
            else:
                distance2 = self.distance(
                    face_inside_val['Point 2']['z'], face_inside_val['Point 3']['z'])

        elif axis_val == 'y':
            if face_inside_val['Point 1']['x'] != face_inside_val['Point 2']['x']:
                distance1 = self.distance(
                    face_inside_val['Point 1']['x'], face_inside_val['Point 2']['x'])
            else:
                distance1 = self.distance(
                    face_inside_val['Point 2']['x'], face_inside_val['Point 3']['x'])
            if face_inside_val['Point 1']['z'] != face_inside_val['Point 2']['z']:
                distance2 = self.distance(
                    face_inside_val['Point 1']['z'], face_inside_val['Point 2']['z'])
            else:
                distance2 = self.distance(
                    face_inside_val['Point 2']['z'], face_inside_val['Point 3']['z'])

        return distance1 * distance2
# def area_function(self, face_inside_val, axis_val):
#     if axis_val == 'z':
#         if face_inside_val['Point 1']['_v']['x'] != face_inside_val['Point 2']['_v']['x']:
#             distance1 = self.distance(
#                 face_inside_val['Point 1']['_v']['x'], face_inside_val['Point 2']['_v']['x'])
#         else:
#             distance1 = self.distance(
#                 face_inside_val['Point 2']['_v']['x'], face_inside_val['Point 3']['_v']['x'])
#         if face_inside_val['Point 1']['_v']['y'] != face_inside_val['Point 2']['_v']['y']:
#             distance2 = self.distance(
#                 face_inside_val['Point 1']['_v']['y'], face_inside_val['Point 2']['_v']['y'])
#         else:
#             distance2 = self.distance(
#                 face_inside_val['Point 2']['_v']['y'], face_inside_val['Point 3']['_v']['y'])

#     elif axis_val == 'x':
#         if face_inside_val['Point 1']['_v']['y'] != face_inside_val['Point 2']['_v']['y']:
#             distance1 = self.distance(
#                 face_inside_val['Point 1']['_v']['y'], face_inside_val['Point 2']['_v']['y'])
#         else:
#             distance1 = self.distance(
#                 face_inside_val['Point 2']['_v']['y'], face_inside_val['Point 3']['_v']['y'])
#         if face_inside_val['Point 1']['_v']['z'] != face_inside_val['Point 2']['_v']['z']:
#             distance2 = self.distance(
#                 face_inside_val['Point 1']['_v']['z'], face_inside_val['Point 2']['_v']['z'])
#         else:
#             distance2 = self.distance(
#                 face_inside_val['Point 2']['_v']['z'], face_inside_val['Point 3']['_v']['z'])

#     elif axis_val == 'y':
#         if face_inside_val['Point 1']['_v']['x'] != face_inside_val['Point 2']['_v']['x']:
#             distance1 = self.distance(
#                 face_inside_val['Point 1']['_v']['x'], face_inside_val['Point 2']['_v']['x'])
#         else:
#             distance1 = self.distance(
#                 face_inside_val['Point 2']['_v']['x'], face_inside_val['Point 3']['_v']['x'])
#         if face_inside_val['Point 1']['_v']['z'] != face_inside_val['Point 2']['_v']['z']:
#             distance2 = self.distance(
#                 face_inside_val['Point 1']['_v']['z'], face_inside_val['Point 2']['_v']['z'])
#         else:
#             distance2 = self.distance(
#                 face_inside_val['Point 2']['_v']['z'], face_inside_val['Point 3']['_v']['z'])

#     return distance1 * distance2

    def distance(self, x, y):
        if x >= y:
            result = x - y
        else:
            result = y - x
        return result

    


obj_data = door()
obj_data.mainfuc()

