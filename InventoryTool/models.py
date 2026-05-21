import datetime


from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import GroupedForeignKey


from multiselectfield import MultiSelectField

from InventoryTool.CONSTANTS import CLIENT_RATING

# Create your models here.
class Project(models.Model):

    LOCATIONS = [
        ('Hinjewadi1', 'Hinjewadi Phase 1'),
        ('Hinjewadi2', 'Hinjewadi Phase 2'),
        ('Hinjewadi3', 'Hinjewadi Phase 3'),
        ('Wakad', 'Wakad'),
        ('Tathawade', 'Tathawade'),
        ('Punawale', 'Punawale'),
        ('Hinjewadi / Marunji', 'Hinjewadi / Marunji'),
        ('Balewadi', 'Balewadi'),
        ('Baner', 'Baner'),
        ('Mahalunge', 'Mahalunge'),
        ('Ravet', 'Ravet'),
    ]
    LOCATION_GROUPS = [
        ('Hinjewadi', 'Hinjewadi Phase 1,2,3, Marunji'),
        ('Punawale', 'Punawale, Tathawade'),
        ('Wakad', 'Wakad'),
        ('Ravet', 'Ravet'),
        #('Marunji', 'Marunji'),
        ('Baner', 'Baner, Balewadi'),
        ('Mahalunge', 'Mahalunge')
        #add Mahalunge, move marunji in hinjewadi
    ]

    MAINTAINED_BY = [
        ('PCMC', 'PCMC'),
        ('PMC', 'PMC'),
        ('PMRDA', 'PMRDA'),
        ('MIDC', 'MIDC'),
        ('Township', 'Township'),
        ('Other', 'Other')
    ]

    CONSTRUCTION = [
        ('Mivan', 'Mivan'),
        ('Bricks', 'Bricks'),
        ('Hybrid', 'Internal Bricks Outer Mivan'),
        ('RCC', 'RCC Blocks')
    ]

    POSSESSION_YEARS = [
        (2024, 2024),
        (2025, 2025),
        (2025, 2025),
        (2026, 2026),
        (2027, 2027),
        (2028, 2028),
        (2029, 2029),
        (2030, 2030),
        (2031, 2031),
    ]



    name = models.CharField(max_length=200, help_text='Name of project')
    builder = models.CharField(max_length=200, help_text='Name of Builder')
    about_builder = models.TextField(max_length=2000, blank=True, help_text='About Builder Legacy, previous apartment delivered, etc')

    #add section to add about builder details


    land_parcel = models.DecimalField(default=0, null=True, decimal_places=2, max_digits=6, help_text='Land parcel in acres')
    towers = models.IntegerField(default=0, null=True, help_text='Number of towers')
    amenities = models.CharField(max_length=1000, null=True, blank=True, help_text='comma separated list of amenities')# make it better
    location = models.CharField(max_length=200, choices=LOCATIONS)

    # add direction to project

    location_group = models.CharField(max_length=200, choices=LOCATION_GROUPS)
    direction = models.TextField(blank=True, help_text="customer puchta h project kaha h ?")
    location_link = models.CharField(max_length=300, null=True, blank=True)
    per_floor_flats = models.IntegerField(default=0, null=True, help_text='number of flats per floor')
    no_of_lifts = models.IntegerField(default=0, null=True, help_text='number of lifts including service')
    no_of_units = models.IntegerField(default=-1, null=True, help_text='number of units')
    no_of_floors = models.IntegerField(default=-1, null=True, help_text='number of floors')
    possesion_date_builder = models.DateField(null=True, blank=True, help_text='Date of possession by builder, Add Date as 1 Eg 1 Dec')
    possesion_date_rera = models.DateField(null=True, blank=True, help_text='Date of possession as per rera, Add Date as 1 Eg 1 Dec')
    possesion_date_misc = models.TextField(blank=True, help_text='Date of possession misc notes')

    #add no of units in projects

    #add no of storey in project

    #multiple possession, month of possession

    possession_builder = models.IntegerField(default=0, null=True, choices = POSSESSION_YEARS, help_text='Year of Possession as per builder', )#with month
    possession_rera = models.IntegerField(default=0, null=True, choices = POSSESSION_YEARS, help_text='Year of Possession as per rera')
    construction = models.CharField(max_length=200, choices=CONSTRUCTION, help_text='contruction type- Mivan, bricks, hybrid')
    litigation = models.BooleanField(default=False, help_text='check the box if the project has litigation')
    project_link = models.CharField(max_length=200, null=True, blank=True, help_text='official website of project')
    project_mb_link = models.CharField(max_length=200, null=True, blank=True, help_text='mbhousing google drive link of project')
    nearby = models.CharField(max_length=1000, blank=True, help_text='nearby places/landmark')

    #make bonus point text field
    bonus_points = models.TextField(max_length=1000, blank=True, help_text='Eg 200m from metro, 3 minute drive from expressway')
    open_space = models.IntegerField(default=0, null=True, help_text='percentage of open sapce')#open space in percent
    is_township = models.BooleanField(default=False, help_text='check the box if project in township')
    is_mhada_inside = models.BooleanField(default=False, help_text='check the box if mhada is inside project')
    maintained_by = models.CharField(max_length=200, choices=MAINTAINED_BY, help_text='maintained by PCMC, PMRDA, etc')
    Hospitals_Nearby = models.CharField(max_length=500, null=True, blank=True, help_text='Hospitals nearby, comma separated')
    Commercial_Nearby = models.CharField(max_length=500, null=True, blank=True, help_text='Commercial nearby, comma separated')
    Schools_Nearby = models.CharField(max_length=500, null=True, blank=True, help_text='Schools nearby, comma separated')
    Colleges_Nearby = models.CharField(max_length=500, null=True, blank=True, help_text='Colleges nearby, comma separated')
    Nearest_Metro = models.CharField(max_length=500, null=True, blank=True, help_text='Nearest Metro, comma separated')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    """def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        
    class Meta:
        unique_together = ("name", "year", )    
    """
    # Porject closed/no inventory left
    # construction mivan/ bricks
    # jodi_unit available

    def __str__(self):
        return f"{self.builder} - {self.name}"


