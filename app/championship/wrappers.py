"""Wrappers for championship data management."""

from functools import wraps
from flask import abort


def extract_param_from_kwargs(kwargs):
    """Extract params value from kwargs.

    Returns:
        Extracted value or raises value error.

    """
    if kwargs is None:
        raise ValueError('No kwargs.')

    val = None
    for key in kwargs.keys():
        if key == kwargs['param_name']:
            val = kwargs[key]

    if val is None:
        raise ValueError('No ' + kwargs['param_name'] + 'in kwargs.')

    return val


def verify_mode(funct):
    """Verify state is correct."""
    @wraps(funct)
    def decorated_function(*args, **kwargs):
        """Decorator."""
        kwargs['param_name'] = 'mode'
        mode = extract_param_from_kwargs(kwargs)
        kwargs.pop('param_name', None)

        if mode not in ['all', 'specific']:
            abort(404)

        return funct(*args, **kwargs)

    return decorated_function
