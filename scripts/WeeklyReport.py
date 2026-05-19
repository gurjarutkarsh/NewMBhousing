from django.contrib.auth import get_user_model
import datetime as DT


from InventoryTool.models import Visit, NewVisit, DailyPotentialClients

exclude_user_ids = [5, 6, 8, 11, 1, 3, 19, 4, 2, 14, 10, 18]


today = DT.date.today()
#week_ago = today - DT.timedelta(days=7)

start = today - DT.timedelta(days=10)
end = today - DT.timedelta(days=3)

User = get_user_model()
#us = User.objects.filter(is_staff = True)
us = User.objects.all().exclude(id__in=exclude_user_ids)

#vs = Visit.objects.filter(visited_on__gte = week_ago, visited_on__lte = today)

#ds = DailyPotentialClients.objects.filter(date__gte = week_ago, date__lte = today)

vs = NewVisit.objects.filter(visited_on__gte = start, visited_on__lte = end)
ds = DailyPotentialClients.objects.filter(date__gte = start, date__lte = end)
users = {}

for u in us:
    users[u.first_name] = {'daily': 0, 'visit': 0, 'pre_sales_visit': 0}

for v in vs:
    if v.pre_sales.id not in exclude_user_ids:
        users[v.pre_sales.first_name]['visit'] += 1
    if v.pre_sales != v.sales_person and v.sales_person.id not in exclude_user_ids:
        users[v.sales_person.first_name]['pre_sales_visit'] += 1


for d in ds:
    users[d.employee.first_name]['daily'] += 1


print("date =>", start, end)
for u in users:
    #print(u, users[u])
    print (u, " -> daily prospects => " + str(users[u]['daily']) + "\tvisits => " + str(users[u]['visit']) + " \tpre sales clients visits => " + str(users[u]['pre_sales_visit']) )



#sudo sntp -sS time.apple.com

#python manage.py shell < scripts/WeeklyReport.py



