from datetime import date
import datetime
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)
from django import forms
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from django.contrib.auth.models import User


from more_admin_filters import (MultiSelectDropdownFilter, ChoicesDropdownFilter,
                                MultiSelectRelatedFilter, MultiSelectRelatedDropdownFilter,
                                BooleanAnnotationFilter)
from rangefilter.filters import (DateRangeFilterBuilder, DateTimeRangeFilterBuilder,
                                NumericRangeFilterBuilder, DateRangeQuickSelectListFilterBuilder,
                                 )

from .models import Project, Apartment, ApartmentSales, Visit, Negatives, Attendance, DailyPotentialClients, HikeCall, NewVisit

from multiselectfield import MultiSelectField


class ProjectPossessionBuilderListFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("Possession Builder")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "project__possession_builder"

    def lookups(self, request, model_admin):
        return[
            (2024, _("possession by 2024")),
            (2025, _("possession by 2025")),
            (2026, _("possession in 2026")),
            (2027, _("possession in 2027")),
            (2028, _("possession in 2028")),
            (2029, _("possession in 2029")),
            (2030, _("possession in 2030")),
        ]

    def queryset(self, request, queryset):
        possession_year = self.value()
        if possession_year:
            return queryset.filter(
                possession_builder__lte=possession_year,
                possession_builder__gt=0
            )

class ProjectPossessionReraListFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("Possession Rera")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "project__possession_rera"

    def lookups(self, request, model_admin):
        return[
            (2024, _("possession by 2024")),
            (2025, _("possession by 2025")),
            (2026, _("possession in 2026")),
            (2027, _("possession in 2027")),
            (2028, _("possession in 2028")),
            (2029, _("possession in 2029")),
            (2030, _("possession in 2030")),
        ]

    def queryset(self, request, queryset):
        possession_year = self.value()
        if possession_year:
            return queryset.filter(
                possession_rera__lte=possession_year,
                possession_rera__gt=0
            )

"""class BuilderListFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("Builder")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "builder"

    def lookups(self, request, model_admin):
        #queryset = model_admin.get_queryset(request)
        #return queryset.objects.values('builder').distinct()
        return Project.objects.values('id', 'builder').distinct('builder')

    def queryset(self, request, queryset):
        builder = self.value()
        if builder:
            return queryset.filter(
                builder = builder
            )"""

#admin.site.register(Project)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_name", "location", "land_parcel", "possession", "possession_new", "construction", "bonus_points", "link")
    list_filter = (("location", ChoiceDropdownFilter),
                   ("location_group", ChoiceDropdownFilter),
                   ProjectPossessionBuilderListFilter,
                   ProjectPossessionReraListFilter,
                   ("maintained_by", ChoiceDropdownFilter),
                   ("builder", DropdownFilter),
                   #('possesion_date_builder', DateRangeFilter),
                   )
    search_fields = ["name__icontains", "builder__icontains"]
    list_per_page = 10

    def possession(self, obj):
        return str(obj.possession_builder) + " / " +  str(obj.possession_rera) + "(rera)"

    def possession_new(self, obj):
        if obj.possesion_date_builder:
            p_builder = obj.possesion_date_builder.strftime("%B %Y")
        else:
            p_builder = " - "
        if obj.possesion_date_rera:
            p_rera = obj.possesion_date_rera.strftime("%B %Y") + "(rera)"
        else:
            p_rera = " - "
        return  p_builder + " / " + p_rera
        #return str(obj.possession_builder) + " / " +  str(obj.possession_rera) + "(rera)"

    def project_name(self, obj):
        return obj.builder + " - " + obj.name

    def link(self, obj):
        return format_html('<a href="{}">website</a>', obj.project_link)


class BHKListFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("BHK")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "bhk"

    def lookups(self, request, model_admin):
        return[
            (1, _("1 BHK ")),
            (2, _("2, 2.5 BHK")),
            (3, _("3, 3.5 BHK")),
            (4, _("4 BHK"))
        ]

    def queryset(self, request, queryset):
        no_of_bhk = self.value()
        if no_of_bhk:
            return queryset.filter(
                bhk__gte=no_of_bhk,
                bhk__lt=(int(no_of_bhk) + 1)
            )

class LitigationFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("Litigation")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "project__litigation"

    def lookups(self, request, model_admin):
        return[
            ('Yes', _("Yes")),
            ('No', _("No")),
        ]

    def queryset(self, request, queryset):
        litigation = self.value()
        if litigation:
            if litigation == "No":
                return queryset.filter(
                    project__litigation=False
                )
            elif litigation == "Yes":
                return queryset.filter(
                    project__litigation=True
                )



class CostListFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("Cost")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "price"

    def lookups(self, request, model_admin):
        return[
            (60,  _(" less than 60 Lakhs")),
            (65,  _(" less than 65 Lakhs")),
            (70, _(" less than 70 Lakhs")),
            (80, _(" less than 80 Lakhs")),
            (90, _(" less than 90 Lakhs")),
            (100, _(" less than 1 crore")),
            (110, _(" less than 1.1 crore")),
            (120, _(" less than 1.20 crore")),
            (150, _(" less than 1.50 crore")),
            (200, _(" less than 2 crore")),
            (300, _(" less than 3 crore"))
        ]

    def queryset(self, request, queryset):
        price = self.value()
        if price:
            return queryset.filter(
                price__lte=price
            )
class BalconyListFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("Balcony")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "no_of_balcony"

    def lookups(self, request, model_admin):
        return[
            (1, _(" more than 1 balcony")),
            (2, _(" more than 2 balcony")),
            (3, _(" more than 3 balcony")),
            (4, _(" more than 4 balcony"))
        ]

    def queryset(self, request, queryset):
        no_of_balcony = self.value()
        if no_of_balcony:
            return queryset.filter(
                no_of_balcony__gte=no_of_balcony
            )

class PossessionBuilderListFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("Possession Builder")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "project__possession_builder"

    def lookups(self, request, model_admin):
        return[
            (2024, _("possession by 2024")),
            (2025, _("possession by 2025")),
            (2026, _("possession in 2026")),
            (2027, _("possession in 2027")),
            (2028, _("possession in 2028")),
            (2029, _("possession in 2029")),
            (2030, _("possession in 2030")),
        ]

    def queryset(self, request, queryset):
        possession_year = self.value()
        if possession_year:
            return queryset.filter(
                project__possession_builder__lte=possession_year,
                project__possession_builder__gt=0
            )

class PossessionReraListFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("Possession Rera")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "project__possession_rera"

    def lookups(self, request, model_admin):
        return[
            (2024, _("possession by 2024")),
            (2025, _("possession by 2025")),
            (2026, _("possession in 2026")),
            (2027, _("possession in 2027")),
            (2028, _("possession in 2028")),
            (2029, _("possession in 2029")),
            (2030, _("possession in 2030")),
        ]

    def queryset(self, request, queryset):
        possession_year = self.value()
        if possession_year:
            return queryset.filter(
                project__possession_rera__lte=possession_year,
                project__possession_rera__gt=0
            )

class CarpetListFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("Carpet Range")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "carpet"

    def lookups(self, request, model_admin):
        return[
            (1, _("carpet less than 800 sqft")),
            (2, _("carpet more than 800sqft and less than 900 sqft")),
            (3, _("carpet more than 900sqft and less than 1100 sqft")),
            (4, _("carpet more than 1100sqft and less than 1500 sqft")),
            (5, _("carpet more than 1500 sqft")),
        ]

    def queryset(self, request, queryset):
        carpet_value = self.value()
        if carpet_value:
            carpet_value = int(carpet_value)
            if carpet_value == 1:
                return queryset.filter(carpet__lte=800)
            elif carpet_value == 2:
                return queryset.filter(
                    carpet__gte=800,
                    carpet__lte=900
                )
            elif carpet_value == 3:
                return queryset.filter(
                    carpet__gte=900,
                    carpet__lte=1100
                )
            elif carpet_value == 4:
                return queryset.filter(
                    carpet__gte=1100,
                    carpet__lte=1500
                )
            elif carpet_value == 5:
                return queryset.filter(
                    carpet__gte=1500
                )

class LocationListFilter(MultipleChoiceListFilter):
    title = 'project__location'
    parameter_name = 'project__location__in'

    def lookups(self, request, model_admin):
        return Project.LOCATIONS