class Apartment(models.Model):
    BALCONY_FACING = [
        ('East', 'East'),
        ('West', 'West'),
        ('North', 'North'),
        ('South', 'South'),
    ]

    MASTER_WITH_BALCONY = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('May', 'May'),
        ('NA', 'NA')
    ]

    BHK_OPTIONS = [(1.0,1.0), (2.0,2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0,4.0), (4.5, 4.5), (5.0, 5.0)]


    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    #make it choice field comfort/premium/luxury/royal/
    Variant = models.CharField(max_length=200, null=True, blank=True, help_text='Variant of Apartment Eg comfort/luxury/premium/Royal')



    bhk = models.DecimalField(default=0, decimal_places=1, max_digits=2, choices = BHK_OPTIONS)
    carpet = models.IntegerField(default=0, help_text='carpet area in square feet')
    carpet_variants = models.CharField(blank=True, max_length=100, help_text='carpet variants comma separated Eg- 720, 722, 754')
    rating = models.IntegerField(default=5, help_text='rating to show good rated apartments first')

    #multiple carpet handling


    # add option with price( onwards, around, maximum ), another more comments about price

    price = models.IntegerField(default=0, null=True, help_text='price of apartment in lakhs')
    negotiable = models.BooleanField(default=True, null=True)
    negotiable_upto = models.IntegerField(default=0, null=True, help_text='negotiable upto in lakhs')
    last_sold_price = models.IntegerField(default=0, null=True, help_text='last sold price in lakhs')
    Tower = models.CharField(max_length=200, null=True, blank=True, help_text='Tower name or number')
    no_of_balcony = models.IntegerField(default=0, null=True, help_text='number of balcony; excluding dry balcony')
    dry_balcony_open = models.BooleanField(default=False)
    vastu_compliant = models.BooleanField(default=True)
    east_west_facing_balcony = models.BooleanField(default=False)

    balcony_facing = models.CharField(max_length=100, null=True, blank=True, help_text='balcony facing East, West. North, South')
    bonus_points = models.TextField(max_length=1000, null=True, blank=True, help_text="Eg walking wardrobe, etc")#walking wardrobe
    dimensions_room = models.TextField(max_length=1000, null=True, blank=True, help_text='living - 20 * 14, comma separated')
    balcony_size = models.CharField(max_length=200, null=True, blank=True, help_text='11 * 5')
    master_bedroom_size = models.CharField(max_length=200, null=True, blank=True, help_text='15 * 12')
    master_bedroom_with_balcony = models.CharField(choices=MASTER_WITH_BALCONY, default='NA', help_text='master bedroom with balcony')
    is_duplex = models.BooleanField(default=False, help_text='check the box if apartment is duplex')
    jodi_unit_available = models.BooleanField(default=False, help_text='check the box if apartment has jodi unit option')
    no_of_inventory_available = models.IntegerField(default=-1, null=True, help_text='number of inventory available')
    inventory_enquiry_date = models.DateTimeField(auto_now=True, null=True, blank=True, help_text='date of inventory enquiry')
    inventory_finished = models.BooleanField(default=False, help_text='check the box if apartment has no inventory left')
    inventory_availability_comments = models.TextField(max_length=2000, null=True, blank=True, help_text='inventory availability comments')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    #master bedroom with balcony

    def __str__(self):
        return f"{self.project} - {self.bhk} bhk - {self.carpet}"

    """class Meta:
        ordering = ['project__builder']"""


