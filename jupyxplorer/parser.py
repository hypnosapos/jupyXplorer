# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import yaml
from cerberus import validator, Validator

SCHEMA = {
    'dataset': {
        'type': 'dict',
        'required': True,
        'schema': {
            'source': {
                'type': 'string',
                'required': True,
                'empty': False
            },
            'type': {
                'type': 'string',
                'required': False,
                'empty': False
            }
        }
    },
    'requirements': {
        'type': 'list',
        'required': False,
        'schema': {
            'type': 'string'
        }
    },
    'fields': {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'name': {
                    'type': 'string',
                    'required': True,
                    'empty': False
                },
                'type': {
                    'type': 'string',
                    'required': False,
                    'empty': False
                }
            }
        }
    }
}

_v = Validator(SCHEMA)


def load_yaml(yaml_path, schema_validation=True):
    """
    Read a YAML file
    :param yaml_path: file path
    :param schema_validation: validate file against YAML schema
    :return: yaml document
    """
    with open(yaml_path, 'r') as stream:
        try:
            document = yaml.load(stream)
            if schema_validation:
                if not _v.validate(document):
                    raise Exception("YAML SchemaError: %s" % _v.errors)
            return document
        except yaml.YAMLError as exception:
            if hasattr(exception, 'problem_mark'):
                mark = exception.problem_mark
                raise Exception("YAML SyntaxError. The error position is (line %s, column %s)"
                                "" % (mark.line + 1, mark.column + 1))
        except validator.DocumentError as exc:
            raise Exception("YAML SyntaxError: %s" % exc)