@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'location', 'details', 'proj_details', 'bonus_pts')
    #readonly_fields = ('bhk',)
    list_filter = (
                   BHKListFilter,
                   CostListFilter,
                   ("price", NumericRangeFilterBuilder()),
                   #('project__location', ChoiceDropdownFilter),
                   ('project__location', MultiSelectDropdownFilter),
                   ('project__location_group', ChoiceDropdownFilter),
                   #LocationListFilter,
                   BalconyListFilter,
                   PossessionBuilderListFilter,
                   PossessionReraListFilter,
                   CarpetListFilter,
                   ("carpet", NumericRangeFilterBuilder()),
                   #("project__litigation", RelatedDropdownFilter),
                   LitigationFilter,
                   ('project', MultiSelectRelatedDropdownFilter),
                   ('project__builder', MultiSelectDropdownFilter),
                   ('jodi_unit_available'),
                   ('east_west_facing_balcony'),
                   )
    #
    search_fields = ["project__name__icontains", "project__builder__icontains", "project__location__icontains"]

    list_per_page = 10
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(inventory_finished=False).order_by('-rating', '-carpet', '-price')


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.order_by('builder')

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    # list_select_related.

    """class DynamicColumn():

        def __init__(self, qs: QuerySet):
            self.qs = qs
            # Analyze the queryset to decide what to show
            self.__name__ = "Dynamic column title"

        def __call__(self, widget: Widget) -> str:
            # Take the model instance and return something to display
            return f"This QS has {len(self.qs)} items

    def get_list_display(self, request):
        qs = self.get_queryset(request)
        dc = DynamicColumn(qs)
        out = list(self.list_display)
        out.append(dc)  # Add multiple different instances if you want
        return out"""

    def project_name(self, obj):
        return obj.project.builder + " - " + obj.project.name

    def location(self, obj):
        location = obj.project.location
        direction = obj.project.direction
        html_str = "<ul>"
        if location:
            html_str += "<li>" + location + "</li>"
        if direction:
            html_str += "<li> direction => " + direction + "</li>"
        html_str += "</ul>"
        #html_str = html_str + "</br>" + '&nbsp;' * 150
        return mark_safe(html_str)

    def location_group(self, obj):
        return obj.project.location_group

    def land_parcel(self, obj):
        return obj.project.land_parcel

    def link(self, obj):
        return format_html('<a href="{}">website</a>', obj.project.project_link)

    #def possession(self, obj):
    #    return str(obj.project.possession_builder) + " / " +  str(obj.project.possession_rera) + "(rera)"

    def possession(self, obj):
        if obj.project.possesion_date_builder:
            p_builder = obj.project.possesion_date_builder.strftime("%B %Y")
        else:
            p_builder = " - "
        if obj.project.possesion_date_rera:
            p_rera = obj.project.possesion_date_rera.strftime("%B %Y") + "(rera)"
        else:
            p_rera = " - "
        return  p_builder + " / " + p_rera

    def cost(self, obj):
        if obj.price > 99:
            return str(obj.price/100) + " crore"
        else:
            return str(obj.price) + " lakhs"

    def constt(self, obj):
        return obj.project.construction

    @admin.display(description="Bonus Points")
    def bonus_pts(self, obj):
        out = obj.project.bonus_points + ", " + obj.bonus_points
        out_list = out.split(", ")
        html_str = "<ul>"
        for pt in out_list:
            html_str += "<li>" + pt + "</li>"
        html_str += "</ul>"
        html_str = html_str + "</br>" + '&nbsp;' * 150
        return mark_safe(html_str)

    @admin.display(description="Details")
    def details(self, obj):
        if obj.price > 99:
            price = str(obj.price/100) + " crore"
        else:
            price = str(obj.price) + " lakhs"


        if obj.project.possesion_date_builder:
            p_builder = obj.project.possesion_date_builder.strftime("%B %Y")
        else:
            p_builder = " - "
        if obj.project.possesion_date_rera:
            p_rera = obj.project.possesion_date_rera.strftime("%B %Y") + "(rera)"
        else:
            p_rera = " - "

        pos =  p_builder + " / " + p_rera

        """html_str = "<ul>"

        html_str += "<li> " + str(obj.carpet) + " Sqft</li>"
        html_str += "<li> " + price + "</li>"
        html_str += "<li> " + pos + "</li>"

        html_str += "</ul>"""
        html_str = "<table>"
        html_str += "<tr><th>BHK</th><td>" + str(obj.bhk) + " BHK"
        if obj.is_duplex:
            html_str += " <b>Duplex</b>"
        html_str += "</td></tr>"
        html_str += "<tr><th>Carpet</th><td>" + str(obj.carpet) + " Sqft</td></tr>"
        html_str += "<tr><th> Price </th><td>" + price + "</td></tr>"
        html_str += "<tr><th> Pos </th><td>" + pos + "</td></tr>"

        html_str += "</table>"

        return mark_safe(html_str)

    @admin.display(description="Proj Details")
    def proj_details(self, obj):
        no_of_towers_val = obj.project.towers
        construction = obj.project.construction
        land_parcel = obj.project.land_parcel
        no_of_towers = obj.project.towers
        per_floor_flats = obj.project.per_floor_flats
        no_of_lifts = obj.project.no_of_lifts
        no_of_floors = obj.project.no_of_floors
        amenities = obj.project.amenities
        location_link = obj.project.location_link
        no_of_balcony = obj.no_of_balcony
        balcony_facing = obj.balcony_facing

        html_str = "<ul>"

        if land_parcel:
            html_str += "<li> Land Parcel -> " + str(land_parcel) + " Acres</li>"
        if no_of_towers != 0:
            html_str += "<li> No Of Towers -> " + str(obj.project.towers) + "</li>"
        if construction:
            html_str += "<li> Construction -> " + construction + "</li>"
        if per_floor_flats != 0:
            html_str += "<li> Per Floor Flats -> " + str(per_floor_flats) + "</li>"
        if no_of_lifts != 0:
            html_str += "<li> No Of Lifts -> " + str(no_of_lifts) + "</li>"
        if no_of_floors != -1:
            html_str += "<li> No of Floors -> " + str(no_of_floors) + "</li>"
        if amenities:
            html_str += "<li> Amenities -> " + amenities + " </li>"
        if no_of_balcony:
            html_str += "<li> No Of Balcony -> " + str(no_of_balcony) + " </li>"

        #add check of -1

        if balcony_facing:
            html_str += "<li> Balcony Facing -> " + obj.balcony_facing + "</li>"
        if location_link:
            html_str += '<li> Location -> <a href=' + location_link + '>click here</a> </li>'

        html_str += "</ul>" + "</br>" + '&nbsp;' * 50


        """constt = "<li>Construction - " + obj.project.construction if obj.project.construction else " - " + "</li>"
        land_parcel = "<li> Land Parcel - " + str(obj.project.land_parcel) + " Acres" + "</li>"
        no_of_towers = "<li> No Of Towers - " + str(obj.project.towers) + "</li>"
        per_floor_flats = "<li> Per Floor Flats - " + str(obj.project.per_floor_flats) + "</li>"
        no_of_lifts = "<li> No Of Lifts - " + str(obj.project.no_of_lifts) + "</li>"
        no_of_floors = "<li> No of Floors - " + str(obj.project.no_of_floors) + "/li>"
        amenities = "<li> Amenities - " + obj.project.amenities + " </li>"
        no_of_balcony = "<li> No Of Balcony - " + obj.no_of_balcony + " </li>"
        balcony_facing = "<li> Balcony Facing - " + obj.balcony_facing + "</li>"""""


        #html_str = "<ul>" + land_parcel + constt + no_of_towers + "</ul>" + "</br>" + '&nbsp;' * 50
        return mark_safe(html_str)




    def is_township(self, obj):
        return obj.project.is_township



class VisitListFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("No Of Sites Visited")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "no_of_sites_visited"

    def lookups(self, request, model_admin):
        return[
            (1, _("no of visits 1")),
            (2, _("no of visits 2")),
            (3, _("no of visits 3")),
            (4, _("no of visits 4")),
            (5, _("no of visits 5")),
            (6, _("no of visits more than 5")),
        ]

    def queryset(self, request, queryset):
        no_of_visits = self.value()
        if no_of_visits:
            no_of_visits = int(no_of_visits)
            if no_of_visits > 5:
                return queryset.filter(no_of_sites_visited__gte=no_of_visits)
            else:
                return queryset.filter(no_of_sites_visited=no_of_visits)

# in admin.py we have DeviceAdmin with custom form
class VisitAdminForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all().order_by('builder'))
    Apartment = forms.ModelChoiceField(queryset=Apartment.objects.filter(inventory_finished=False).order_by('project__builder'), label='apartment')
    pre_sales = forms.ModelChoiceField(queryset=User.objects.all(), label='pre_sales')
    sales_person = forms.ModelChoiceField(queryset=User.objects.all(), label='pre_sales')
    builder_sales_person = forms.CharField()
    builder_sales_person_phone = forms.CharField()
    buyer_phone = forms.CharField()
    buyer_name = forms.CharField()
    buyer_budget = forms.DecimalField()
    visited_on = forms.DateField()
    no_of_sites_visited = forms.IntegerField()
    conversation_description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Apartment
        exclude = ['created_on', 'updated_on']



