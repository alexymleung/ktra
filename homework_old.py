import json
from events.models import Event

# Delete all existing data in the Event model
Event.objects.all().delete()

# Load new data from events.json and insert into the Event model
with open('events.json') as f:
    events_json = json.load(f)

for e in events_json:
    event = Event(
        title=e['title'],
        event_type=e['event_type'],
        content=e['content'],
        publish_date=e['publish_date']
    )
    event.save()

#Clear all data and Insert new data to service

import json 
from services.models import Service

# Delete all existing data in the Service model
Service.objects.all().delete()

# Load new data from services.json and insert into the Service model 
with open('services.json') as f:
    services_json = json.load(f)
for s in services_json:
    service = Service(
    title = s['title'],
    service_type = s['service_type'],
    description = s['description'],
    service_start_time = s['service_start_time'],
    service_end_time = s['service_end_time'],
    fee = s['fee'],
    quota = s['quota'],
    )
    service.save()


import json 
from donations.models import Donation

# Delete all existing data in the Donation model
Donation.objects.all().delete()

# Load new data from donations.json and insert into the Donation model 
with open('donations.json') as f:
    donations_json = json.load(f)
for d in donations_json:
    donation = Donation(
    donor = d['donor'],
    email = d['email'],
    phone = d['phone'],
    address = d['address'],
    amount = d['amount'],
    donation_date = d['donation_date'],
    message = d['message'],
    payment_type = d['payment_type'],
    transaction_date = d['transaction_date']
    )
    donation.save()