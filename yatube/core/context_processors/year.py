from datetime import datetime


def year(request):
    """ Add current year"""
    year = datetime.today().year
    return {
        'year': year,
    }