"""@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    form = VisitAdminForm"""



@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.order_by('builder')

        if db_field.name == "apartment":
            kwargs["queryset"] = Apartment.objects.order_by('project__builder')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ("apartment", "pre_sales", "sales_person", "buyer_phone", "buyer_name", "visited_on", "budget", "no_of_sites_visited", "conversation_description")
    list_filter = (('apartment', RelatedDropdownFilter),
                   ('project', RelatedDropdownFilter),
                   ('pre_sales', RelatedDropdownFilter),
                   ('sales_person', RelatedDropdownFilter),
                   ("visited_on", DateRangeFilterBuilder(title="Filter by Dates", )),
                   VisitListFilter,
                   ('no_of_sites_visited', MultiSelectDropdownFilter),
                   )

    search_fields = ("buyer_phone__icontains", "buyer_name__icontains", "conversation_description__icontains")
    #list_select_related = True
    #autocomplete_fields = ["apartment"]

    def budget(self, obj):
        if obj.buyer_budget > 99:
            return str(obj.buyer_budget/100) + " crore"
        else:
            return str(obj.buyer_budget) + " lakhs"


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
            return qs
        return qs.filter(pre_sales=request.user) | qs.filter(sales_person=request.user)

    def description(self, obj):
        return obj.conversation_description
    #exclude = ["project"]
    #add filter to get visit of employee in date range


admin.site.register(ApartmentSales)
#admin.site.register(Visit)
@admin.register(Negatives)
class NegativesAdmin(admin.ModelAdmin):
    list_display = ('project', 'apartment', 'negative_points')
    #readonly_fields = ('bhk',)
    list_filter = (('project', RelatedDropdownFilter),
                   ('apartment', RelatedDropdownFilter),
                   )

    search_fields = ["project__name__icontains", "project__builder__icontains", "project__location__icontains"]




    @admin.display(description="negative Points")
    def negative_points(self, obj):
        out_list = obj.negatives.split(", ")
        html_str = "<ul>"
        for pt in out_list:
            html_str += "<li>" + pt + "</li>"
        html_str += "</ul>"
        html_str = html_str + "</br>" + '&nbsp;' * 150
        return mark_safe(html_str)



@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'check_in_time', 'check_out_time')

    list_filter = (('employee_name', RelatedDropdownFilter),)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
            return qs
        return qs.filter(employee_name=request.user)


class RatingFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    title = _("By Ratings")
    # Parameter for the filter that will be used in the URL query.
    parameter_name = "project__possession_rera"

    def lookups(self, request, model_admin):
        return[
            (5, _("rating above 5")),
            (6, _("rating above 6")),
            (7, _("rating above 7")),
            (8, _("rating above 8")),
            (9, _("rating above 9")),
            (10, _("rating above 10")),
        ]

    def queryset(self, request, queryset):
        rating = self.value()
        if rating:
            return queryset.filter(
                client_rating__gte=rating
            )



