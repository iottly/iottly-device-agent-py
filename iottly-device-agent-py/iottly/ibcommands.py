import copy
import datetime
import hashlib
import logging
import json

class Command(object):
    def __init__(self, name, descr, cmd_msg, autoset=None, warn=False, show=True):
        self.desc = descr
        self.name = name
        self.cmd_msg = cmd_msg
        self.command = None
        self.warn = warn
        self.show = show
        self.autoset = autoset
        self._parse_json()

    def _parse_json(self):
        if self.cmd_msg.startswith('/json '):
            try:
                self.command = json.loads(self.cmd_msg[6:])
            except ValueError as e:
                logging.warn('JSON parsing failed', e, self.cmd_msg)
        else:
            self.command = {}

    def _apply_key_value(self, key_parts, obj, value):
        if len(key_parts) == 1:
            obj[key_parts[0]] = value
        else:
            self._apply_key_value(key_parts[1:], obj[key_parts[0]], value)

    '''
    Each command takes an optional autoset function which updates the dictionary with default
    values at runtime
    '''
    def apply_args(self, **kwargs):
        if kwargs is None:
            kwargs = {}

        if self.autoset:
            self.autoset(kwargs)
        obj = copy.deepcopy(self.command)
        for k, v in kwargs.items():
            self._apply_key_value(k.split('.'), obj, v)

        return obj

    '''
    This method accepts optional keyword arguments that will be applied to the commands object.
    The key value pairs represent a flattened view into the command object. For example,
    command = {
        'key_1' : {
            'key_2': value1
        },
        'key_23': value2
    }
    If we want to override key_2 with value3 we would pass in **{ 'key_1.key_2': value3 }
    '''
    def to_json(self, **kwargs):
        if not self.cmd_msg.startswith('/json '):
            return
        obj = self.apply_args(**kwargs)
        return obj

    def __str__(self):
        return "-".join((self.name, self.desc, self.cmd_msg))

    def hash(self):
        return hashlib.md5(str(self)).hexdigest()


    @staticmethod
    def deserialize(ui_command_def):
        cmd = copy.deepcopy(ui_command_def)
        metadata = cmd.pop('metadata')
        return Command(metadata['type'], metadata['description'], '/json {}'.format(metadata['jsonfmt']))