class Visit(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE) #on delete
    #apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="a")
    apartment = GroupedForeignKey(Apartment, "project", related_name="an")
    #pre_sales_name = models.CharField(max_length=200, null=True, blank=True)
    #sales_person_name = models.CharField(max_length=200)
    pre_sales = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "pre_sales_person", null=True)
    sales_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "sales_person", default=4)#address default value
    builder_sales_person = models.CharField(max_length=200, help_text='builder_sales_person')
    builder_sales_person_phone = models.CharField(max_length=200, help_text='builder_sales_person_phone')
    buyer_phone = models.CharField(max_length=200)
    buyer_name = models.CharField(max_length=200)
    buyer_budget = models.DecimalField(default=0, decimal_places=2, max_digits=6, null=True, help_text="add amount in lakhs")
    visited_on = models.DateField(default=datetime.date.today)
    no_of_sites_visited = models.IntegerField(default=0)
    conversation_description = models.TextField(blank=True, help_text = "A brief description about the conversation you had with the customers")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.apartment} - {self.pre_sales if self.pre_sales else ''} - {self.sales_person}"


class ApartmentSales(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    pre_sales_name = models.CharField(max_length=200, null=True, blank=True)
    sales_person_name = models.CharField(max_length=200)
    buyer_phone = models.CharField(max_length=200)
    buyer_name = models.CharField(max_length=200)
    token_on = models.DateTimeField()
    agreement_on = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Apartment Sales"
        verbose_name_plural = "Apartment Sales"

    def __str__(self):
        return f"{self.apartment} - {self.pre_sales_name} - {self.sales_person_name}"




class Negatives(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null = True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null = True)
    negatives = models.TextField(max_length=2000, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Negative"
        verbose_name_plural = "Negatives"



class Attendance(models.Model):

    employee_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "employee", null=True)
    check_in_time = models.DateTimeField( null=True, blank=True)
    check_out_time = models.DateTimeField( null=True, blank=True)
    comments = models.TextField(blank=True, max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)



class DailyPotentialClients(models.Model):

    RATINGS = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "employee_daily_followup", null=True)
    bhk = models.DecimalField(max_length=200, null=True, decimal_places=1, max_digits=2, choices = [(1.0,1.0), (2.0,2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0,4.0), (4.5, 4.5), (5.0, 5.0)])
    client_phone = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200)
    client_budget = models.IntegerField(null=True, blank=True, help_text="client budget in lakhs. 1 crore = 100 lakh")
    client_rating = models.IntegerField(choices = RATINGS, help_text="client budget in lakhs. 1 crore = 100 lakh", null=True)
    rating = models.CharField(max_length=200, choices=CLIENT_RATING, null=True)
    location = MultiSelectField(choices = Project.LOCATIONS, max_length=200, null=True, blank=True)
    client_job_location = models.CharField(max_length=200, null=True, blank=True)
    other_property_visited = models.CharField(max_length=200, null=True, blank=True, help_text = "properties visited with other cp")
    details = models.TextField(max_length=2000, null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.bhk} bhk - {self.client_name} - {self.client_phone}"

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.client_phone:
            self.client_phone = self.client_phone.replace(" ", "").replace("+91", "")

        return super(DailyPotentialClients, self).save(*args, **kwargs)


class HikeCall(models.Model):

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "employee_hike_call")
    hike_call_assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "employee_hike_call_assigned_to")
    client_phone = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200, null=True)
    client_details = models.TextField(max_length=2000, null=True, blank=True)
    hike_call_expectation = models.TextField(max_length=2000, null=True, blank=True)
    hike_call_followup = models.TextField(max_length=2000, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']


# Add projects shared with client

class NewVisit(models.Model):


    pre_sales = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pre_sales_person_new_visit", null=True)
    sales_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales_person_new_visit",
                                     default=4)  # address default value

    buyer_phone = models.CharField(max_length=200)
    buyer_name = models.CharField(max_length=200)
    project_visited = models.ManyToManyField(Apartment, help_text='select all the projects')
    builder_sales_person = models.CharField(max_length=200, help_text='builder_sales_person_new_visit')
    builder_sales_person_phone = models.CharField(max_length=200, help_text='builder_sales_person_phone_new_visit')
    buyer_budget = models.IntegerField(default=0, null=True,
                                       help_text="add amount in lakhs. if budget = `1.2 cr` add `120`")
    visited_on = models.DateField(default=datetime.date.today)
    no_of_sites_visited = models.IntegerField(default=0)
    conversation_description = models.TextField(blank=True,
                                                help_text="A brief description about the conversation you had with the customers")
    visit_is_revisit = models.BooleanField(default=False, help_text='check the box if the visit is revisit')
    rating = models.CharField(max_length=200, choices=CLIENT_RATING)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_by_new_visit", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.full_clean()

        if self.buyer_phone:
            self.buyer_phone = self.buyer_phone.replace(" ", "").replace("+91", "")

        return super(NewVisit, self).save(*args, **kwargs)



class DelayedFollowUp(models.Model):
    buyer_phone = models.CharField(max_length=200)
    buyer_name = models.CharField(max_length=200)
    follow_up_date = models.DateField(default=datetime.date.today)
    details = models.TextField(blank=True,
                                   help_text="any other details")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)










