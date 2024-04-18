import flask

blueprint = flask.Blueprint(
    'style_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/style_file', methods=["GET"])
def get_style(font_family='-', font_color='black'):
    answer = dict()
    answer['font'] = {
        'size': flask.request.args.get('font_size'),
        'family': flask.request.args.get('font_family'),
        'font_color': flask.request.args.get('font_color')
    }
    return flask.jsonify(answer)
