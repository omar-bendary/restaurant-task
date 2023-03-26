from rest_framework.decorators import action
from datetime import datetime, time, timedelta
from .serializers import ReservationSerializer
from .models import Table, Reservation
from rest_framework import viewsets, status, permissions
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import TableSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = (permissions.IsAdminUser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.reservations.count() > 0:
            return Response({'error': 'Cannot delete a table with reservations.'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reservations to be viewed or edited.
    """
    queryset = Reservation.objects.all().order_by('start_time')
    serializer_class = ReservationSerializer

    @action(detail=False, methods=['get'])
    def available_time_slots(self, request):
        """
        Returns a list of available time slots for a given number of seats.
        """
        seats = request.query_params.get('seats')
        if not seats:
            return Response({'error': 'Please provide number of seats'})

        try:
            seats = int(seats)
        except ValueError:
            return Response({'error': 'Number of seats should be an integer'})

        now = timezone.now()
        end_of_day = timezone.datetime.combine(now.date(), time.max)

        # Filter reservations for today
        reservations_today = Reservation.objects.filter(
            start_time__date=now.date(),
            end_time__gte=now,
        )

        # Get all tables with required seats or more
        tables = Table.objects.filter(seats__gte=seats).order_by('seats')

        # Find available time slots
        available_time_slots = []
        start_time = now
        for reservation in reservations_today:
            # Check if there's an available time slot before the next reservation
            if start_time + timezone.timedelta(minutes=30) <= reservation.start_time:
                end_time = reservation.start_time
                if end_time <= end_of_day:
                    available_time_slots.append((start_time, end_time))
                start_time = reservation.end_time

        # Check if there's an available time slot after the last reservation
        if start_time + timezone.timedelta(minutes=30) <= end_of_day:
            available_time_slots.append((start_time, end_of_day))

        # Filter available time slots based on table availability
        available_time_slots_filtered = []
        for start_time, end_time in available_time_slots:
            available_tables = tables.exclude(
                reservations__start_time__lt=end_time,
                reservations__end_time__gt=start_time,
            )
            if available_tables:
                available_time_slots_filtered.append((start_time, end_time))

        return Response({'available_time_slots': available_time_slots_filtered})

    def create(self, request):
        """
        Creates a new reservation.
        """
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()

            # Check if the table is available at the specified time slot
            tables = Table.objects.filter(id=reservation.table.id)
            overlapping_reservations = Reservation.objects.filter(
                table__in=tables,
                start_time__lt=reservation.end_time,
                end_time__gt=reservation.start_time,
            )
            if overlapping_reservations.exists():
                reservation.delete()
                return Response({'error': 'Table is not available at the specified time slot'})

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    # Get reservations for today

    @action(detail=False, methods=['GET'])
    def today(self, request):
        today = datetime.today()
        reservations = Reservation.objects.filter(
            start_time__gte=today, start_time__lte=today+timedelta(days=1))
        page = self.paginate_queryset(reservations)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # Get all reservations
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        # Filter by table(s)
        table = request.query_params.get('table', None)
        if table is not None:
            queryset = queryset.filter(table=table)

        # Filter by date range
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date is not None and end_date is not None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(
                end_date, '%Y-%m-%d') + timedelta(days=1)
            queryset = queryset.filter(
                start_time__gte=start_date, start_time__lte=end_date)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # Delete a reservation
    def destroy(self, request, pk=None):
        reservation = self.get_object()
        if reservation.start_time < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Cannot delete past reservations.'})
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
