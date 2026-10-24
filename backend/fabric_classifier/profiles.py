"""Human-readable fabric knowledge profiles shown by the web UI (no heavy imports)."""

# Comprehensive fabric textile knowledge profiles
FABRIC_PROFILES = {
    "Cotton": {
        "category": "Natural Plant Fiber (Cellulose)",
        "tagline": "Breathable, soft, and naturally hypoallergenic everyday staple",
        "description": "Cotton is one of the world's most widely used natural fibers, renowned for its soft hand feel, high absorbency, and exceptional breathability across diverse climates.",
        "properties": {
            "breathability": "High",
            "durability": "Medium-High",
            "stretch": "Low (without elastane)",
            "texture": "Soft, natural matte"
        },
        "care": {
            "washing": "Machine wash warm or cold with like colors",
            "drying": "Tumble dry medium or line dry to minimize shrinkage",
            "ironing": "Warm to hot iron while slightly damp"
        },
        "uses": ["T-shirts", "Button-down shirts", "Bedding", "Denim blends", "Summer apparel"]
    },
    "Polyester": {
        "category": "Synthetic Polymer",
        "tagline": "Durable, wrinkle-resistant, and high-performance synthetic",
        "description": "Polyester is an extremely durable synthetic fabric that resists wrinkling, shrinking, and abrasion. It offers rapid drying and maintains its shape well under active conditions.",
        "properties": {
            "breathability": "Moderate",
            "durability": "Very High",
            "stretch": "Moderate recovery",
            "texture": "Smooth, lightweight"
        },
        "care": {
            "washing": "Machine wash warm with mild detergent",
            "drying": "Tumble dry low or air dry (dries rapidly)",
            "ironing": "Cool iron; avoid high heat to prevent fiber melting"
        },
        "uses": ["Sportswear", "Outerwear", "Lining", "Blended fabrics", "Suits"]
    },
    "Silk": {
        "category": "Natural Protein Fiber",
        "tagline": "Luxurious natural fiber with brilliant sheen and fluid drape",
        "description": "Harvested from silkworm cocoons, silk has a triangular prism fiber structure that refracts light naturally, yielding its legendary lustrous luster and fluid, temperature-regulating drape.",
        "properties": {
            "breathability": "High",
            "durability": "Medium (delicate when wet)",
            "stretch": "Low",
            "texture": "Ultra-smooth, luxurious sheen"
        },
        "care": {
            "washing": "Hand wash cold with silk detergent or dry clean",
            "drying": "Dry flat on towel away from direct sunlight",
            "ironing": "Low iron with a pressing cloth while slightly damp"
        },
        "uses": ["Evening gowns", "Silk scarves", "Blouses", "Ties", "Luxury bedding"]
    },
    "Denim": {
        "category": "Heavy Cotton Twill",
        "tagline": "Iconic diagonal twill weave engineered for rugged endurance",
        "description": "Denim is a sturdy warp-faced cotton twill woven with indigo warp yarns and white weft yarns. It develops character, fading, and softening uniquely with each wear.",
        "properties": {
            "breathability": "Medium",
            "durability": "Exceptional",
            "stretch": "Rigid (or slight comfort stretch)",
            "texture": "Sturdy, textured diagonal twill"
        },
        "care": {
            "washing": "Turn inside-out, wash in cold water to prevent fading",
            "drying": "Hang or line dry to preserve fabric structure",
            "ironing": "Medium-high iron if needed"
        },
        "uses": ["Jeans", "Denim jackets", "Overalls", "Heavy duty shirts", "Tote bags"]
    },
    "Linen": {
        "category": "Natural Flax Fiber",
        "tagline": "Crisp, ultra-breathable ancient fiber that softens with age",
        "description": "Spun from flax plant stems, linen has natural hollow fibers that provide supreme airflow and rapid moisture dissipation, marked by distinctive natural slub texture.",
        "properties": {
            "breathability": "Maximum",
            "durability": "High (stronger when wet)",
            "stretch": "Minimal",
            "texture": "Crisp slub weave, softens beautifully over time"
        },
        "care": {
            "washing": "Gentle cycle cold or warm water",
            "drying": "Line dry or gentle low tumble",
            "ironing": "Iron while damp with high steam"
        },
        "uses": ["Summer suits", "Breezy shirts", "Resort wear", "Trousers", "Curtains"]
    },
    "Wool": {
        "category": "Natural Animal Fiber (Protein)",
        "tagline": "Warm, resilient, moisture-wicking natural thermo-regulator",
        "description": "Wool fibers feature microscopic scales and natural crimp that trap insulating air pockets, keeping wearers warm in winter while repelling moisture and resisting odors.",
        "properties": {
            "breathability": "High",
            "durability": "High",
            "stretch": "High natural elasticity",
            "texture": "Warm, fibrous, resilient"
        },
        "care": {
            "washing": "Hand wash cold with wool-safe wash, or professional dry clean",
            "drying": "Reshape and lay flat on a dry towel",
            "ironing": "Steam on wool setting with pressing cloth"
        },
        "uses": ["Knit sweaters", "Tailored suits", "Winter overcoats", "Scarves", "Blankets"]
    },
    "Leather": {
        "category": "Tanned Natural Hide / Alternative",
        "tagline": "Supple, wind-resistant material that develops a rich patina",
        "description": "Tanned animal hide or premium vegan alternative featuring tight fiber grain that blocks wind, resists abrasion, and patinas handsomely over years of use.",
        "properties": {
            "breathability": "Low-Moderate",
            "durability": "Exceptional",
            "stretch": "Yields gradually to shape",
            "texture": "Supple, smooth or pebbled grain"
        },
        "care": {
            "washing": "Do not submerge; wipe with damp microfiber cloth",
            "drying": "Air dry naturally away from radiators or heat",
            "ironing": "Do not iron directly; condition periodically"
        },
        "uses": ["Biker & bomber jackets", "Boots & footwear", "Belts & bags", "Gloves"]
    },
    "Velvet": {
        "category": "Woven Tufted Pile Fabric",
        "tagline": "Plush, opulent cut-pile weave with rich visual depth",
        "description": "Woven on a specialized loom that weaves two thicknesses simultaneously, velvet is then sliced to produce its dense, plush surface pile with rich optical highlights.",
        "properties": {
            "breathability": "Moderate",
            "durability": "Medium",
            "stretch": "Low to medium",
            "texture": "Plush, velvety soft, directional pile"
        },
        "care": {
            "washing": "Professional dry clean recommended",
            "drying": "Never wring or squeeze",
            "ironing": "Steam only; never press directly onto the pile"
        },
        "uses": ["Evening wear", "Dinner jackets", "Formal dresses", "Luxury upholstery"]
    },
    "Corduroy": {
        "category": "Cut-Pile Ribbed Cotton Blend",
        "tagline": "Tactile parallel cord ridges offering vintage warmth and style",
        "description": "A durable ribbed fabric featuring tufted cords (wales) running longitudinally. It blends the softness of velvet with the everyday resilience of heavy cotton twill.",
        "properties": {
            "breathability": "Medium",
            "durability": "High",
            "stretch": "Low",
            "texture": "Distinctive parallel ribbed wales"
        },
        "care": {
            "washing": "Turn inside-out, wash cold on gentle",
            "drying": "Tumble dry low or line dry to keep wales fluffy",
            "ironing": "Iron inside out with steam"
        },
        "uses": ["Corduroy trousers", "Overshirts", "Jackets", "Caps", "Vintage casual wear"]
    },
    "Fleece": {
        "category": "Brushed High-Loft Knit",
        "tagline": "Ultra-lightweight, fluffy thermal knit for maximum coziness",
        "description": "Constructed from knitted synthetic or blended yarn brushed on both faces to create a deep, insulating pile that retains body heat while remaining featherlight.",
        "properties": {
            "breathability": "High",
            "durability": "High",
            "stretch": "Moderate",
            "texture": "Fluffy, brushed, cozy"
        },
        "care": {
            "washing": "Machine wash cold with mild detergent",
            "drying": "Air dry or tumble dry low (avoids pilling)",
            "ironing": "Do not iron"
        },
        "uses": ["Zip hoodies", "Outdoor fleeces", "Thermal mid-layers", "Winter blankets"]
    },
    "Nylon": {
        "category": "Synthetic Polyamide",
        "tagline": "High-tensile, abrasion-proof synthetic engineered for endurance",
        "description": "A legendary thermoplastic polymer known for exceptional tensile strength, elasticity, water resistance, and resistance to mildew and tearing.",
        "properties": {
            "breathability": "Low-Moderate (unless vented)",
            "durability": "Extremely High",
            "stretch": "High elasticity",
            "texture": "Sleek, smooth, crisp"
        },
        "care": {
            "washing": "Machine wash cool on gentle cycle",
            "drying": "Line dry or tumble dry low",
            "ironing": "Cool iron; high heat can melt fibers"
        },
        "uses": ["Windbreakers", "Raincoats", "Activewear", "Backpacks", "Tights & hosiery"]
    },
    "Satin": {
        "category": "Glossy Filament Weave",
        "tagline": "Glossy, fluid fabric characterized by luminous surface luster",
        "description": "Formed through a satin weave where four or more weft threads float over warp threads, creating an ultra-smooth, light-catching surface with minimal friction.",
        "properties": {
            "breathability": "Medium",
            "durability": "Medium",
            "stretch": "Low",
            "texture": "Silky smooth, high gloss sheen"
        },
        "care": {
            "washing": "Hand wash cold or gentle machine cycle in mesh bag",
            "drying": "Air dry flat away from direct heat",
            "ironing": "Low iron inside out with steam"
        },
        "uses": ["Bridal gowns", "Lingerie", "Cocktail dresses", "Jacket lining", "Hair bonnets"]
    },
    "Knitted": {
        "category": "Interlooped Yarn Structure",
        "tagline": "Stretchy, adaptive textile with forgiving body-contouring drape",
        "description": "Fabric constructed by interlacing continuous loops of yarn. Knitted structures offer multidirectional stretch, breathability, and exceptional everyday comfort.",
        "properties": {
            "breathability": "High",
            "durability": "Medium-High",
            "stretch": "High multidirectional stretch",
            "texture": "Looped, soft, flexible"
        },
        "care": {
            "washing": "Gentle wash cold with similar colors",
            "drying": "Lay flat to dry to prevent distortion and stretching",
            "ironing": "Steam gently or iron on low"
        },
        "uses": ["Jersey tops", "Cardigans", "Polo shirts", "Sportswear", "Socks"]
    },
    "Suede": {
        "category": "Napped Leather / Microfiber",
        "tagline": "Velvety textured napped finish with understated matte elegance",
        "description": "Created from the underside of leather or advanced micro-denier fibers, suede has a soft brushed nap that absorbs light, creating a rich, matte tactile appearance.",
        "properties": {
            "breathability": "Moderate",
            "durability": "Medium-High",
            "stretch": "Low",
            "texture": "Soft napped velvety texture"
        },
        "care": {
            "washing": "Do not use water; clean with dedicated suede brush and eraser",
            "drying": "Keep dry; apply waterproof suede protector spray",
            "ironing": "Do not iron"
        },
        "uses": ["Suede jackets", "Chelsea boots", "Handbags", "Overshirts", "Trims"]
    }
}
