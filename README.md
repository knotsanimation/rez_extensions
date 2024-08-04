# rez_extensions

Extend rez behavior using its native plugins features.

# development

- perform necessary changes
- commit and push
- check [knots-pipe-internals](https://github.com/knotsanimation/knots-pipe-internals) to deploy on server

# content

## include/

**Install:**

Path to the directory must be added to the `package_definition_python_path` config key.

**Usage:**

It's content can then be used with [the `include` decorator](https://rez.readthedocs.io/en/stable/package_definition.html#sharing-code-across-installed-packages).

**Example:**

```python
name = "myPackage"

@include("rezprovides")
def commands():
    rezprovides.is_provided(this.name, env, defined)
    # ...
```

## rezplugins/

**Install:**

The _root_ of this repository must be added to the rez's config 
[`plugin_path`](https://rez.readthedocs.io/en/stable/configuring_rez.html#plugin_path).

### release_vcs/

**Usage:**

To be used with `rez-release` `--vcs` argument.

- `none`: to release without using a vcs at all
- `simple`: store the changelog in a `CHANGELOG.md` file at root

### release_hook

**Install:**

Enable each hook in the rez config file :

```yaml
release_hooks:
  - doc-publish
```

**Configure:**

```yaml
# configure settings
plugins:
  release_hooks:
    doc-publish:
      # name of the attributes in the package.py of the package being released 
      publish_command_attr_name: doc_publish_command
      publish_require_attr_name: doc_publish_requires
```