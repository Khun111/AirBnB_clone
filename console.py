#!/usr/bin/python3
'''
Command line interpreter for the Airbnb cmd interface
'''

import cmd
import shlex
import re

import models
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.review import Review

CLASSES = [
    "BaseModel",
    "User",
    "City",
    "Place",
    "State",
    "Amenity",
    "Review"
]


class HBNBCommand(cmd.Cmd):
    """Airbnb command processor/interpreter."""

    prompt = '(hbnb) '
    storage = models.storage

    def do_EOF(self, line):
        '''End the program on EOF'''
        return True

    def do_quit(self, line):
        '''End the program when quit cmd is typed'''
        return True

    def emptyline(self):
        '''Do nothing when an empty line is entered'''
        pass

    def do_create(self, line):
        '''Create a new instance of BaseModel, saves it (to the JSON file)
        and prints the id.'''
        arr = shlex.split(line)
        if len(arr) == 0:
            print('** class name missing **')
            return None
        if arr[0] not in CLASSES:
            print("** class doesn't exist **")
            return None
        '''Code that does actual work'''
        print(eval(arr[0])().id)
        self.storage.save()

    def do_show(self, line):
        '''Print the string representation of an instance
        based on the class name and id'''
        arr = shlex.split(line)
        if len(arr) == 0:
            print('** class name missing **')
            return None
        if arr[0] not in CLASSES:
            print("** class doesn't exist **")
            return None
        if len(arr) < 2:
            print("** instance id missing **")
            return None
        '''Code that deos the main work'''
        key = "{}.{}".format(arr[0], arr[1])
        if key not in self.storage.all():
            print("** no instance found **")
        else:
            print(self.storage.all()[key])

    def do_destroy(self, line):
        ''' Delete an instance based on the class name and
        id (save the change into the JSON file).'''
        arr = shlex.split(line)
        if len(arr) == 0:
            print('** class name missing **')
            return None
        if arr[0] not in CLASSES:
            print("** class doesn't exist **")
            return None
        if len(arr) < 2:
            print("** instance id missing **")
            return None
        '''Code that deos the main work'''
        key = "{}.{}".format(arr[0], arr[1])
        if key in self.storage.all():
            del self.storage.all()[key]
            self.storage.save()
        else:
            print("** no instance found **")

    def do_all(self, line):
        '''Print all string representation of all instances based
        or not on the class name.'''
        arr = shlex.split(line)
        objects = self.storage.all().values()
        if not arr:
            print([str(obj) for obj in objects])
        else:
            if arr[0] not in CLASSES:
                print("** class doesn't exist **")
            else:
                print([str(obj) for obj in objects
                       if arr[0] == obj.__class__.__name__])

    def do_update(self, line):
        '''
        Update an instance based on the class name and id by adding or
        updating attribute
        (save the change into the JSON file)
        '''
        arr = shlex.split(line)
        if len(arr) == 0:
            print('** class name missing **')
            return None
        if arr[0] not in CLASSES:
            print("** class doesn't exist **")
            return None
        if len(arr) < 2:
            print("** instance id missing **")
            return None
        if len(arr) < 3:
            print("** attribute name missing **")
            return None
        if len(arr) < 4:
            print("** value missing **")
            return None
        '''Code that deos the main work'''
        instance_id = "{}.{}".format(arr[0], arr[1])
        if instance_id in self.storage.all():
            obj = self.storage.all()[instance_id]
            if arr[2] in type(obj).__dict__:
                v_type = type(obj.__class__.__dict__[arr[2]])
                setattr(obj, arr[2], v_type(arr[3]))
            else:
                setattr(obj, arr[2], arr[3])
        else:
            print("** no instance found **")

        self.storage.save()

    def do_count(self, line):
        """Retrieve the number of instances of a class"""
        arr = shlex.split(line)
        count = 0
        for obj in models.storage.all().values():
            if arr[0] == type(obj).__name__:
                count += 1
        print(count)

    def default(self, line):
        """Default behaviour for cmd module when input is invalid"""

        action_map = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update,
            "create": self.do_create
        }

        match = re.search(r"\.", line)
        if match:
            line1 = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", line1[1])
            if match:
                command = [line1[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in action_map:
                    if command[0] != "update":
                        call = "{} {}".format(line1[0], command[1])
                        return action_map[command[0]](call)
                    else:
                        call = "{} {}".format(line1[0], command[1])
                        if "{" in call:
                            call = call.replace(",", "")
                            call = call.replace("{", "")
                            call = call.replace("}", "")
                            call = call.replace(":", " ")
                            call = call.replace(",", "")
                            call = shlex.split(call)
                            while (len(call) > 2):
                                action_map["update"](" ".join(call))
                                del call[2:4]
                            return None
                        else:
                            call = call.replace(",", "")
                            return action_map["update"](call)

        print("*** Unknown syntax: {}".format(line))
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