# in admin.py we have DeviceAdmin with custom form
class DailyPotentialClientsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DailyPotentialClientsForm, self).__init__(*args, **kwargs)
        """if self.instance.pk:
            categories = self.instance.category.all()
        else:
            categories = None

        if categories:
            self.fields['topic'].queryset = self.fields['topic'].queryset.filter(category__in=categories)
        else:
            del self.fields['topic']"""
    client_name = forms.CharField()
    client_phone = forms.CharField()
    bhk = forms.DecimalField(decimal_places=1, max_digits=2,
                             widget=forms.Select(
                                 choices=Apartment.BHK_OPTIONS,
                             ))
    client_budget = forms.IntegerField(help_text="client budget in lakhs. 1 crore = 100 lakh")
    date = forms.DateField(initial=datetime.date.today)
    any_other_details = forms.CharField(widget=forms.Textarea)
    #other_property_visited = forms.CharField(widget=forms.Textarea)

    def save(self, commit=True):

        """employee = self.current_user
        title = self.cleaned_data.get('title', 'N/A')
        do_a = self.cleaned_data.get('do_a', True)
        do_b = self.cleaned_data.get('do_b', True)
        do_c = self.cleaned_data.get('do_c', True)

        # Assume these two work fine
        page_links = work_out_links(do_a, do_b, do_c)
        start_page = get_start_page(do_a, do_b, do_c)

        self.cleaned_data['page_links'] = page_links
        self.cleaned_data['start_page'] = start_page"""
        return super(DailyPotentialClientsForm, self).save(commit=commit)



