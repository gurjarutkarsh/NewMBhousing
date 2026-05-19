"""from InventoryTool.models import Visit, NewVisit

vs = Visit.objects.all()

for v in vs:
    n = NewVisit(
        pre_sales = v.pre_sales,
        sales_person = v.sales_person,
        buyer_phone = v.buyer_phone,
        buyer_name = v.buyer_name,
        builder_sales_person = v.builder_sales_person,
        builder_sales_person_phone = v.builder_sales_person_phone,
        buyer_budget = v.buyer_budget,
        visited_on = v.visited_on,
        no_of_sites_visited = v.no_of_sites_visited,
        conversation_description = v.conversation_description,
        created_on = v.created_on,
        updated_on = v.updated_on,
        rating = "exploring")
    n.save()

    n.project_visited.set([v.apartment])
    n.save()"""
print('Hi')


    # python manage.py shell < scripts/Migrate_visit_to_newvisit.py