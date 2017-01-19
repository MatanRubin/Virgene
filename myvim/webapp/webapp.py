import itertools

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

    result = render_template(
        "configure.html", builtins=builtins_html, plugins=plugins_html, snippets=snippets_html)
    return result


def form_to_json(form):
    # outputs a list of list.
    # each sublist is of the form [<plugin name>, <option name>, <value>]
    plugin_option_value = [x.replace(']', '').split('[') + [form[x]]
                           for x in form]
    sorted_plugin_option_value = sorted(
        plugin_option_value, key=lambda x: x[0])
    plugins = [
        {
            "name": key,
            "options": [{option[1]: option[2]} for option in group]
        }
        for key, group in itertools.groupby(sorted_plugin_option_value, lambda x: x[0])
    ]
    return plugins


@app.route("/vimrc", methods=['POST'])
def vimrc():
    default_config = config_mgr.build_default_config()
    form_json = form_to_json(request.form)
    print(form_json)
    return r"<pre>" + config_mgr.generate(default_config) + r"</pre>"


if __name__ == "__main__":
    app.run()
