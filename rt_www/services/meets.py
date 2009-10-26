from rt_www.index.models import Meet
class Service:
    def get_results(self, year, limit):
        return [{'date':m.get_display_date(), 'name':m.name, 'meet_pool':m.meet_pool, 
            'city':m.city, 'state':m.state.code, 'country':m.country, 'results_link':m.results_link } 
                for m in Meet.objects.filter(date_start__year=int(year), 
                        results_link__isnull=False).exclude(results_link__exact='').order_by('-date_start')[:int(limit)] ]
service = Service()
