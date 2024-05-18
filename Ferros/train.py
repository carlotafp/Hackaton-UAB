class Train:
    def __init__(self, line, ID, direction, stops, train_type, position, m1, m2, mi, ri = 0):
        self._line = line                                          # Línia (L7, S2, RL1...)
        self._ID = ID                                              # ID tren
        self._direction = direction                                # D/A
        self._stops = stops                                        # quantes parades li queden
        self._train_type = train_type                              # tipus tren (113/114/115 etc)
        self._position = position                                  # geolocalització
        self._carriers = {'M1': m1, 'M2': m2, 'RI': ri, 'MI': mi}  # Carrier % status

        """Només tenen 3 vagons, el RI no existeix en aquests trens"""
        if train_type in ['113', '213', '213x2']: #113 L7, 213 llobregat-anoia
            self._carriers['RI'] = None


    # Getters
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
    
    def dict(self):
        return {'line': self._line, 'ID': self._ID, 'direction': self._direction, 'stops': self._stops, 'train_type': self._train_type, 'position': self._position, 'carriers': self._carriers}

    def __str__(self):
        return f"Line: {self._line} - ID: {self._ID} - Direction: {self._direction} - Stops left: {self._stops} - Type: {self._train_type} - Position: {self._position} - Carriers: {self._carriers}"
    
    def __repr__(self):
        return f"Train(line={self._line}, ID={self._ID}, direction={self._direction}, stops={self._stops}, train_type={self._train_type}, position={self._position}, carriers={self._carriers})"

