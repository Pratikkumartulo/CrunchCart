chipsData = {
    1: {
        "name": "Sour Cream & Cheddar",
        "price": 89.00,
        "image_url": "img1.jpg",
        "description": "Creamy cheddar meets tangy sour cream in this classic blend.",
        "discount": 10,
        "stock": 20
    },
    2: {
        "name": "Ginger",
        "price": 29.00,
        "image_url": "img2.jpg",
        "description": "Zesty ginger for a sharp, bold taste experience.",
        "discount": 0,
        "stock": 40
    },
    3: {
        "name": "Carolina Reaper",
        "price": 99.00,
        "image_url": "img3.jpg",
        "description": "Insanely spicy chips made with the world's hottest chili.",
        "discount": 5,
        "stock": 12
    },
    4: {
        "name": "Salt & Vinegar",
        "price": 59.00,
        "image_url": "img4.jpg",
        "description": "Sharp vinegar and classic salt in every crunchy bite.",
        "discount": 0,
        "stock": 25
    },
    5: {
        "name": "Dill Pickle",
        "price": 49.00,
        "image_url": "img5.jpg",
        "description": "Bold pickle flavor with a touch of dill herb.",
        "discount": 15,
        "stock": 18
    },
    6: {
        "name": "Sour Cream & Onion",
        "price": 79.00,
        "image_url": "img6.jpg",
        "description": "Smooth sour cream blended with onion zing.",
        "discount": 0,
        "stock": 0
    },
    7: {
        "name": "Barbecue",
        "price": 109.00,
        "image_url": "img7.jpg",
        "description": "Smoky and sweet barbecue seasoning on every chip.",
        "discount": 25,
        "stock": 10
    },
    8: {
        "name": "Chile Limon",
        "price": 89.00,
        "image_url": "img8.jpg",
        "description": "Spicy chile and tangy lime for a Mexican twist.",
        "discount": 5,
        "stock": 30
    },
    9: {
        "name": "Garlic",
        "price": 69.00,
        "image_url": "img10.jpg",
        "description": "Crunchy chips infused with rich garlic essence.",
        "discount": 0,
        "stock": 22
    },
    10: {
        "name": "Spicy Schezwan",
        "price": 19.00,
        "image_url": "img11.jpg",
        "description": "Hot and tangy chips with authentic Schezwan flair.",
        "discount": 10,
        "stock": 50
    },
    11: {
        "name": "Sweet & Spicy Honey",
        "price": 39.00,
        "image_url": "img12.jpg",
        "description": "Sticky sweet honey meets fiery spices in a perfect balance.",
        "discount": 0,
        "stock": 0
    },
    12: {
        "name": "Adobadas",
        "price": 29.00,
        "image_url": "img13.jpg",
        "description": "Rich Mexican-style adobo sauce flavor explosion.",
        "discount": 20,
        "stock": 14
    },
    13: {
        "name": "Spicy Peri Peri",
        "price": 29.00,
        "image_url": "img14.jpg",
        "description": "Fiery Peri Peri flavor that kicks in with heat and flavor.",
        "discount": 0,
        "stock": 33
    },
    14: {
        "name": "Classic(Salted)",
        "price": 59.00,
        "image_url": "img15.jpg",
        "description": "Simple and timeless salted chips for every snack mood.",
        "discount": 5,
        "stock": 27
    }
}


def findMaxThreeDiscount(chips):
    max1 = {"discount":float('-inf')}
    max2 = {"discount":float('-inf')}
    max3 = {"discount":float('-inf')}
    for i in chips:
        if chips[i]['discount']>max1['discount']:
            max3 = max2
            max2 = max1
            max1 = chips[i]
            max1['id'] = i
        elif chips[i]['discount'] > max2['discount']:
            max3 = max2
            max2 = chips[i]
            max2['id'] = i
        elif chips[i]['discount'] >max3['discount']:
            max3 = chips[i]
            max3['id'] = i
    return max1,max2,max3
