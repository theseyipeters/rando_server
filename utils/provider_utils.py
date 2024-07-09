from faker import Faker
from rando_providers import NigeriaProvider, USProvider

# Setting up the Nigerian provider
fake = Faker('en_US')
fake.add_provider(NigeriaProvider)

# Setting up the US provider
us_fake = Faker('en_US')
us_fake.add_provider(USProvider)

def choose_provider(provider):
    if provider == 'NG':
        return fake
    elif provider == 'US':
        return us_fake
    else:
        raise ValueError(f"Unsupported provider: {provider}")
