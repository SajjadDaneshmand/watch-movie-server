from flask import Flask, redirect, url_for, request, session, flash, render_template, send_from_directory
import functools
import sys
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='d0c90397995b2c31834b20d78394eaa0',
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    return app


app = create_app()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))

        return view(**kwargs)
    return wrapped_view


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == '123654':
            session['user_id'] = True
            return redirect(url_for('files'))
        else:
            error = 'password isn\'t correct'
            flash(error)
            return redirect(request.url)
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
@login_required
def files():
    path = sys.argv[1] if len(sys.argv) > 1 else '/data/data/com.termux/files/home/storage/shared/Download/Telegram'
    listdir = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

    if request.method == 'POST':
        if request.form['filenames'] in listdir:
            filename = request.form['filenames']
            type_of_file = filename.rsplit('.')[-1]
            film_ext = ['webm', 'mkv', 'flv', 'flv', 'gif', 'wmv', 'mp4']
            if type_of_file in film_ext:
                complete_path_file = os.path.join(path, filename)
                return render_template('film.html', path=complete_path_file)
            return send_from_directory(path, filename)

    return render_template('files.html', files=listdir)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

