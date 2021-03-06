from django.db import models
# from django.contrib.auth.models import User
#
# class Post(models.Model):
#     post = models.CharField(max_length=500)
#     user = models.ForeignKey(User)


# import webapp.models
#
# ticket = Ticket()
# ticket.firstname = "john"
# ticket.date = ""
# ticket.Save()
#
# ticket = Ticket.filter(name="john")

class Seat(models.Model):
    number = models.IntegerField()#Number of the seat

    def get_row(self):
        rows = self.row_set.all()

        if len(rows) >= 1:
            return list(rows)
        else:
            return

    get_row.short_description = 'Row'

    def __str__(self):
        return str(self.number)

    #row = models.ForeignKey(Row, on_delete=models.CASCADE, null=True) #One-to-one reference to the row that contains this Seat

class Row(models.Model):
    name = models.CharField(max_length=10)#Number or name of the row.
    seats = models.ManyToManyField(Seat)

    def get_section(self):
        section = self.section_set.all()

        if len(section) >= 1:
            return list(section)
        else:
            return

    get_section.short_description = 'Section'

    def get_seats(self):
        seats = self.seats.all()
        if len(seats) >= 1:
            return len(seats)
        else:
            return

    get_seats.short_description = 'Seats'

    def __str__(self):
        return self.name

class PriceGroup(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=6)

    def get_sections(self):
        sections = self.section_set.all()

        if len(sections) >= 1:
            return list(sections)
        else:
            return

    get_sections.short_description = 'Sections'

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=50)
    rows = models.ManyToManyField(Row)
    pricegroups = models.ManyToManyField(PriceGroup)

    def get_rows(self):
        rows = self.rows.all()
        if len(rows) >= 1:
            return list(rows)
        else:
            return

    get_rows.short_description = 'Rows'

    def get_pricegroups(self):
        prices = self.pricegroups.all()
        if len(prices) >= 1:
            return list(prices)
        else:
            return

    get_pricegroups.short_description = 'Price Groups'

    def __str__(self):
        return self.name

    def getName(self):
        return self.name


#The site that a Performance is held in. Contains the seating information, name, and location.
class Theater(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)#Location of the theater
    sections = models.ManyToManyField(Section)

    def get_sections(self):
        sections = self.sections.all()
        if len(sections) >= 1:
            return list(sections)
        else:
            return

    get_sections.short_description = 'Sections'

    def __str__(self):
        return self.name


class Performance(models.Model):
    time = models.DateTimeField()#Date and time of the performance.
    theater = models.ManyToManyField(Theater)

    def get_theater(self):
        theater = self.theater.all()
        if len(theater) >= 1:
            return list(theater)
        else:
            return

    get_theater.short_description = 'Theater'

    def get_show(self):
        show = self.show_set.all()

        if len(show) >= 1:
            return list(show)
        else:
            return

    get_show.short_description = 'Show'

    def __str__(self):

        return str(self.time)[:16] #Only get first 16 characters to cut off minutes and past



class Show(models.Model):
    name = models.CharField(max_length=50)
    performances = models.ManyToManyField(Performance)

    def get_performances(self):
        performances = self.performances.all()
        if len(performances) >= 1:
            return list(performances)
        else:
            return

    get_performances.short_description = 'Performances'

    def get_season(self):
        season = self.season_set.all()

        if len(season) >= 1:
            return list(season)
        else:
            return

    get_season.short_description = 'Season'

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=50)
    shows = models.ManyToManyField(Show)
    #Insert a one-to-many referance to a list of Shows.

    def get_shows(self):
        shows = self.shows.all()
        if len(shows) >= 1:
            return list(shows)
        else:
            return

    get_shows.short_description = 'Shows'

    def __str__(self):
        return self.name


class Customer(models.Model):
    firstName = models.CharField(max_length=30)
    middleName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    address = models.CharField(max_length=400)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return str(self.firstName) + " " + str(self.middleName) + " " + str(self.lastName)

    def get_tickets(self):
        tickets = self.ticket_set.all()

        if len(tickets) >= 1:
            return list(tickets)
        else:
            return

    get_tickets.short_description = 'Tickets'


class Ticket(models.Model):
    customer = models.ManyToManyField(Customer)
    seat = models.ManyToManyField(Seat)
    season = models.ManyToManyField(Season)
    show = models.ManyToManyField(Show)#Name of the show that this ticket is valid for
    performance = models.ManyToManyField(Performance)#The individual performance.
    paid = models.BooleanField(default=False)#Whether or not the ticket has been paid. Keeps track of advance tickets.
    datePurchased = models.DateTimeField("Date Purchased")#When the ticket was purchased.
    door = models.BooleanField()#Whether or not the ticket was purchased at the door
    printed = models.BooleanField(default=False)#Whether or not the ticket has been printed.

    def __str__(self):
        #return self.customer.firstName + ' ' + self.customer.lastName + ', '+ self.show.name + ', ' + self.performance.time
        return '(' + str(self.performance.all()[0].time)+ ', ' + str(self.show.all()[0].name) + ', ' + str(self.season.all()[0].name) + ', '\
               + str(self.customer.all()[0].firstName) + ' ' + str(self.customer.all()[0].lastName) + ')'


    def get_customer_name(self):
        customer = self.customer.all()

        if len(customer) >= 1:
            return list(customer)
        else:
            return

    get_customer_name.short_description = 'Customer Name'


    def get_seat(self):
        seats = self.seat.all()

        if len(seats) >= 1:
            return list(seats)
        else:
            return

    get_seat.short_description = 'Seat'


    def get_season(self):
        season = self.season.all()

        if len(season) >= 1:
            return list(season)
        else:
            return

    get_season.short_description = 'Season'


    def get_show(self):
        show = self.show.all()

        if len(show) >= 1:
            return list(show)
        else:
            return

    get_show.short_description = 'Show'

    def get_performance(self):
        performance = self.performance.all()

        if len(performance) >= 1:
            return list(performance)
        else:
            return

    get_performance.short_description = 'Performance'
