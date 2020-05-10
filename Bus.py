from typing import Dict, Any


class SeatInformation:

    def __init__(self,
                 seat_number):
        self.taken = False
        self.passenger_name = ""
        self.seat_number = seat_number

    def set_passenger(self, passenger_name):
        self.passenger_name = passenger_name
        # empty string indicates the seat is empty
        if passenger_name == "":
            self.taken = False
        else:
            self.taken = True


class BusInformation:

    def __init__(self,
                 bus_number,
                 driver_name,
                 arrival_time,
                 departure_time,
                 destination,
                 origin,
                 bus_size=21):
        self.bus_size = bus_size
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.driver_name = driver_name
        self.bus_number = bus_number
        # todo: make seats based on the bus size
        self.seats = self.init_seats()

    def init_seats(self):
        seat_list = []
        for i in range(self.bus_size):
            seat_list.append(SeatInformation(seat_number=i))
        return seat_list

    def detailed_print(self, print_seats=False):
        print(f'Bus Number: {self.bus_number}')
        print(f'Bus Size: {self.bus_size}')
        print(f'From: {self.origin}')
        print(f'To: {self.destination}')
        print(f'Departure: {self.departure_time}')
        print(f'Arrival: {self.arrival_time}')
        print(f'Bus Is Full: {self.is_full()}')

        if print_seats:
            print("--------------------")
            print("Seat Info:")
            for seat in self.seats:
                print(f'Seat No:{seat.seat_number} {seat.passenger_name}')

    def edit_seat_info(self, seat_number, passenger_name):
        # check the seat number to be valid
        if seat_number < 0 or seat_number > self.bus_size:
            print("Seat Number does not exist")
            return False
        # change it
        self.seats[seat_number].set_passenger(passenger_name)

    def is_full(self):
        # check for empty seats
        for seat in self.seats:
            if not seat.taken:
                return False
        return True

    def seat_is_taken(self, seat_number):
        """
        handle value error
        :param seat_number:
        :return:
        """
        # check range
        if seat_number < 0 or seat_number > self.bus_size:
            print("Seat Number does not exist")
            raise ValueError
        # check seat
        return self.seats[seat_number].taken
        pass


class Reservation:

    buses: Dict[int, BusInformation]

    # todo: dont repeat your self at make a bus valid method or smthing :)

    def __init__(self):
        self.buses = {}  # store key value pairs of bus number and bus

    def get_available_buses(self):
        print("List of Available buses")
        numbers = []
        for bus in self.buses.values():
            if not bus.is_full():
                numbers.append(bus.bus_number)
        print(numbers)
        print("detailed:")
        for bus_number in numbers:
            self.get_bus_info(bus_number)

    def get_bus_info(self, bus_number, detailed=False):
        # get a specific bus information
        # validate bus exists
        if self.buses.get(bus_number) is None:
            print("bus number does not exist - operation failed")
        else:
            self.buses[bus_number].detailed_print(detailed)

    def get_registered_buses(self):
        # get bus numbers registered, and their state
        print("Registered buses:")
        if len(self.buses) == 0:
            print("No Bus Information Registered")
        else:
            for bus in self.buses.values():
                bus.detailed_print(print_seats=False)

    def register_bus_information(self,
                                 bus_number,
                                 driver_name,
                                 arrival_time,
                                 departure_time,
                                 destination,
                                 origin):
        # validate bus number
        if self.buses.get(bus_number) is not None:
            print("bus number already exists exist - operation failed")
        else:
            # todo: check departure and arrival time
            # todo: could check destination and origin
            self.buses[bus_number] = BusInformation(bus_number=bus_number,
                                                    driver_name=driver_name,
                                                    arrival_time=arrival_time,
                                                    departure_time=departure_time,
                                                    destination=destination,
                                                    origin=origin)

    def remove_bus_information(self, bus_number):
        # validate exists then del
        if self.buses.get(bus_number) is None:
            print("bus number does not exist - operation failed")
        else:
            del self.buses[bus_number]

    def reserve_bus(self, bus_number, seat_number, passenger_name):
        if passenger_name == "":
            print("no passenger name - operation failed")
        # validate bus exists
        if self.buses.get(bus_number) is None:
            print("bus number does not exist - operation failed")
        else:
            # validate seat is empty
            bus = self.buses[bus_number]
            try:
                if bus.seat_is_taken(seat_number=seat_number):
                    print("seat already reserved - operation failed")
                else:
                    bus.edit_seat_info(seat_number=seat_number, passenger_name=passenger_name)
            except ValueError:
                pass

    def remove_reservation(self, bus_number, seat_number):
        # validate bus exists
        if self.buses.get(bus_number) is None:
            print("bus number does not exist - operation failed")
        else:
            # validate seat is full
            bus = self.buses[bus_number]
            try:
                if bus.seat_is_taken(seat_number=seat_number):
                    print("seat not reserved, would you like to reserve it - operation failed")
                else:
                    bus.edit_seat_info(seat_number=seat_number, passenger_name="")
            except ValueError:
                pass


if __name__ == '__main__':
    r = Reservation()
    print("should return no bus registered")
    r.get_registered_buses()
    print()
    # register a bus
    r.register_bus_information(bus_number=111,
                               driver_name="abas",
                               arrival_time="2020/05/10-23:30:00",
                               departure_time="2020/05/10-23:40:00",
                               destination="Tehran",
                               origin="Mashad")
    print("should print the bus")
    r.get_registered_buses()
    print()
    print()

    print("Should print detailed view of the bus")
    r.get_bus_info(bus_number=111, detailed=True)

    r.register_bus_information(bus_number=222,
                               driver_name="ali",
                               arrival_time="2020/05/10-23:30:00",
                               departure_time="2020/05/10-23:40:00",
                               destination="Tehran",
                               origin="Gorgan")

    for i in range(21):
        r.reserve_bus(222, i, f'Iman number:{i}')

    print("Should now have a ful bus")
    r.get_registered_buses()

    print()
    print("show reservation information:")
    r.get_bus_info(222, True)

    print("available buses, should show only 111")
    r.get_available_buses()

