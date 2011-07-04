from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module

from wpimport.importer import BaseWordpressImporter


class Command(BaseCommand):
    args = '<filename> - path to whr file'
    help = 'Imports data from .whr file to an app models using custom importer'

    option_list = BaseCommand.option_list + (
        make_option('--appname',
            action='store',
            dest='appname',
            type="string",
            help='Fully qualified name of an app'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("This command takes exactly one argument")
        filename = args[0]
        appname = options.get('appname', '')

        klass = BaseWordpressImporter
        if appname:
            try:
                importer_module = import_module(appname+'.importer')
                if hasattr(importer_module, 'WordpressImporter'):
                    klass = getattr(importer_module, 'WordpressImporter')
            except ImportError:
                self.stdout.write("No importer module has been found, using default importer\n")

        importer = klass(filename, verbosity=int(options['verbosity']))
        importer.parse()
