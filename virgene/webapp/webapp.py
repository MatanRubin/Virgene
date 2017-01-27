import itertools
import html

from flask import Flask, render_template, request

from config_mgr import ConfigMgr
app = Flask(__name__)

config_mgr = ConfigMgr()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/configure")
def configure():
    default_config = config_mgr.build_default_config()

    builtins = [
        x for x in default_config.features if x.feature_type == 'Builtin']
    builtins_html = [
        render_template('feature.html', feature=x) for x in builtins]

    plugins = [
        x for x in default_config.features if x.feature_type == 'Plugin']
    plugins_html = [
        render_template('feature.html', feature=x) for x in plugins]

    snippets = [
        x for x in default_config.features if x.feature_type == 'Snippet']
    snippets_html = [
        render_template('feature.html', feature=x) for x in snippets]

    result = render_template("configure.html",
                             builtins=builtins_html,
                             plugins=plugins_html,
                             snippets=snippets_html)
    return result


def form_to_json(form):
    feature_configs = {}
    for key in form:
        feature_name, option_identifier = key.replace(']', '').split('[')
        value = form.getlist(key)
        if len(value) == 1:
            value = value[0]
        if feature_name not in feature_configs.keys():
            feature_configs[feature_name] = {}
        feature_configs[feature_name][option_identifier] = value
    return feature_configs


@app.route("/vimrc", methods=['POST'])
def vimrc():
    default_config = config_mgr.build_default_config()
    form_dict = form_to_json(request.form)
    default_config.apply_config(form_dict)
    vimrc_str = config_mgr.generate(default_config)
    return r"<pre>" + html.escape(vimrc_str) + r"</pre>"


if __name__ == "__main__":
    app.run()
