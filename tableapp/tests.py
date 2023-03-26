import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone
from mixer.backend.django import mixer
from .models import Table, Reservation


@pytest.mark.django_db
class TestTable:
    def test_create_table(self):
        table = mixer.blend(Table, number=1, seats=4)
        assert str(table) == "Table 1"
        assert table.number == 1
        assert table.seats == 4

    def test_create_duplicate_table(self):
        mixer.blend(Table, number=1, seats=4)
        with pytest.raises(IntegrityError):
            mixer.blend(Table, number=1, seats=6)

    def test_create_table_with_zero_seats(self):
        with pytest.raises(ValidationError):
            mixer.blend(Table, number=2, seats=0)

    def test_create_table_with_negative_seats(self):
        with pytest.raises(ValidationError):
            mixer.blend(Table, number=2, seats=-2)


@pytest.mark.django_db
class TestReservation:
    def test_create_reservation(self):
        table = mixer.blend(Table)
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        reservation = mixer.blend(
            Reservation, table=table, start_time=start_time, end_time=end_time)
        assert str(
            reservation) == f"Reservation for Table {table.number} at {start_time}"
        assert reservation.table == table
        assert reservation.start_time == start_time
        assert reservation.end_time == end_time

    def test_create_reservation_without_table(self):
        with pytest.raises(IntegrityError):
            mixer.blend(
                Reservation, start_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(hours=1))

    def test_create_overlapping_reservation(self):
        table = mixer.blend(Table)
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        mixer.blend(
            Reservation, table=table, start_time=start_time, end_time=end_time)
        with pytest.raises(ValidationError):
            mixer.blend(
                Reservation, table=table, start_time=start_time, end_time=end_time - timezone.timedelta(minutes=30))

    def test_create_reservation_with_end_time_before_start_time(self):
        table = mixer.blend(Table)
        start_time = timezone.now()
        end_time = start_time - timezone.timedelta(hours=1)
        with pytest.raises(ValidationError):
            mixer.blend(
                Reservation, table=table, start_time=start_time, end_time=end_time)
