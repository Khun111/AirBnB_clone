#!/usr/bin/python3
'''
Module for FileNotFoundError Class
'''
import json

class FileStorage:
    '''Class for Serialization and Deserialization'''
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        '''Returns the dictionary __objects'''
        return self.__objects

    def new(self, obj):
	    '''
        Sets in __objects the obj with key <obj class name>.id
        Args: obj
        '''
        self.__objects[f'{obj.__class__.__name__}.{obj.id}'] = obj
        
    def save(self):
	    '''
        Serializes __objects to the JSON file (path: __file_path)
        '''
        obj_dict = {k: v.to_dict() for k, v in self.__objects.items() if hasattr(v, 'to_dict')}
        with open(self.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    def reload(self):
	    '''
        Deserializes the JSON file to __objects (only if the JSON file\
        (__file_path) exists ; otherwise, do nothing.
        '''
        try:
            with open(self.__file_path, 'r') as file:
                obj_load = json.load(file)
                for k, v in obj_load.items():
                    self.__objects[k]  = eval(f'{v.__class__.__name__}(**v)')
        except FileNotFoundError:
            pass

