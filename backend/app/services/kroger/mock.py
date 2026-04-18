import re

PRODUCT_FIXTURES: dict[str, list[dict]] = {
    "milk": [
        {
            "productId": "0001111041700",
            "description": "Simple Truth Organic Whole Milk",
            "brand": "Simple Truth",
            "upc": "0001111041700",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/e8f5e9/1b5e20?text=Milk"}]}],
            "items": [{"size": "1 gal", "price": {"regular": 5.49, "promo": 4.79}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0001111042200",
            "description": "Kroger Whole Milk",
            "brand": "Kroger",
            "upc": "0001111042200",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/e8f5e9/1b5e20?text=Milk"}]}],
            "items": [{"size": "1 gal", "price": {"regular": 3.99}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0001111043100",
            "description": "Horizon Organic Whole Milk",
            "brand": "Horizon",
            "upc": "0001111043100",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/e8f5e9/1b5e20?text=Milk"}]}],
            "items": [{"size": "1 gal", "price": {"regular": 6.29, "promo": 5.99}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "eggs": [
        {
            "productId": "0002100079003",
            "description": "Simple Truth Cage Free Large White Eggs",
            "brand": "Simple Truth",
            "upc": "0002100079003",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff9c4/f57f17?text=Eggs"}]}],
            "items": [{"size": "12 ct", "price": {"regular": 4.99, "promo": 3.99}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0002100079010",
            "description": "Kroger Large White Eggs",
            "brand": "Kroger",
            "upc": "0002100079010",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff9c4/f57f17?text=Eggs"}]}],
            "items": [{"size": "12 ct", "price": {"regular": 3.29}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0002100079020",
            "description": "Vital Farms Pasture-Raised Eggs",
            "brand": "Vital Farms",
            "upc": "0002100079020",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff9c4/f57f17?text=Eggs"}]}],
            "items": [{"size": "12 ct", "price": {"regular": 7.49, "promo": 6.99}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "bread": [
        {
            "productId": "0003800082929",
            "description": "Dave's Killer Bread Organic 21 Whole Grains",
            "brand": "Dave's Killer Bread",
            "upc": "0003800082929",
            "categories": ["Bakery"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/ffe0b2/e65100?text=Bread"}]}],
            "items": [{"size": "27 oz", "price": {"regular": 5.99, "promo": 4.99}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0003800082930",
            "description": "Kroger Honey Wheat Bread",
            "brand": "Kroger",
            "upc": "0003800082930",
            "categories": ["Bakery"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/ffe0b2/e65100?text=Bread"}]}],
            "items": [{"size": "20 oz", "price": {"regular": 2.49}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0003800082931",
            "description": "Nature's Own 100% Whole Wheat Bread",
            "brand": "Nature's Own",
            "upc": "0003800082931",
            "categories": ["Bakery"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/ffe0b2/e65100?text=Bread"}]}],
            "items": [{"size": "20 oz", "price": {"regular": 3.99, "promo": 3.49}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "chicken": [
        {
            "productId": "0002030000001",
            "description": "Simple Truth Organic Boneless Skinless Chicken Breast",
            "brand": "Simple Truth",
            "upc": "0002030000001",
            "categories": ["Meat"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fce4ec/880e4f?text=Chicken"}]}],
            "items": [{"size": "per lb", "price": {"regular": 7.99, "promo": 6.99}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0002030000002",
            "description": "Kroger Boneless Skinless Chicken Breast",
            "brand": "Kroger",
            "upc": "0002030000002",
            "categories": ["Meat"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fce4ec/880e4f?text=Chicken"}]}],
            "items": [{"size": "per lb", "price": {"regular": 4.99, "promo": 3.99}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0002030000003",
            "description": "Bell & Evans Air Chilled Chicken Breast",
            "brand": "Bell & Evans",
            "upc": "0002030000003",
            "categories": ["Meat"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fce4ec/880e4f?text=Chicken"}]}],
            "items": [{"size": "per lb", "price": {"regular": 9.99}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "apples": [
        {
            "productId": "0004011000001",
            "description": "Gala Apples",
            "brand": "",
            "upc": "0004011000001",
            "categories": ["Produce"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/e8f5e9/1b5e20?text=Apples"}]}],
            "items": [{"size": "per lb", "price": {"regular": 1.99, "promo": 1.49}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0004011000002",
            "description": "Honeycrisp Apples",
            "brand": "",
            "upc": "0004011000002",
            "categories": ["Produce"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/e8f5e9/1b5e20?text=Apples"}]}],
            "items": [{"size": "per lb", "price": {"regular": 2.99, "promo": 2.49}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0004011000003",
            "description": "Fuji Apples Bag",
            "brand": "",
            "upc": "0004011000003",
            "categories": ["Produce"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/e8f5e9/1b5e20?text=Apples"}]}],
            "items": [{"size": "3 lb bag", "price": {"regular": 4.99}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "butter": [
        {
            "productId": "0007027000001",
            "description": "Kerrygold Pure Irish Butter",
            "brand": "Kerrygold",
            "upc": "0007027000001",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff8e1/ff6f00?text=Butter"}]}],
            "items": [{"size": "8 oz", "price": {"regular": 4.99, "promo": 3.99}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0007027000002",
            "description": "Kroger Unsalted Butter",
            "brand": "Kroger",
            "upc": "0007027000002",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff8e1/ff6f00?text=Butter"}]}],
            "items": [{"size": "16 oz", "price": {"regular": 3.49}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0007027000003",
            "description": "Land O Lakes Salted Butter",
            "brand": "Land O Lakes",
            "upc": "0007027000003",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff8e1/ff6f00?text=Butter"}]}],
            "items": [{"size": "16 oz", "price": {"regular": 5.29, "promo": 4.79}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "cheese": [
        {
            "productId": "0007105000001",
            "description": "Tillamook Medium Cheddar Cheese",
            "brand": "Tillamook",
            "upc": "0007105000001",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff3e0/bf360c?text=Cheese"}]}],
            "items": [{"size": "16 oz", "price": {"regular": 6.99, "promo": 5.99}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0007105000002",
            "description": "Kroger Shredded Mexican Cheese",
            "brand": "Kroger",
            "upc": "0007105000002",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff3e0/bf360c?text=Cheese"}]}],
            "items": [{"size": "8 oz", "price": {"regular": 2.99}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "yogurt": [
        {
            "productId": "0007935000001",
            "description": "Chobani Plain Greek Yogurt",
            "brand": "Chobani",
            "upc": "0007935000001",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/e3f2fd/0d47a1?text=Yogurt"}]}],
            "items": [{"size": "32 oz", "price": {"regular": 5.49, "promo": 4.49}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0007935000002",
            "description": "Kroger Greek Yogurt Vanilla",
            "brand": "Kroger",
            "upc": "0007935000002",
            "categories": ["Dairy"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/e3f2fd/0d47a1?text=Yogurt"}]}],
            "items": [{"size": "32 oz", "price": {"regular": 3.99}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "pasta": [
        {
            "productId": "0007680000001",
            "description": "Barilla Penne Rigate Pasta",
            "brand": "Barilla",
            "upc": "0007680000001",
            "categories": ["Pasta & Rice"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/f3e5f5/4a148c?text=Pasta"}]}],
            "items": [{"size": "16 oz", "price": {"regular": 1.89, "promo": 1.49}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0007680000002",
            "description": "Kroger Penne Pasta",
            "brand": "Kroger",
            "upc": "0007680000002",
            "categories": ["Pasta & Rice"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/f3e5f5/4a148c?text=Pasta"}]}],
            "items": [{"size": "16 oz", "price": {"regular": 0.99}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "rice": [
        {
            "productId": "0007431000001",
            "description": "Lundberg Family Farms Organic Long Grain Brown Rice",
            "brand": "Lundberg",
            "upc": "0007431000001",
            "categories": ["Pasta & Rice"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/f9fbe7/33691e?text=Rice"}]}],
            "items": [{"size": "2 lb", "price": {"regular": 4.99, "promo": 3.99}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0007431000002",
            "description": "Kroger Long Grain White Rice",
            "brand": "Kroger",
            "upc": "0007431000002",
            "categories": ["Pasta & Rice"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/f9fbe7/33691e?text=Rice"}]}],
            "items": [{"size": "5 lb", "price": {"regular": 3.49}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "coffee": [
        {
            "productId": "0004656000001",
            "description": "Starbucks Pike Place Roast Ground Coffee",
            "brand": "Starbucks",
            "upc": "0004656000001",
            "categories": ["Coffee & Tea"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/3e2723/ffffff?text=Coffee"}]}],
            "items": [{"size": "12 oz", "price": {"regular": 10.99, "promo": 8.99}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0004656000002",
            "description": "Kroger Colombian Ground Coffee",
            "brand": "Kroger",
            "upc": "0004656000002",
            "categories": ["Coffee & Tea"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/3e2723/ffffff?text=Coffee"}]}],
            "items": [{"size": "12 oz", "price": {"regular": 5.99}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "orange juice": [
        {
            "productId": "0003000000001",
            "description": "Tropicana Pure Premium Original Orange Juice",
            "brand": "Tropicana",
            "upc": "0003000000001",
            "categories": ["Juice"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff3e0/e65100?text=OJ"}]}],
            "items": [{"size": "52 oz", "price": {"regular": 5.49, "promo": 4.49}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0003000000002",
            "description": "Kroger Orange Juice 100% Pure Squeezed",
            "brand": "Kroger",
            "upc": "0003000000002",
            "categories": ["Juice"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff3e0/e65100?text=OJ"}]}],
            "items": [{"size": "52 oz", "price": {"regular": 3.99}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "cereal": [
        {
            "productId": "0003800000001",
            "description": "Cheerios Original Whole Grain Oats Cereal",
            "brand": "General Mills",
            "upc": "0003800000001",
            "categories": ["Breakfast"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff8e1/f9a825?text=Cereal"}]}],
            "items": [{"size": "18 oz", "price": {"regular": 5.49, "promo": 4.49}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0003800000002",
            "description": "Kroger Toasted Oats Cereal",
            "brand": "Kroger",
            "upc": "0003800000002",
            "categories": ["Breakfast"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff8e1/f9a825?text=Cereal"}]}],
            "items": [{"size": "14 oz", "price": {"regular": 2.49}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "ground beef": [
        {
            "productId": "0002030100001",
            "description": "Simple Truth 85% Lean Ground Beef",
            "brand": "Simple Truth",
            "upc": "0002030100001",
            "categories": ["Meat"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fce4ec/b71c1c?text=Beef"}]}],
            "items": [{"size": "per lb", "price": {"regular": 6.99, "promo": 5.99}, "inventory": {"status": "AVAILABLE"}}],
        },
        {
            "productId": "0002030100002",
            "description": "Kroger 80% Lean Ground Beef",
            "brand": "Kroger",
            "upc": "0002030100002",
            "categories": ["Meat"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fce4ec/b71c1c?text=Beef"}]}],
            "items": [{"size": "per lb", "price": {"regular": 4.99, "promo": 4.49}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "banana": [
        {
            "productId": "0004011000101",
            "description": "Bananas",
            "brand": "",
            "upc": "0004011000101",
            "categories": ["Produce"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff9c4/f57f17?text=Bananas"}]}],
            "items": [{"size": "per lb", "price": {"regular": 0.59}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
    "bananas": [
        {
            "productId": "0004011000101",
            "description": "Bananas",
            "brand": "",
            "upc": "0004011000101",
            "categories": ["Produce"],
            "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": "https://placehold.co/80x80/fff9c4/f57f17?text=Bananas"}]}],
            "items": [{"size": "per lb", "price": {"regular": 0.59}, "inventory": {"status": "AVAILABLE"}}],
        },
    ],
}

_CATEGORY_KEYWORDS = ["dairy", "meat", "produce", "bakery", "breakfast", "juice", "pasta", "rice", "coffee"]


def _generic_product(query: str) -> dict:
    return {
        "productId": f"GENERIC_{query[:8].upper()}",
        "description": f"{query.title()} (Store Brand)",
        "brand": "Kroger",
        "upc": None,
        "categories": ["Grocery"],
        "images": [{"perspective": "front", "sizes": [{"size": "medium", "url": f"https://placehold.co/80x80/e8f5e9/1b5e20?text={query[:6].title()}"}]}],
        "items": [{"size": "", "price": {"regular": 3.99, "promo": 3.49}, "inventory": {"status": "AVAILABLE"}}],
    }


async def search_products(query: str, location_id: str, limit: int = 10) -> list[dict]:
    key = query.lower().strip()
    key = re.sub(r"\s+", " ", key)

    for fixture_key, products in PRODUCT_FIXTURES.items():
        if fixture_key == key or fixture_key in key or key in fixture_key:
            return products[:limit]

    words = key.split()
    for fixture_key, products in PRODUCT_FIXTURES.items():
        fk_words = fixture_key.split()
        if any(w in fk_words for w in words if len(w) > 3):
            return products[:limit]

    return [_generic_product(query)]
