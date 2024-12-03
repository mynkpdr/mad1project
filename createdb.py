from app import create_app
from app.models.user import User, Role
from app.models import db
from datetime import datetime, timedelta
from faker import Faker
import random
import requests


fake = Faker('en_IN')  # Use 'en_IN' locale for Indian data
api_url = "http://127.0.0.1:5000"

# Define known city latitudes and longitudes within India
city_coordinates = [
    (28.6129, 77.2295),  # India Gate, Delhi
    (18.9220, 72.8347),  # Gateway of India, Mumbai
    (13.0827, 80.2707),  # Marina Beach, Chennai
    (12.9716, 77.5946),  # Lalbagh Botanical Garden, Bangalore
    (22.5726, 88.3639),  # Victoria Memorial, Kolkata
    (23.0339, 72.5850),  # Sabarmati Ashram, Ahmedabad
    (17.3850, 78.4867),  # Charminar, Hyderabad
    (26.9220, 75.8267),  # Hawa Mahal, Jaipur
    (15.2993, 74.1240),  # Baga Beach, Goa
    (11.0168, 76.9558),  # Dhyanalinga Temple, Coimbatore
]

random_images = ['Ab De Villiers.jpeg',
                 'Jasprit Bumrah.jpg',
                 'MS Dhoni.jpg',
                 'Rohit Sharma.png',
                 'Sachin Tendulkar.png',
                 'Smriti Mandhana.jpg',
                 'Shreyanka Patil.jpg'
                 ]

def generate_indian_city_latitude_longitude():
    # Randomly select a city and return its coordinates
    return random.choice(city_coordinates)

def generate_random_image():
    # Randomly select a city and return its coordinates
    return random.choice(random_images)


app = create_app()

