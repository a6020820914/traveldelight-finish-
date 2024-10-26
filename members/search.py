from django.db.models import Q
from .models import Tour
from datetime import datetime

# (搜尋的條件判斷function，因為太長，所以放這裡)
def searchTour(startDate, endDate, tour_toursite, tour_tourday, tour_company, options):
    tours = Tour.objects.all()
    toursite_filter=Q()
    tourday_filter = Q()
    company_filter = Q()

    goDateIDlist=[]
    for inx, godate in zip(Tour.objects.all().values("id"), Tour.objects.all().values("goDate")): #每個行程的godate list
        for date in godate["goDate"].split(", "): #每個行程的godate list的date
            try:
                date=datetime.strptime(date.replace("'", "").replace("/", "-"),"%Y-%m-%d").date()
            except:
                continue
            if date >= startDate and date <= endDate:
                goDateIDlist.append(inx["id"])
                break 
    goDate_filter = Q(id__in=goDateIDlist)

    if tour_toursite!=None:
        toursite_filter=Q(toursite=tour_toursite)
        if tour_tourday!=None and tour_company!=None:
            
            for t in range(len(tour_tourday)):
                if "4" in tour_tourday:
                    tourday_filter |= Q(tourday__gte=int(tour_tourday[t]))
                else:
                    tourday_filter |= Q(tourday=int(tour_tourday[t]))
            
            for c in range(len(tour_company)):
                company_filter |= Q(company=tour_company[c]) 

            tours = Tour.objects.filter(goDate_filter &toursite_filter & tourday_filter & company_filter)
            # Sorting
            if options == "P":
                tours = tours.order_by('price')
            else:
                tours = tours.order_by('earlierGoDate')      
        else:
            tours = 'None'
    else:
        if (tour_tourday!=None) and (tour_company!=None):
            
            for t in range(len(tour_tourday)):
                if "4" in tour_tourday:
                    tourday_filter |= Q(tourday__gte=int(tour_tourday[t]))
                else:
                    tourday_filter |= Q(tourday=int(tour_tourday[t]))

            for c in range(len(tour_company)):
                company_filter |= Q(company=tour_company[c])
            tours = Tour.objects.filter(goDate_filter & tourday_filter & company_filter) 
            # Sorting
            if options == "P":
                tours = tours.order_by('price')
            else:
                tours = tours.order_by('earlierGoDate')
        else:
            tours = 'None'
    return tours


     
    