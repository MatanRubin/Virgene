from os import path
from myvim.common_defs import BUILD_DIR
from myvim.myvim_file import ConfigMgr
from flask import Flask, render_template, request
app = Flask(__name__)

config_mgr = ConfigMgr()

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/configure")
def configure():
    default_config = config_mgr.get_default_config()

    builtins = [x for x in default_config.features if x.feature_type == 'Builtin']
    builtins_html = [render_template('feature.html', feature=x) for x in builtins]

    plugins = [x for x in default_config.features if x.feature_type == 'Plugin']
    plugins_html = [render_template('feature.html', feature=x) for x in plugins]

    snippets = [x for x in default_config.features if x.feature_type == 'Snippet']
    snippets_html = [render_template('feature.html', feature=x) for x in snippets]

    result = render_template("configure.html", builtins=builtins_html, plugins=plugins_html, snippets=snippets_html)
    return result


def form_to_json(form):
    form_dict = {x[0]: x[1] for x in form}
    print(form_dict)


@app.route("/vimrc", methods=['POST'])
def vimrc():
    test_config_path = path.join(BUILD_DIR, "default.json")
    config_mgr.default_config(test_config_path)
    form_json = form_to_json(request.form)
    return r"<pre>" + config_mgr.generate(test_config_path) + r"</pre>"


if __name__ == "__main__":
    app.run()