# Create the database structure
with app.app_context():
    db.drop_all()
    db.create_all()

    # List of categories to be added
    categories = [
        {"name": "Home Cleaning"},
        {"name": "Plumbing"},
        {"name": "Electrical"},
        {"name": "Carpentry"},
        {"name": "Painting"},
        {"name": "Gardening"},
        {"name": "Appliance Repair"}
    ]

    # List of services to be added
    services = [
        {"name": "Full House Cleaning", "price": 2499, "description": "Deep cleaning of the entire house including kitchen, bathrooms, and all rooms.", "image": "home.png", "category_name": "Home Cleaning"},
        {"name": "Sofa Cleaning", "price": 1199, "description": "Cleaning of sofa fabric and cushions using high-quality cleaning agents.", "image": "home.png", "category_name": "Home Cleaning"},
        {"name": "Bathroom Cleaning", "price": 799, "description": "Thorough cleaning of bathroom tiles, fittings, and mirrors.", "image": "home.png", "category_name": "Home Cleaning"},
        {"name": "Pipe Installation", "price": 1499, "description": "Installation of water and drainage pipes.", "image": "plumber.png", "category_name": "Plumbing"},
        {"name": "Leakage Repair", "price": 999, "description": "Fixing water leaks in pipes, faucets, and other plumbing fixtures.", "image": "plumber.png", "category_name": "Plumbing"},
        {"name": "Water Heater Installation", "price": 1799, "description": "Installation of electric or gas water heaters.", "image": "plumber.png", "category_name": "Plumbing"},
        {"name": "Fan Installation", "price": 499, "description": "Installation of ceiling or wall fans in any room.", "image": "electrician.png", "category_name": "Electrical"},
        {"name": "Switchboard Repair", "price": 699, "description": "Repair of damaged or malfunctioning switchboards.", "image": "electrician.png", "category_name": "Electrical"},
        {"name": "Wiring Replacement", "price": 2999, "description": "Complete rewiring of rooms or houses for safety.", "image": "electrician.png", "category_name": "Electrical"},
        {"name": "Furniture Assembly", "price": 1199, "description": "Assembly of furniture items like tables, chairs, and shelves.", "image": "carpenter.png", "category_name": "Carpentry"},
        {"name": "Door Repair", "price": 899, "description": "Repairing damaged doors and hinges.", "image": "carpenter.png", "category_name": "Carpentry"},
        {"name": "Custom Shelves Installation", "price": 1999, "description": "Design and installation of custom wooden shelves.", "image": "carpenter.png", "category_name": "Carpentry"},
        {"name": "Interior Wall Painting", "price": 4999, "description": "Painting of interior walls with the color of your choice.", "image": "painter.png", "category_name": "Painting"},
        {"name": "Exterior House Painting", "price": 9999, "description": "Painting of the exterior walls of the house.", "image": "painter.png", "category_name": "Painting"},
        {"name": "Fence Painting", "price": 1999, "description": "Painting of wooden or metal fences.", "image": "painter.png", "category_name": "Painting"},
        {"name": "Lawn Mowing", "price": 1199, "description": "Mowing of grass and maintenance of garden lawns.", "image": "pest_control.png", "category_name": "Gardening"},
        {"name": "Hedge Trimming", "price": 1499, "description": "Trimming of hedges and shrubs to maintain garden aesthetics.", "image": "gardener.png", "category_name": "Gardening"},
        {
        "name": "AC Repair and Installation",
        "price": 1199,
        "description": "Repair and installation of air conditioners, including split and window AC units.",
        "image": "ac_repair.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "Water Purifier Sales And Repair",
        "price": 799,
        "description": "Sales, installation, and repair of water purifiers for clean drinking water.",
        "image": "water_purifier.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "Refrigerator Repair",
        "price": 999,
        "description": "Repair services for refrigerators, addressing cooling issues and part replacements.",
        "image": "refrigerator.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "Washing Machine Repair",
        "price": 899,
        "description": "Repair of front-load and top-load washing machines, including motor and drum repairs.",
        "image": "washing_machine.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "Laptop / Desktop Sales And Repair",
        "price": 1499,
        "description": "Sales, installation, and repair of laptops and desktops, including hardware and software services.",
        "image": "laptop_repair.png",
        "category_name": "Electrical"
    },
    {
        "name": "Microwave Repair",
        "price": 699,
        "description": "Repair services for microwave ovens, including heating and electrical issues.",
        "image": "microwave.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "Gas Geyser Repair",
        "price": 599,
        "description": "Repair of gas geysers, ensuring efficient water heating and safety checks.",
        "image": "gas_geyser.png",
        "category_name": "Plumbing"
    },
    {
        "name": "Dish Washer Repair",
        "price": 899,
        "description": "Repair services for dishwashers, addressing water leakage and cleaning efficiency.",
        "image": "dish_washer.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "Geyser Repair",
        "price": 699,
        "description": "Repair of electric geysers, fixing heating elements and water flow issues.",
        "image": "geyser.png",
        "category_name": "Plumbing"
    },
    {
        "name": "Water Pump Repair",
        "price": 799,
        "description": "Repair services for water pumps, including motor and pressure issues.",
        "image": "water_pump.png",
        "category_name": "Plumbing"
    },
    {
        "name": "Water Level Controller Installation",
        "price": 1499,
        "description": "Installation and maintenance of water level controllers for overhead tanks.",
        "image": "water_level_controller.png",
        "category_name": "Plumbing"
    },
    {
        "name": "Inverter UPS Sales And Repair",
        "price": 2499,
        "description": "Sales and repair of inverters and UPS systems for uninterrupted power supply.",
        "image": "inverter_ups.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "CCTV Installation & Repairs",
        "price": 1999,
        "description": "Installation and repair of CCTV cameras and surveillance systems.",
        "image": "cctv.png",
        "category_name": "Electrical"
    },
    {
        "name": "Gas Stove And Hob Repair and Installation",
        "price": 699,
        "description": "Repair and installation of gas stoves and hobs, ensuring safety and functionality.",
        "image": "gas_stove.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "Solar Water Heater Repair",
        "price": 1499,
        "description": "Repair and maintenance services for solar water heaters.",
        "image": "solar_heater.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "Cooking Range Repair",
        "price": 999,
        "description": "Repair services for cooking ranges, including burners and electrical components.",
        "image": "cooking_range.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "Chimney Repair and Installation",
        "price": 1199,
        "description": "Installation and repair of kitchen chimneys, ensuring proper ventilation and smoke extraction.",
        "image": "chimney.png",
        "category_name": "Appliance Repair"
    },
    {
        "name": "TV Repair and Installation",
        "price": 1299,
        "description": "Repair and installation services for LED and LCD TVs, including screen and sound issues.",
        "image": "tv_repair.png",
        "category_name": "Electrical"
    }]


    name="Virat Kohli"
    username="virat.kohli"
    email="admin@email.com"
    phone="9999999999"
    pincode=600036
    password="12345678"
    admin = User(name=name, username=username, email=email, password=password, role=Role.ADMIN, phone=phone, pincode=pincode)
    db.session.add(admin)
    db.session.commit()

    print("ADMIN ADDED")

    response = requests.post(f'{api_url}/api/gettoken', json={"email":"admin@email.com", "password":"12345678"})
    if response.status_code == 200:
        token = response.json()['token']
    else:
        raise Exception
    
    category_map = {}
    for category_data in categories:
        response = requests.post(f'{api_url}/api/categories', json={"name": category_data['name']}, headers={"token":token})
        if response.status_code == 201:
            category = response.json()  # Parse the JSON response if it contains category details
            category_map[category_data['name']] = category['data']['id']  # Store the category ID or any other needed field
        else:
            raise Exception(f"Failed to create category {category_data['name']}: {response.text}")
    
    print("CATEGORIES ADDED")

    for service_data in services:
        service = {
            "name":service_data["name"],
            "price":service_data["price"],
            "description":service_data["description"],
            "image":service_data["image"],
            "category_id":category_map[service_data["category_name"]]  # Link service to the appropriate category
        }
        response = requests.post(f'{api_url}/api/services', json=service, headers={"token":token})
        if response.status_code == 201:
            pass
        else:
            raise Exception(f"Failed to create services {service['name']}: {response.text}")
    
    print("SERVICES ADDED")

    for i in range(1, 51):
        profile_image = generate_random_image()
        latitude, longitude = generate_indian_city_latitude_longitude()
        professional = {
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "profile_image": profile_image,
            "username": f"professional{i}",
            "about": fake.sentence(),
            "address": fake.address(),
            "password": "12345678",  # Or use `fake.password()` for random passwords
            "pincode": int(fake.postcode()),
            "lat": str(latitude),
            "lng": str(longitude),
            "service_id":i-20 if i>20 else i,
            "service_price":i*500+i*100+99,
            "experience":5 + i,
            "documents":f"sample.pdf"
        }
        professional1 = {
            "name": "Professional",
            "email": "professional@email.com",
            "phone": "9898989898",
            "profile_image": profile_image,
            "username": f"professional",
            "about": "Deleniti illo ratione pariatur doloribus alias molestiae fugiat.",
            "address": "E-38/39, Rajiv Chowk, Inner Circle, Block E, Connaught Place",
            "password": "12345678",  # Or use `fake.password()` for random passwords
            "pincode": 110001,
            "lat": "22.567495",
            "lng": "88.3519948",
            "service_id":1,
            "service_price":699,
            "experience":6,
            "documents":f"sample.pdf"
        }
        if i == 1:
            response1 = requests.post(f'{api_url}/api/professionals', json=professional1)
        else:
            response1 = requests.post(f'{api_url}/api/professionals', json=professional)
        if response1.status_code == 201:
            if i < 31:
                response2 = requests.post(f'{api_url}/api/professional/{i}/active', json={"active":True}, headers={"token":token})
                if response2.status_code == 200:
                    pass
                else:
                    raise Exception(response2.text)
        else:
            raise Exception(f"Failed to create professional {professional['name']}: {response1.text}")
    
    print("PROFESSIONALS ADDED")

    for i in range(1, 101):
        profile_image = generate_random_image()
        latitude, longitude = generate_indian_city_latitude_longitude()
        customer = {
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "profile_image": profile_image,
            "username": f"customer{i}",
            "about": fake.sentence(),
            "address": fake.address(),
            "password": "12345678",  # Or use `fake.password()` for random passwords
            "pincode": int(fake.postcode()),
            "lat": str(latitude),
            "lng": str(longitude)
        }
        customer1 = {
            "name": "Customer",
            "email": "customer@email.com",
            "phone": "9898989899",
            "profile_image": profile_image,
            "username": "customer",
            "about": "Deleniti illo ratione pariatur doloribus alias molestiae fugiat.",
            "address": "4th Floor, East India Building, 8, Madan St, Chandni Chawk, Bowbazar, Kolkata, India",
            "password": "12345678",  # Or use `fake.password()` for random passwords
            "pincode": 700072,
            "lat": "22.566495",
            "lng": "88.3518849"
        }
        if i == 1:
            response = requests.post(f'{api_url}/api/customers', json=customer1)
        else:
            response = requests.post(f'{api_url}/api/customers', json=customer)
        if response.status_code == 201:
            pass
        else:
            raise Exception(f"Failed to create professional {customer['name']}: {response.text}")
    
    print("CUSTOMERS ADDED")

    for i in range(1, 31):
        contact = {
            "name":fake.name(),
            "email":fake.email(),
            "phone":fake.phone_number(),
            "message":fake.text()
        }
        response = requests.post(f'{api_url}/api/contacts', json=contact)
        if response.status_code == 201:
            pass
        else:
            raise Exception(f"Failed to create contact {contact['name']}: {response.text}")

    print("CONTACTS ADDED")

    for i in range(1, 31):
        service_request = {
            "service_id":i-20 if i > 20 else i,
            "customer_id":i,
            "professional_id":i-20 if i > 20 else i,
            "start_date":(datetime.now().date() + timedelta(days=i)).isoformat(),
            "total_days":i-20 if i > 20 else i,
            "hours_per_day":i-20 if i > 20 else i,
            "remarks":f"Service request {i} remarks"
        }
        response1 = requests.post(f'{api_url}/api/service_requests', json=service_request, headers={"token":token})
        if response1.status_code == 201:
            if i <= 10:
                response2 = requests.put(f'{api_url}/api/service_request/{i}', json={"service_status":"CLOSED"}, headers={"token":token})
                if response2.status_code == 200:
                    pass
                else:
                    raise Exception(response2.text)
            elif i <= 15:
                response3 = requests.put(f'{api_url}/api/service_request/{i}', json={"service_status":"ASSIGNED"}, headers={"token":token})
                if response3.status_code == 200:
                    pass
                else:
                    raise Exception(response3.text)
            elif i <= 30 and i > 25:
                response4 = requests.put(f'{api_url}/api/service_request/{i}', json={"service_status":"REJECTED"}, headers={"token":token})
                if response4.status_code == 200:
                    pass
                else:
                    raise Exception(response4.text)
        else:
            raise Exception(f"Failed to create service_request {service_request['service_id']}: {response1.text}")

    print("SERVICE REQUESTS ADDED")

    for i in range(1, 11):
        review = {
            'professional_id': i,
            'customer_id': i,
            'service_request_id': i,
            'description': fake.text(),
            'value': random.randint(1, 5),
        }
        response = requests.post(f'{api_url}/api/reviews', json=review, headers={"token":token})
        if response.status_code == 201:
            pass
        else:
            raise Exception(f"Failed to create review {review['professional_id']}: {response.text}")
        
    print("REVIEWS ADDED")
