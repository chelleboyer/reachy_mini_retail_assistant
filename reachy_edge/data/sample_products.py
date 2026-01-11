"""Sample truck stop/travel center product data for L2 cache initialization.

Includes realistic products across key categories:
- Fuel & Fluids
- Trucker Supplies
- Electronics
- Energy & Snacks
- Hot Food & Beverages
- Services
- Safety & Lighting
- Convenience
"""
from typing import List
from models import Product


def get_sample_products() -> List[Product]:
    """Generate 40+ realistic truck stop products.
    
    Returns:
        List of Product models with authentic truck stop/travel center items
    """
    return [
        # FUEL & FLUIDS (6 products)
        Product(
            sku="FUEL-DIESEL-001",
            name="Premium Diesel Fuel",
            category="Fuel & Fluids",
            location="Fuel Island 1-4",
            price=3.89,
            description="Ultra-low sulfur diesel fuel for commercial trucks and RVs"
        ),
        Product(
            sku="FUEL-DEF-001",
            name="BlueDEF Diesel Exhaust Fluid",
            category="Fuel & Fluids",
            location="Fuel Island 2",
            price=12.99,
            description="Premium DEF fluid meets ISO 22241 standards for SCR systems"
        ),
        Product(
            sku="FUEL-OIL-015",
            name="Shell Rotella T6 15W-40 Motor Oil",
            category="Fuel & Fluids",
            location="Aisle 1 - Auto",
            price=89.99,
            description="Synthetic heavy-duty diesel engine oil, 5-gallon jug"
        ),
        Product(
            sku="FUEL-COOL-003",
            name="Prestone Extended Life Antifreeze",
            category="Fuel & Fluids",
            location="Aisle 1 - Auto",
            price=24.99,
            description="Long-life coolant for diesel engines, 1 gallon"
        ),
        Product(
            sku="FUEL-WASH-007",
            name="Rain-X Windshield Washer Fluid",
            category="Fuel & Fluids",
            location="Aisle 1 - Auto",
            price=6.99,
            description="All-season windshield washer fluid, bug remover formula"
        ),
        Product(
            sku="FUEL-HEET-002",
            name="HEET Diesel Fuel Treatment",
            category="Fuel & Fluids",
            location="Aisle 1 - Auto",
            price=4.99,
            description="Prevents fuel line freeze-up and removes water from diesel"
        ),
        
        # TRUCKER SUPPLIES (8 products)
        Product(
            sku="TRUCK-LOG-101",
            name="Simplified Logbook for Truck Drivers",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=8.99,
            description="DOT compliant driver logbook, 31-day format"
        ),
        Product(
            sku="TRUCK-STRAP-205",
            name="Ratchet Tie-Down Straps 4-Pack",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=34.99,
            description="Heavy-duty 2-inch x 27-foot straps, 10,000 lb capacity"
        ),
        Product(
            sku="TRUCK-BUNGEE-303",
            name="Bungee Cord Assortment",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=12.99,
            description="24-piece bungee set with hooks, various sizes"
        ),
        Product(
            sku="TRUCK-MUD-404",
            name="Heavy-Duty Mud Flaps",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=49.99,
            description="18-wheeler universal mud flaps, pair"
        ),
        Product(
            sku="TRUCK-GLOVE-505",
            name="Mechanix Wear Work Gloves",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=24.99,
            description="Heavy-duty work gloves for drivers and mechanics"
        ),
        Product(
            sku="TRUCK-TARP-606",
            name="Silver Poly Tarp 20x30",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=39.99,
            description="Heavy-duty waterproof tarp for load protection"
        ),
        Product(
            sku="TRUCK-CHAIN-707",
            name="Tire Chains for Commercial Trucks",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=189.99,
            description="Heavy-duty snow chains for 18-wheelers"
        ),
        Product(
            sku="TRUCK-LOCK-808",
            name="King Pin Lock",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=129.99,
            description="Anti-theft king pin lock for semi-trailers"
        ),
        
        # ELECTRONICS (5 products)
        Product(
            sku="ELECT-CB-105",
            name="Cobra 29 LX CB Radio",
            category="Electronics",
            location="Aisle 4 - Electronics",
            price=129.99,
            description="40-channel CB radio with weather alerts and Bluetooth"
        ),
        Product(
            sku="ELECT-GPS-206",
            name="Garmin dezl OTR800 Truck GPS",
            category="Electronics",
            location="Aisle 4 - Electronics",
            price=599.99,
            description="Professional truck GPS with live traffic and weigh station alerts"
        ),
        Product(
            sku="ELECT-DASH-307",
            name="Nextbase Dash Cam",
            category="Electronics",
            location="Aisle 4 - Electronics",
            price=149.99,
            description="1080p HD dash camera with night vision"
        ),
        Product(
            sku="ELECT-CHARGE-408",
            name="USB-C Fast Charger for Trucks",
            category="Electronics",
            location="Aisle 4 - Electronics",
            price=29.99,
            description="Dual-port fast charger, 12V cigarette lighter adapter"
        ),
        Product(
            sku="ELECT-HEAD-509",
            name="Bluetooth Headset for Drivers",
            category="Electronics",
            location="Aisle 4 - Electronics",
            price=79.99,
            description="Noise-canceling Bluetooth headset for hands-free calls"
        ),
        
        # ENERGY & SNACKS (8 products)
        Product(
            sku="SNACK-COFFEE-301",
            name="Truck Stop Coffee - Large",
            category="Energy & Snacks",
            location="Coffee Station",
            price=2.49,
            description="Fresh-brewed coffee, 20 oz cup"
        ),
        Product(
            sku="SNACK-REDBULL-402",
            name="Red Bull Energy Drink 4-Pack",
            category="Energy & Snacks",
            location="Cooler - Front",
            price=9.99,
            description="Energy drink 4-pack, 8.4 oz cans"
        ),
        Product(
            sku="SNACK-JERKY-503",
            name="Jack Link's Beef Jerky Variety Pack",
            category="Energy & Snacks",
            location="Aisle 3 - Snacks",
            price=15.99,
            description="Beef jerky variety pack, 10 oz total"
        ),
        Product(
            sku="SNACK-NUTS-604",
            name="Planters Mixed Nuts",
            category="Energy & Snacks",
            location="Aisle 3 - Snacks",
            price=8.99,
            description="Roasted mixed nuts, 16 oz canister"
        ),
        Product(
            sku="SNACK-BAR-705",
            name="Clif Bar Energy Bars 12-Pack",
            category="Energy & Snacks",
            location="Aisle 3 - Snacks",
            price=14.99,
            description="Energy bars variety pack for long hauls"
        ),
        Product(
            sku="SNACK-TRAIL-806",
            name="Nature Valley Trail Mix",
            category="Energy & Snacks",
            location="Aisle 3 - Snacks",
            price=6.99,
            description="Trail mix with nuts and dried fruit, 26 oz"
        ),
        Product(
            sku="SNACK-WATER-907",
            name="Bottled Water 24-Pack",
            category="Energy & Snacks",
            location="Cooler - Back",
            price=4.99,
            description="Purified drinking water, 16.9 oz bottles"
        ),
        Product(
            sku="SNACK-5HOUR-008",
            name="5-hour Energy Shot 6-Pack",
            category="Energy & Snacks",
            location="Front Counter",
            price=12.99,
            description="Energy shots for alertness, berry flavor"
        ),
        
        # HOT FOOD & BEVERAGES (5 products)
        Product(
            sku="FOOD-PIZZA-201",
            name="Fresh Pizza Slice",
            category="Hot Food & Beverages",
            location="Hot Food Counter",
            price=3.99,
            description="Fresh-made pizza slice, pepperoni or cheese"
        ),
        Product(
            sku="FOOD-BURGER-302",
            name="Double Cheeseburger Meal",
            category="Hot Food & Beverages",
            location="Hot Food Counter",
            price=8.99,
            description="Double cheeseburger with fries and drink"
        ),
        Product(
            sku="FOOD-CHICKEN-403",
            name="Fried Chicken Tenders - 4 Piece",
            category="Hot Food & Beverages",
            location="Hot Food Counter",
            price=6.99,
            description="Crispy chicken tenders with dipping sauce"
        ),
        Product(
            sku="FOOD-BREAK-504",
            name="Breakfast Sandwich",
            category="Hot Food & Beverages",
            location="Hot Food Counter",
            price=4.99,
            description="Egg, sausage, and cheese on English muffin"
        ),
        Product(
            sku="FOOD-HOT-605",
            name="Hot Dog with Fixings",
            category="Hot Food & Beverages",
            location="Hot Food Counter",
            price=2.99,
            description="All-beef hot dog with condiments"
        ),
        
        # SERVICES (4 products)
        Product(
            sku="SERV-SHOWER-001",
            name="Shower Credit - 30 Minutes",
            category="Services",
            location="Service Desk",
            price=15.00,
            description="Clean private shower for longhaul drivers, towel included"
        ),
        Product(
            sku="SERV-LAUNDRY-002",
            name="Laundry Service - 1 Load",
            category="Services",
            location="Service Desk",
            price=5.00,
            description="Wash and dry one load of laundry"
        ),
        Product(
            sku="SERV-WASH-003",
            name="Truck Wash - Full Service",
            category="Services",
            location="Truck Wash Bay",
            price=125.00,
            description="Complete exterior truck and trailer wash"
        ),
        Product(
            sku="SERV-PARK-004",
            name="Reserved Parking - Overnight",
            category="Services",
            location="Service Desk",
            price=20.00,
            description="Reserved overnight parking spot with security"
        ),
        
        # SAFETY & LIGHTING (4 products)
        Product(
            sku="SAFE-LED-101",
            name="LED Emergency Road Flares",
            category="Safety & Lighting",
            location="Aisle 5 - Safety",
            price=29.99,
            description="Rechargeable LED warning lights, 3-pack"
        ),
        Product(
            sku="SAFE-VEST-202",
            name="High-Visibility Safety Vest",
            category="Safety & Lighting",
            location="Aisle 5 - Safety",
            price=12.99,
            description="ANSI Class 2 reflective safety vest"
        ),
        Product(
            sku="SAFE-FLASH-303",
            name="Heavy-Duty LED Flashlight",
            category="Safety & Lighting",
            location="Aisle 5 - Safety",
            price=34.99,
            description="Rechargeable tactical flashlight, 1000 lumens"
        ),
        Product(
            sku="SAFE-FIRST-404",
            name="Roadside Emergency Kit",
            category="Safety & Lighting",
            location="Aisle 5 - Safety",
            price=49.99,
            description="Complete emergency kit with first aid and tools"
        ),
        
        # CONVENIENCE (4 products)
        Product(
            sku="CONV-SUNGL-501",
            name="Polarized Driving Sunglasses",
            category="Convenience",
            location="Front Counter",
            price=19.99,
            description="UV protection sunglasses for driving"
        ),
        Product(
            sku="CONV-WIPES-602",
            name="Wet Wipes Travel Pack",
            category="Convenience",
            location="Aisle 6 - Convenience",
            price=4.99,
            description="Personal hygiene wipes, 40 count"
        ),
        Product(
            sku="CONV-ASPIRIN-703",
            name="Advil Pain Reliever",
            category="Convenience",
            location="Aisle 6 - Convenience",
            price=8.99,
            description="Ibuprofen pain relief, 50 tablets"
        ),
        Product(
            sku="CONV-TOOTH-804",
            name="Travel Toothbrush & Toothpaste Kit",
            category="Convenience",
            location="Aisle 6 - Convenience",
            price=5.99,
            description="Portable oral care kit for drivers"
        ),
    ]


def load_sample_data(cache):
    """Load sample products into ProductCache.
    
    Args:
        cache: ProductCache instance (initialized)
    
    Returns:
        int: Number of products loaded
    """
    products = get_sample_products()
    cache.insert_products(products)
    return len(products)
