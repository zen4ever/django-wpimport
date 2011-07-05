Django WordPress importer
=========================

An utility app that helps you to create custom WordPress importer
for your Django blog application.

Install instructions
--------------------

To install run:

::

  pip install -e git://github.com/zen4ever/django-wpimport.git#egg=django-wpimport


Then add wpimport to your INSTALLED_APPS:

::
  
  INSTALLED_APPS = [
      # ...
      'wpimport',
  ]

Getting started
---------------

In your WordPress admin visit Tools > Export, and download export file.

Run following command

::

  python manage.py wordpress_import -v 2 path_to_your_export_file.xml

This will parse your WXR file and print out resulting python data.
It might also print out tags it couldn't match. If you want just see only
unmatched tags output, but not the resulting data, run the command with
a verbosity 1.

Now you can write your own custom importer and place it somewhere in your
python path. Good place would be an `importer.py` file in your blog app.

This module should contain `WordpressImporter` class, inherited from
`wpimport.importer.BaseWordpressImporter`.
To access parsed data you should override `handle_default` method,
something along the lines:

::

  from wpimport.importer import BaseWordpressImporter


  class WordpressImporter(BaseWordpressImporter):

      def handle_default(self, tag):
          result = super(WordpressImporter, self).handle_default(tag)

          # do something with the result


If you interested in just one type of data, you can define `handle_post`,
`handle_page` or `handle_attachments` methods on your `WordpressImporter`
class.

To use your custom importer just run:

::

  python manage.py wordpress_import -v 2 --importer="parent_module.interpreter" path_to_your_export_file.xml

Replace "parent_module.interpreter" with a module which contains your
`WordpressImporter` class.