#DailyFollowUp
@admin.register(DailyPotentialClients)
class DailyPotentialClientsAdmin(admin.ModelAdmin):
    #form = DailyPotentialClientsForm

    list_display = ('employee', 'bhk', 'client_details', 'client_budget_location', 'date', 'details', 'other_property_visited')

    list_filter = (('employee', RelatedDropdownFilter),
                   ('bhk', ChoiceDropdownFilter),
                   ("date", DateRangeFilterBuilder( title="Filter by Dates", )),
                   ("rating", ChoiceDropdownFilter),
                   ("client_budget", NumericRangeFilterBuilder()),
                   #RatingFilter
                   #("bhk", NumericRangeFilterBuilder()),
                   #("created_on", DateRangeQuickSelectListFilterBuilder()),
                   )
    #add date filter, bhk filter
    exclude = ['client_rating']

    search_fields = ("client_phone__icontains", "client_name__icontains", "location__icontains", "details__icontains")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
            return qs
        return qs.filter(employee=request.user)

    def client_details(self, obj):
        #return obj.client_name
        html_str = "<ul>"
        html_str += "<li>" + obj.client_name + "</li>"
        html_str += "<li>" + str(obj.client_phone) + "</li>"
        html_str += "<li> status -> " + obj.rating + "</li>"
        #html_str += "<li> rating -> " + str(obj.client_rating) + "</li>"
        html_str += "</ul>"
        return mark_safe(html_str)

    @admin.display(description="Budget / Location")
    def client_budget_location(self, obj):
        html_str = "<ul>"
        if obj.client_budget:
            if obj.client_budget < 100:
                html_str += "<li>" + str(obj.client_budget) + " Lakhs</li>"
            else:
                html_str += "<li>" + str(obj.client_budget/100) + " Cr" + "</li>"
        if obj.location:
            html_str += "<li>" + str(obj.location) + "</li>"
        html_str += "</ul>"
        return mark_safe(html_str)

    @admin.display(description="Details")
    def details(self, obj):
        out = obj.any_other_details
        if out:
            out_list = out.split(", ")
            html_str = "<ul>"
            for pt in out_list:
                html_str += "<li>" + pt + "</li>"
            html_str += "</ul>"
            html_str = html_str + "</br>" + '&nbsp;' * 15
            return mark_safe(html_str)

    def get_form(self, request, *args, **kwargs):
        form = super(DailyPotentialClientsAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form

    """def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.employee = request.user
        else:
            obj.employee = request.user
            #unnecessary if add change functionality for change by admin later
        super().save_model(request, obj, form, change)"""

    """def get_readonly_fields(self, request, obj):
        fields = super().get_readonly_fields(request)
        if not request.user.is_superuser:
            fields.append('employee')
        if not request.user.is_superuser:
            obj.employee = request.user
            self.readonly_fields = ['employee']
        return self.readonly_fields"""




    """
    #changelist-filter{
    position: absolute;
    left: 85%;
    }
    """


@admin.register(HikeCall)
class HikeCallAdmin(admin.ModelAdmin):
    """
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "employee_hike_call")
    hike_call_assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "employee_hike_call_assigned_to")
    client_phone = models.CharField(max_length=200)
    client_details = models.TextField(max_length=2000, null=True, blank=True)
    hike_call_expectation = models.TextField(max_length=2000, null=True, blank=True)
    hike_call_followup = models.TextField(max_length=2000, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    """
    list_display = (
    'employee', 'caller', 'call_details', 'expectation', 'hike_call_followup', 'created_on')

    list_filter = (('employee', RelatedDropdownFilter),
                   ('hike_call_assigned_to', RelatedDropdownFilter),
                   ("created_on", DateRangeFilterBuilder(title="Filter by Dates", )),
                   # ("bhk", NumericRangeFilterBuilder()),
                   # ("created_on", DateRangeQuickSelectListFilterBuilder()),
                   )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
            return qs
        return qs.filter(employee=request.user) | qs.filter(hike_call_assigned_to=request.user)

    def expectation(self, obj):
        return obj.hike_call_expectation

    def caller(self, obj):
        return obj.hike_call_assigned_to

    def call_details(self, obj):
        html_str = "<ul>"
        if obj.client_phone:
            html_str += "<li>" + str(obj.client_phone) + "</li>"
        if obj.client_details:
            html_str += "<li>" + str(obj.client_details) + "</li>"
        html_str += "</ul>"
        return mark_safe(html_str)



@admin.register(NewVisit)
class NewVisitAdmin(admin.ModelAdmin):
    list_display = ("pre_sales", "sales", "buyer", "visited_on", "budget",
                    "visited", "no_of_sites_visited", "conversation_description")

    #add projects like description
    list_filter = (('project_visited', RelatedDropdownFilter),
                   ('pre_sales', RelatedDropdownFilter),
                   ('sales_person', RelatedDropdownFilter),
                   ("visited_on", DateRangeFilterBuilder(title="Filter by Dates", )),
                   ('rating', ChoiceDropdownFilter),
                   VisitListFilter,
                   ('no_of_sites_visited', MultiSelectDropdownFilter),
                   )

    search_fields = ("buyer_phone__icontains", "buyer_name__icontains", "conversation_description__icontains")

    exclude = ['added_by']

    def budget(self, obj):
        if obj.buyer_budget > 99:
            return str(obj.buyer_budget / 100) + " crore"
        else:
            return str(obj.buyer_budget) + " lakhs"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
            return qs
        return qs.filter(pre_sales=request.user) | qs.filter(sales_person=request.user)

    def description(self, obj):
        return obj.conversation_description

    def visited(self, obj):
        if obj.project_visited:
            html_str = "<ul>"
            for p in obj.project_visited.all():
                html_str += "<li>" + str(p) + "</li>"
            html_str += "</ul>"
            html_str = html_str + "</br>" + '&nbsp;' * 50
            return mark_safe(html_str)

    def sales(self, obj):
        return obj.sales_person

    def buyer(self, obj):
        html_str = "<ul>"
        if obj.buyer_name:
            html_str += "<li>" + obj.buyer_name+ "</li>"

        if obj.buyer_phone:
            html_str += "<li>" + obj.buyer_phone+ "</li>"

        html_str += "</ul>"
        html_str = html_str + "</br>" + '&nbsp;' * 20
        return mark_safe(html_str)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project_visited":
            kwargs["queryset"] = Apartment.objects.order_by('project__builder')

        """if db_field.name == "apartment":
            kwargs["queryset"] = Apartment.objects.order_by('project__builder')"""
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['project_visited'].queryset = form.base_fields['project_visited'].queryset.order_by('project__builder', 'project__name')
        return form

    def save_model(self, request, obj, form, change):
        print("I was here")
        obj.added_by = request.user
        #obj.save()
        super().save_model(request, obj, form, change)