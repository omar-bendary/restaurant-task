from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)])

    def __str__(self):
        return f"Table {self.number}"


class Reservation(models.Model):
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='reservations')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Reservation for Table {self.table.number} at {self.start_time}"
