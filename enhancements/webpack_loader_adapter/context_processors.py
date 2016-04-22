'''
Translate template tags of webpack loader into Jinja2 context.
'''

from webpack_loader.templatetags import webpack_loader as tags


def render_bundle(bundle_name, extension=None, config='DEFAULT'):
    return tags.render_as_tags(
        tags._get_bundle(bundle_name, extension, config)
    )


def webpack_static(asset_name, config='DEFAULT'):
    return "{0}{1}".format(
        tags.get_loader(config).get_assets().get(
            'publicPath', getattr(tags.settings, 'STATIC_URL')
        ),
        asset_name
    )


def get_files(bundle_name, extension=None, config='DEFAULT'):
    """
    Returns all chunks in the given bundle.
    Example usage::

        {% get_files 'editor' 'css' as editor_css_chunks %}
        CKEDITOR.config.contentsCss = '{{ editor_css_chunks.0.publicPath }}';

    :param bundle_name: The name of the bundle
    :param extension: (optional) filter by extension
    :param config: (optional) the name of the configuration
    :return: a list of matching chunks
    """
    return list(tags._get_bundle(bundle_name, extension, config))


def webpack(request):
    return dict(
        render_bundle=render_bundle,
        get_files=get_files,
        webpack_static=webpack_static,
    )
