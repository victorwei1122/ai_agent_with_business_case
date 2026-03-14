import random
from datetime import datetime, timedelta
from src.db.database import SessionLocal
from src.db.models import Product, ProductReview

def generate_synthetic_reviews():
    """Generates 3-5 synthetic reviews for every product in the database."""
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        print(f"Found {len(products)} products. Generating reviews...")

        review_templates = [
            # Positive
            ("Absolute game changer! The {feature} is better than expected.", 5),
            ("Solid performance for the price. Highly recommend the {feature}.", 4),
            ("Very impressed with the build quality and the {feature}.", 5),
            ("Exactly what I needed. The {feature} works perfectly.", 4),
            # Neutral/Constructive
            ("It's decent, but I wish the {feature} was a bit more robust.", 3),
            ("Good product overall. The {feature} is okay, but could be improved.", 3),
            # Negative/Issues
            ("Disappointed. The {feature} stopped working after a week.", 2),
            ("Not worth the money. Specifically having issues with the {feature}.", 1),
            ("Average. The {feature} is definitely the weak point here.", 2)
        ]

        features_by_product = {
            "P001": ["battery life", "keyboard feel", "processor speed", "portability"],
            "P002": ["noise cancellation", "battery", "comfort", "sound clarity"],
            "P003": ["stability", "motor noise", "assembly process", "durability"],
            "P004": ["switch tactile feel", "backlighting", "connectivity", "cable quality"],
            "P005": ["color accuracy", "refresh rate", "stand flexibility", "brightness"],
            "P006": ["lumbar support", "cushioning", "armrest adjustability", "material"],
            "P007": ["pairing speed", "app interface", "voice recognition", "range"],
            "P008": ["zipper quality", "padding", "compartment space", "water resistance"],
            "P009": ["thermal cooling", "GPU performance", "screen finish", "speaker quality"],
            "P010": ["finish quality", "wood grain", "leg stability", "size"]
        }

        names = ["Alice T.", "Bob M.", "Charlie R.", "David W.", "Eve S.", "Frank K.", "Grace L.", "Henry J."]

        total_added = 0
        for product in products:
            # Add 3-5 reviews per product
            num_to_add = random.randint(3, 5)
            # Subtract existing if any (simplified)
            current_count = len(product.reviews)
            to_add = max(0, num_to_add - current_count)
            
            features = features_by_product.get(product.id, ["quality", "performance", "design"])

            for _ in range(to_add):
                template, rating = random.choice(review_templates)
                feature = random.choice(features)
                comment = template.format(feature=feature)
                
                review = ProductReview(
                    product_id=product.id,
                    customer_name=random.choice(names),
                    rating=rating,
                    comment=comment,
                    date=(datetime.now() - timedelta(days=random.randint(1, 100))).strftime("%Y-%m-%d")
                )
                db.add(review)
                total_added += 1

        db.commit()
        print(f"Successfully added {total_added} synthetic reviews.")

    finally:
        db.close()

if __name__ == "__main__":
    generate_synthetic_reviews()
