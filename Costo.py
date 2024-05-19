class Cost():
    def __init__(self, state): # constructor
        self.state = state
        self.MANPOWERDICTIONARY = {'Aguascalientes':0.0,  # idicex of incrementes from every state
                                   'Baja California':11.7,
                                   'Baja California Sur':1.8,
                                   'Campeche':4.8,
                                   'Chiapas':10.0,
                                   'Chihuahua':5,
                                   'Coahuila':3.9,
                                   'Colima':4.2,
                                   'Durango':4.9,
                                   'Guanajuato':2.2,
                                   'Guerrero':8.8,
                                   'Hidalgo':10.8,
                                   'Jalisco':3.5,
                                   'México':4.3,
                                   'Michoacán':7.2,
                                   'Morelos':4.1,
                                   'Nayarit':3.2,
                                   'Nuevo León':3.7,
                                   'Oaxaca':8.5,
                                   'Puebla':6.5,
                                   'Querétaro':6.4,
                                   'Quintana Roo':6.6,
                                   'San Luis Potosí':13.9,
                                   'Sinaloa':11.0,
                                   'Sonora':5.7,
                                   'Tabasco': 6.6,
                                   'Tamaulipas':5.0,
                                   'Tlaxcala':7.2,
                                   'Veracruz':8.2,
                                   'Yucatán':0.7,
                                   'Zacatecas':-4.5}
        self.MEDIA = 111.77   # the mean cost of manpower in México

    def getManPower(self):    # getting the value of the manpower by using the mean and index of increment
        index = self.MANPOWERDICTIONARY[self.state] + 100
        manPower = (self.MEDIA * index) / 100
        return manPower

    def setInfrastructure(self): # question on the quality of the infrastructure to see how many estimated porcentage we add to the final cost
        print('\nFrom the following options (Good, Bad, Regular) write the correct one...')
        level = input('What is the level of infrastructure like? (How difficult is it to arrive to the destination place or to carry instruments): ')

        valid_levels = {'good','Good','GOOD','Bad','bad','Bad','regular','Regular','REGULAR'}
        while level not in valid_levels:
            print('Error! The input is incorrect.')
            level =input('Try again: ')

        self.level = level

    def calculate(self):
        if self.level =='Bad'or self.level == 'bad'or self.level == 'BAD':
            cost = self.getManPower() * 1.02
        elif self.level == 'Regular'or self.level == 'regular'or self.level == 'REGULAR':
            cost = self.getManPower() * 1.01
        else:
            cost = self.getManPower() * 1.005

        result = 'The estimated cost of planting a tree in {} is: ${}'.format(self.state, cost)
        return result