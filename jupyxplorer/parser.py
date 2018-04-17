import yaml
from cerberus import Validator

SCHEMA = {
    'dataset': {
        'type': 'string',
        'required': True,
        'empty': False
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


v = Validator(SCHEMA)


def load_yaml(yaml_path):
    with open(yaml_path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exception:
            if hasattr(exception, 'problem_mark'):
                mark = exception.problem_mark
                return "syntax incorrect. The error position is (line %s, column %s)" % (mark.line + 1, mark.column + 1)


def validate_data(document):
    return v.validate(document)


def parser_errors(document):
    v.validate(document)
    return v.errors
