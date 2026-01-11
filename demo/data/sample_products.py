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
- Promotions & Deals
- Seasonal Items
"""
from typing import List
from models import Product


def get_sample_products() -> List[Product]:
    """Generate 80+ realistic truck stop products with promotions and variety.
    
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
        
        # PROMOTIONS & DEALS (15 products - Special pricing and bundles)
        Product(
            sku="PROMO-FUEL-SAVE",
            name="Fuel Rewards Card - $0.10/gal Discount",
            category="Promotions & Deals",
            location="Service Desk",
            price=0.00,
            description="Sign up for free fuel rewards card, save $0.10 per gallon"
        ),
        Product(
            sku="PROMO-COFFEE-DEAL",
            name="Coffee Club Card - Buy 9 Get 1 Free",
            category="Promotions & Deals",
            location="Coffee Station",
            price=0.00,
            description="Free loyalty card for coffee purchases"
        ),
        Product(
            sku="PROMO-SHOWER-BUNDLE",
            name="Shower & Laundry Bundle - SAVE $5",
            category="Promotions & Deals",
            location="Service Desk",
            price=15.00,
            description="Shower credit + laundry service combo, regular $20"
        ),
        Product(
            sku="PROMO-BREAKFAST-SPECIAL",
            name="Trucker Breakfast Special - $6.99",
            category="Promotions & Deals",
            location="Hot Food Counter",
            price=6.99,
            description="2 eggs, bacon, hash browns, toast & coffee (reg $9.99)"
        ),
        Product(
            sku="PROMO-ENERGY-PACK",
            name="Road Warrior Energy Pack - SAVE $3",
            category="Promotions & Deals",
            location="Aisle 3 - Snacks",
            price=19.99,
            description="2 Red Bulls + jerky + energy bar combo (reg $22.99)"
        ),
        Product(
            sku="PROMO-OIL-CHANGE",
            name="Full Synthetic Oil Change - $20 OFF",
            category="Promotions & Deals",
            location="Service Desk",
            price=69.99,
            description="Complete oil change service (reg $89.99)"
        ),
        Product(
            sku="PROMO-TIRE-CHECK",
            name="Free Tire Pressure Check",
            category="Promotions & Deals",
            location="Service Desk",
            price=0.00,
            description="Complimentary tire pressure inspection and fill"
        ),
        Product(
            sku="PROMO-WASH-WKLY",
            name="Weekly Wash Pass - 3 Washes for $300",
            category="Promotions & Deals",
            location="Truck Wash Bay",
            price=300.00,
            description="Unlimited washes this week (save $75)"
        ),
        Product(
            sku="PROMO-SNACK-BOGO",
            name="Buy 2 Get 1 Free - All Candy Bars",
            category="Promotions & Deals",
            location="Aisle 3 - Snacks",
            price=0.00,
            description="Mix and match any candy bars - promotion"
        ),
        Product(
            sku="PROMO-WATER-CASE",
            name="Water Case Sale - 2 for $8",
            category="Promotions & Deals",
            location="Cooler - Back",
            price=8.00,
            description="Buy 2 cases of water for $8 (reg $4.99 each)"
        ),
        Product(
            sku="PROMO-CB-INSTALL",
            name="CB Radio with Free Installation",
            category="Promotions & Deals",
            location="Aisle 4 - Electronics",
            price=129.99,
            description="Cobra CB radio + free installation (save $50 on install)"
        ),
        Product(
            sku="PROMO-PIZZA-SODA",
            name="Pizza & Drink Combo - $5.49",
            category="Promotions & Deals",
            location="Hot Food Counter",
            price=5.49,
            description="Any pizza slice + 20oz fountain drink (save $1.50)"
        ),
        Product(
            sku="PROMO-TRUCKER-KIT",
            name="New Driver Starter Kit - $99",
            category="Promotions & Deals",
            location="Aisle 2 - Trucker Gear",
            price=99.00,
            description="Logbook, gloves, flashlight, vest & thermos ($130 value)"
        ),
        Product(
            sku="PROMO-LOYALTY-10PCT",
            name="Loyalty Members Save 10% Today",
            category="Promotions & Deals",
            location="Service Desk",
            price=0.00,
            description="Join loyalty program and save 10% on your purchase today"
        ),
        Product(
            sku="PROMO-WEEKEND-PARKING",
            name="Weekend Parking Special - $35 for 2 Nights",
            category="Promotions & Deals",
            location="Service Desk",
            price=35.00,
            description="Friday & Saturday overnight parking (reg $40)"
        ),
        
        # SEASONAL ITEMS (10 products - Winter focused)
        Product(
            sku="SEASON-GLOVES-WINTER",
            name="Insulated Winter Work Gloves",
            category="Seasonal Items",
            location="Aisle 2 - Trucker Gear",
            price=34.99,
            description="Waterproof insulated gloves for cold weather driving"
        ),
        Product(
            sku="SEASON-SCRAPER-ICE",
            name="Heavy-Duty Ice Scraper with Brush",
            category="Seasonal Items",
            location="Aisle 1 - Auto",
            price=14.99,
            description="48-inch ice scraper for trucks and trailers"
        ),
        Product(
            sku="SEASON-ANTIGEL-FUEL",
            name="Winter Diesel Anti-Gel Treatment",
            category="Seasonal Items",
            location="Aisle 1 - Auto",
            price=19.99,
            description="Prevents fuel gelling in extreme cold, treats 250 gallons"
        ),
        Product(
            sku="SEASON-BLANKET-EMERG",
            name="Emergency Thermal Blanket 4-Pack",
            category="Seasonal Items",
            location="Aisle 5 - Safety",
            price=12.99,
            description="Mylar emergency blankets for winter breakdowns"
        ),
        Product(
            sku="SEASON-HEATER-CABIN",
            name="12V Portable Cabin Heater",
            category="Seasonal Items",
            location="Aisle 4 - Electronics",
            price=79.99,
            description="Auxiliary heater for cab, plugs into cigarette lighter"
        ),
        Product(
            sku="SEASON-SOUP-THERMOS",
            name="Insulated Soup Thermos - 24oz",
            category="Seasonal Items",
            location="Aisle 6 - Convenience",
            price=24.99,
            description="Keeps soup or coffee hot for 12+ hours"
        ),
        Product(
            sku="SEASON-CHOCOLATE-HOT",
            name="Premium Hot Chocolate Mix",
            category="Seasonal Items",
            location="Coffee Station",
            price=2.99,
            description="Gourmet hot chocolate, 16 oz cup"
        ),
        Product(
            sku="SEASON-WINDOW-COVER",
            name="Windshield Sun Shade/Winter Cover",
            category="Seasonal Items",
            location="Aisle 1 - Auto",
            price=29.99,
            description="Dual-purpose: sun shade in summer, frost cover in winter"
        ),
        Product(
            sku="SEASON-BATTERY-JUMP",
            name="Portable Jump Starter with Air Compressor",
            category="Seasonal Items",
            location="Aisle 1 - Auto",
            price=149.99,
            description="12,000 mAh jump starter for dead batteries, includes air pump"
        ),
        Product(
            sku="SEASON-HAND-WARMER",
            name="Hand Warmer Packs - 10 Pairs",
            category="Seasonal Items",
            location="Aisle 5 - Safety",
            price=9.99,
            description="Disposable hand warmers, 8+ hours of heat each"
        ),
        
        # ADDITIONAL FOOD & BEVERAGES (10 products)
        Product(
            sku="FOOD-WRAP-CHICKEN",
            name="Grilled Chicken Wrap",
            category="Hot Food & Beverages",
            location="Hot Food Counter",
            price=7.99,
            description="Grilled chicken wrap with lettuce, tomato, ranch"
        ),
        Product(
            sku="FOOD-TACO-BEEF",
            name="Beef Tacos - 3 Pack",
            category="Hot Food & Beverages",
            location="Hot Food Counter",
            price=6.99,
            description="Three soft shell tacos with seasoned beef"
        ),
        Product(
            sku="FOOD-CHILI-BOWL",
            name="Homestyle Chili Bowl",
            category="Hot Food & Beverages",
            location="Hot Food Counter",
            price=5.99,
            description="Hearty beef chili with crackers and cheese"
        ),
        Product(
            sku="FOOD-SALAD-CHEF",
            name="Chef Salad with Chicken",
            category="Hot Food & Beverages",
            location="Cooler - Front",
            price=8.49,
            description="Fresh chef salad with grilled chicken and dressing"
        ),
        Product(
            sku="SNACK-CHIPS-VARIETY",
            name="Frito-Lay Variety Pack",
            category="Energy & Snacks",
            location="Aisle 3 - Snacks",
            price=12.99,
            description="20-count variety pack: Doritos, Cheetos, Lays, Fritos"
        ),
        Product(
            sku="SNACK-PROTEIN-BAR",
            name="Quest Protein Bars 12-Pack",
            category="Energy & Snacks",
            location="Aisle 3 - Snacks",
            price=24.99,
            description="High-protein bars, 20g protein each, assorted flavors"
        ),
        Product(
            sku="SNACK-POPCORN-BAG",
            name="Smartfood Popcorn - Family Size",
            category="Energy & Snacks",
            location="Aisle 3 - Snacks",
            price=4.99,
            description="White cheddar popcorn, 10.5 oz bag"
        ),
        Product(
            sku="SNACK-GATORADE-6PK",
            name="Gatorade 6-Pack Variety",
            category="Energy & Snacks",
            location="Cooler - Front",
            price=7.99,
            description="Sports drinks, 20 oz bottles, assorted flavors"
        ),
        Product(
            sku="FOOD-MUFFIN-BLUEBERRY",
            name="Fresh Blueberry Muffin",
            category="Hot Food & Beverages",
            location="Bakery Counter",
            price=2.99,
            description="Freshly baked jumbo blueberry muffin"
        ),
        Product(
            sku="FOOD-DONUT-GLAZED",
            name="Glazed Donuts - Half Dozen",
            category="Hot Food & Beverages",
            location="Bakery Counter",
            price=5.99,
            description="Six fresh glazed donuts"
        ),
        
        # ADDITIONAL SUPPLIES & ACCESSORIES (10 products)
        Product(
            sku="TRUCK-COOLER-12V",
            name="12V Electric Cooler for Trucks",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=89.99,
            description="Portable electric cooler, 24L capacity, plugs into cigarette lighter"
        ),
        Product(
            sku="TRUCK-INVERTER-POWER",
            name="2000W Power Inverter 12V to 110V",
            category="Trucker Supplies",
            location="Aisle 4 - Electronics",
            price=199.99,
            description="Convert 12V DC to 110V AC, power laptops and appliances"
        ),
        Product(
            sku="TRUCK-MATTRESS-TOPPER",
            name="Memory Foam Truck Mattress Topper",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=79.99,
            description="3-inch memory foam topper for truck sleeper cab"
        ),
        Product(
            sku="TRUCK-FAN-PORTABLE",
            name="12V Portable Truck Fan",
            category="Trucker Supplies",
            location="Aisle 2 - Trucker Gear",
            price=34.99,
            description="Clip-on oscillating fan for truck cab"
        ),
        Product(
            sku="ELECT-TABLET-MOUNT",
            name="Tablet Mount for Truck Dashboard",
            category="Electronics",
            location="Aisle 4 - Electronics",
            price=39.99,
            description="Universal tablet mount for GPS or entertainment"
        ),
        Product(
            sku="ELECT-BACKUP-CAM",
            name="Wireless Backup Camera System",
            category="Electronics",
            location="Aisle 4 - Electronics",
            price=179.99,
            description="Wireless rear-view camera with 7-inch monitor"
        ),
        Product(
            sku="SAFE-TIRE-GAUGE",
            name="Digital Tire Pressure Gauge",
            category="Safety & Lighting",
            location="Aisle 5 - Safety",
            price=24.99,
            description="Heavy-duty digital gauge for truck tires, 0-200 PSI"
        ),
        Product(
            sku="SAFE-REFLECTOR-TRIANGLE",
            name="Emergency Reflector Triangles 3-Pack",
            category="Safety & Lighting",
            location="Aisle 5 - Safety",
            price=19.99,
            description="DOT-approved reflective warning triangles"
        ),
        Product(
            sku="CONV-SUNSCREEN-SPF50",
            name="Sport Sunscreen SPF 50",
            category="Convenience",
            location="Aisle 6 - Convenience",
            price=9.99,
            description="Water-resistant sunscreen for drivers, 8 oz bottle"
        ),
        Product(
            sku="CONV-BUG-SPRAY",
            name="OFF! Deep Woods Insect Repellent",
            category="Convenience",
            location="Aisle 6 - Convenience",
            price=7.99,
            description="Insect repellent for rest stop breaks, 6 oz spray"
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
