from django import template
from datetime import datetime
import math
from members.models import Rating
from django.db.models import Q

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

#評論star
@register.filter(name='range_filter')
def range_filter(value):
    return range(1, value+1)

@register.filter(name='remaining_range')
def remaining_range(value):
    remaining_value = 5 - value
    return range(remaining_value)

#會員折扣(旅遊行程)
@register.filter(name='discount')
def discount(value):
    discount = int(value)-math.ceil(int(value)*0.05)
    return discount

#日期星期
@register.filter(name='weekday')
def weekday(value):
    weekday = datetime.strptime(value,"%Y-%m-%d").date()
    return weekday

@register.filter(name='rating5')
def rating5(valu):
    rating = Rating.objects.filter(Q(tour=valu)&Q(value=5)).count()
    return rating

@register.filter(name='rating4')
def rating4(valu):
    rating = Rating.objects.filter(Q(tour=valu)&Q(value=4)).count()
    return rating
@register.filter(name='rating3')
def rating3(valu):
    rating = Rating.objects.filter(Q(tour=valu)&Q(value=3)).count()
    return rating
@register.filter(name='rating2')
def rating2(valu):
    rating = Rating.objects.filter(Q(tour=valu)&Q(value=2)).count()
    return rating
@register.filter(name='rating1')
def rating1(valu):
    rating = Rating.objects.filter(Q(tour=valu)&Q(value=1)).count()
    return rating

@register.filter(name='traintype')
def traintype(value):
    value=value.split(" ")[0]
    if "自強" in value:
        return True
    else:
        return False