from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module

from wpimport.importer import BaseWordpressImporter


class Command(BaseCommand):
    args = '<filename> - path to WXR file'
    help = 'Imports data from WXR file to an app models using custom importer'

    option_list = BaseCommand.option_list + (
        make_option('--importer',
            action='store',
            dest='importer',
            type="string",
            help='Module which should contain `WordpressImporter` class'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("This command takes exactly one argument")
        filename = args[0]
        importer = options.get('importer', '')

        klass = BaseWordpressImporter
        if importer:
            try:
                importer_module = import_module(importer)
                if hasattr(importer_module, 'WordpressImporter'):
                    klass = getattr(importer_module, 'WordpressImporter')
            except ImportError:
                self.stdout.write("No importer module has been found, using default importer\n")

        importer = klass(filename, verbosity=int(options['verbosity']))
        importer.parse()
