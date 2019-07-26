"""Championship data management routes."""

import traceback
from json import loads, dumps
from flask import request, abort
from app.championship import data_management as dm
from app.championship.utils import ChampionshipDataUtil
from app.championship.wrappers import verify_mode


def get_data():
    """Get data from request."""
    data = None
    try:
        data = loads(request.json)
    except:
        data = request.json
    return data


@dm.route('/api/fixture/result/publish', methods=['POST'])
def publish_fixture_result():
    """Publish results method.

    Returns:
        JSON: Table object, or array of table objects.

    """
    if request.json is None:
        abort(400)

    try:
        data = get_data()
        standings = ChampionshipDataUtil.handle_fixture_results(data)

        return dumps(standings)
    except TypeError:
        traceback.print_exc()
        return {'message': 'Bad JSON.'}, 400
    except:
        traceback.print_exc()
        return {'message': 'Error occured.'}


@dm.route('/api/table/<string:mode>', methods=['GET'])
@verify_mode
def get_tables(mode):
    """Get tables endpoint.

    Args:
        mode: all or specific.
    Returns:
        JSON: Table object, or array of table objects.

    """
    try:
        data = None
        if mode == 'specific':
            # This should be array of dicts with group and league name.
            data = get_data()

        standings = ChampionshipDataUtil.get_tabels_for_groups(data)

        return dumps(standings)
    except TypeError:
        traceback.print_exc()
        return {'message': 'Bad JSON.'}, 400
    except:
        traceback.print_exc()
        return {'message': 'Error occured.'}


@dm.route('/api/fixture/result/filter', methods=['GET', 'POST'])
def filter_results():
    """Filter existing results.

    Returns:
        JSON: Existing filtered results.

    """
    try:
        data = get_data()
        res = ChampionshipDataUtil.filter_results(data)

        return dumps(res)
    except TypeError:
        traceback.print_exc()
        return {'message': 'Bad JSON.'}, 400
    except:
        traceback.print_exc()
        return {'message': 'Error occured.'}


@dm.route('/api/result/update', methods=['PUT'])
def update_result():
    """Update result.

    Returns:
        Status message.

    """
    try:
        data = get_data()
        ChampionshipDataUtil.update_fixture_results(data)

        return {'message': 'Success.'}
    except TypeError:
        traceback.print_exc()
        return {'message': 'Bad JSON.'}, 400
    except:
        traceback.print_exc()
        return {'message': 'Error occured.'}
