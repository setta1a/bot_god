import os, django, sys
sys.path.insert(0, os.path.abspath(".."))  # For discovery of Python modules
sys.path.insert(0, os.path.abspath("."))  # For finding the django_settings.py file
os.environ['DJANGO_SETTINGS_MODULE'] = 'dj_project.settings'
django.setup()

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Bot_good'
copyright = '2023, Andrey Sitalo, Semyon Anikin, Valery Vasenev, Vikntoria Antonova, Pavel Kurnosov, Leonid Perkin, Alyona Smolkina, Vladimir Bykov, Artem Osipov'
author = 'Andrey Sitalo, Semyon Anikin, Valery Vasenev, Vikntoria Antonova, Pavel Kurnosov, Leonid Perkin, Alyona Smolkina, Vladimir Bykov, Artem Osipov'
release = 'v1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
