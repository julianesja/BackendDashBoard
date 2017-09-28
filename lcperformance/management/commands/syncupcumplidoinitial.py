#

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError



# Class MUST be named 'Command'
class Command(BaseCommand):
    help = 'Sincroniza la applicacion con expa'

    """def add_arguments(self, parser):
        parser.add_argument()"""


    def handle(self, *app_labels, **options):
        """
        app_labels - app labels (eg. myapp in "manage.py reset myapp")
        options - configurable command line options
        """

        # Return a success message to display to the user on success
        # or raise a CommandError as a failure condition
        from lcperformance.Process.LcPerformance import LcPerformance
        objLcPerformace = LcPerformance()
        objLcPerformace.SaveLcsInicial()
        raise CommandError('Only the default is supported')
