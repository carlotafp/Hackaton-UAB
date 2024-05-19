class Train:
    class _Carrier:
        def __init__(self, type_train, name, percent):
            self._name = name
            self._percent = percent
            self._minusvalid = 0
            if name in ['M1', 'M2']: self._minusvalid = 4
            self._reservats = 8
            if type_train in ['113', '114']: self._reservats += 8

        def to_dict(self):
            return {
                'name': self._name,
                'percent': self._percent,
                'minusvalid': self._minusvalid,
                'reservats': self._reservats
            }

        def __str__(self):
            return f"Name: {self._name}, Percent: {self._percent}%, Minusvalid: {self._minusvalid}, Reserved: {self._reservats}"

        def __repr__(self):
            return f"Name: {self._name}, Percent: {self._percent}%, Minusvalid: {self._minusvalid}, Reserved: {self._reservats}"

    def __init__(self, line, ID, direction, stops, train_type, position, m1, m2, mi, ri=0):
        self._line = line  # Línia (L7, S2, RL1...)
        self._ID = ID  # ID viatje
        self._direction = direction  # D/A
        self._stops = stops  # quantes parades li queden
        self._train_type = train_type  # tipus tren (113/114/115 etc)
        self._position = position  # geolocalització

        """Només tenen 3 vagons, el RI no existeix en aquests trens"""
        if train_type in ['113', '213', '213x2']:  # 113 L7, 213 llobregat-anoia
            self._carriers = {'M1': self._Carrier(train_type, 'M1', m1), 'M2': self._Carrier(train_type, 'M2', m2),
                              'MI': self._Carrier(train_type, 'MI', mi), 'RI': None}
        else:
            self._carriers = {'M1': self._Carrier(train_type, 'M1', m1), 'M2': self._Carrier(train_type, 'M2', m2),
                              'RI': self._Carrier(train_type, 'RI', ri),
                              'MI': self._Carrier(train_type, 'MI', mi)}  # _Carrier % status

    def to_dict(self):
        return {
            'line': self._line,
            'ID': self._ID,
            'direction': self._direction,
            'stops': self._stops,
            'train_type': self._train_type,
            'position': self._position,
            'carriers': {k: v.to_dict() if v else None for k, v in self._carriers.items()}
        }

    def queden_minusvalids(self):
        return not (all(element._minusvalid == 0 for element in self._carriers.values()))

    def queden_reservats(self):
        return not (all(element._reservats == 0 for element in self._carriers.values()))

    def decrementa_minusvalids(self):

        minim = float("inf")
        cotxe = None

        for element in self._carriers.values():
            if element._minusvalid > 0:
                if element._percent < minim:
                    minim = element._percent
                    cotxe = element
        if cotxe:
            cotxe._minusvalid -= 1

        return cotxe

    def decrementa_reservats(self):

        minim = float("inf")
        cotxe = None

        for element in self._carriers.values():
            if element._reservats > 0:
                if element._percent < minim:
                    minim = element._percent
                    cotxe = element
        if cotxe:
            cotxe._reservats -= 1

        return cotxe

    def get_line(self):
        return self._line

    def get_ID(self):
        return self._ID

    def get_direction(self):
        return self._direction

    def get_stops(self):
        return self._stops

    def get_train_type(self):
        return self._train_type

    def get_position(self):
        return self._position

    def get_carriers(self):
        return self._carriers

    # Setters
    def set_direction(self, direction):
        self._direction = direction

    def set_stops(self, stops):
        self._stops = stops

    def set_position(self, position):
        self._position = position

    def set_carrier(self, m1, m2, mi, ri=0):
        if self._train_type in ['113', '213', '213x2']:
            self._carriers = {'M1': self._Carrier(self._train_type, 'M1', m1),
                              'M2': self._Carrier(self._train_type, 'M2', m2),
                              'MI': self._Carrier(self._train_type, 'MI', mi), 'RI': None}
        else:
            self._carriers = {'M1': self._Carrier(self._train_type, 'M1', m1),
                              'M2': self._Carrier(self._train_type, 'M2', m2),
                              'RI': self._Carrier(self._train_type, 'RI', ri),
                              'MI': self._Carrier(self._train_type, 'MI', mi)}

    def __repr__(self):
        return f"{self._line} {self._ID} {self._direction} {self._stops} {self._train_type} {self._position} {self._carriers}"

    def __str__(self):
        return f"{self._line} {self._ID} {self._direction} {self._stops} {self._train_type} {self._position} {self._carriers}"
        return f"{self._line} {self._ID} {self._direction} {self._stops} {self._train_type} {self._position} {self._carriers}"
