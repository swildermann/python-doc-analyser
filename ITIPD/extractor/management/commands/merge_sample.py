from django.core.management.base import BaseCommand, CommandError
from extractor.merge_goldsample import *


class Command(BaseCommand):
    help = 'merges the samples of two coders'

    def handle(self, *args, **options):
        self.stdout.write("***START***")

        all_units = MappingUnitToUser.objects.filter(user__groups__name='Students')\
            .distinct('documentation_unit')
        status_array = []
        for unit in all_units:
            first_mapped_id = MappingUnitToUser.objects.get(pk=unit.id)
            all_other_mapped= MappingUnitToUser.objects.exclude(user=first_mapped_id.user)\
                .filter(user__groups__name="Students",
                        documentation_unit=unit.documentation_unit,
                        already_marked=True)
            if len(all_other_mapped)>1:
                raise CommandError("!Found to many mappings to this unit: "+str(unit.documentation_unit.id)+
                                   ". Please have a close look to the code!! "+str(len(all_other_mapped)))
            if len(all_other_mapped)==0:
                self.stdout.write("Found no additional mappings to this unit: "+str(unit.documentation_unit.id)+
                                  " Please have a close look to the code! "+str(len(all_other_mapped)))
                continue
            second_mapped_id = all_other_mapped[0]

            self.stdout.write(".",ending='')
            first_markings = MarkedUnit.objects.filter(user=first_mapped_id.user,
                                                       documentation_unit=first_mapped_id.documentation_unit)\
                                                       .values('id', 'char_range','knowledge_type')
            second_markings = MarkedUnit.objects.filter(user=second_mapped_id.user,
                                                        documentation_unit=second_mapped_id.documentation_unit)\
                                                        .values('id', 'char_range','knowledge_type')
            if len(first_markings)==len(second_markings)==0:
                # TODO: save a empty unit to the endresult (and count them maybe?)
                continue
            if len(first_markings)==0 or len(second_markings)==0:
                #TODO save that with markings or without? Save without and count them additional?
                continue

            first_results = merge_markings(first_markings)
            second_results = merge_markings(second_markings)


            #Markierungen vergleichen
                #Bei Konfusion: Pluspunkt vergeben
                #Bei Gleichheit: Gutachter mit mehr Pluspunkten bevorzugen (Markierung übernehmen) (ODER auf "besseren" Gutachter zurückgreifen (Markierung übernehmen))
                #Weder Konfusion noch Gleichheit: Erst Pluspunkte, dann bessere Gutachter


