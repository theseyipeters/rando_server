from faker.providers import BaseProvider
from data.NG.names import first_names, last_names
from data.NG.streetsandcities import streets, cities
from data.NG.companies import companies

class NigeriaProvider(BaseProvider):
    def first_name(self):
        return self.random_element(first_names)

    def last_name(self):
        return self.random_element(last_names)
    
    def name(self):
        return f"{self.first_name()} {self.last_name()}"
    
    def phone_number(self):
        prefixes = ['070', '080', '090', '081']
        return f"{self.random_element(prefixes)}{self.numerify('########')}"
    
    def address(self):
        return f"{self.random_int(1, 100)} {self.random_element(streets)}, {self.random_element(cities)}"
    
    def company(self):
        return self.random_element(companies)
    
    def id(self):
        id_prefix = ['6']
        return f"{self.random_element(id_prefix)}{self.numerify('##########')}"

class USProvider(BaseProvider):
    def phone_number(self):
        prefixes = ['202', '303', '404', '505']
        return f"{self.random_element(prefixes)}-{self.numerify('###-####')}"
