MATERIAL_CLASSES = [
    "Cotton",    # 0
    "Polyester", # 1
    "Silk",      # 2
    "Denim",     # 3
    "Linen",     # 4
    "Wool",      # 5
    "Leather",   # 6
    "Velvet",    # 7
    "Corduroy",  # 8
    "Fleece",    # 9
    "Nylon",     # 10
    "Satin",     # 11
    "Knitted",   # 12
    "Suede",     # 13
]

TEXTILENET_TO_TARGET = {
    # FIBRES -> target class
    "cotton":            "Cotton",
    "polyester":         "Polyester",
    "silk":              "Silk",
    "wool":              "Wool",
    "cashmere":          "Wool",
    "alpaca":            "Wool",
    "mohair":            "Wool",
    "angora":            "Wool",
    "camel":             "Wool",
    "yak":               "Wool",
    "llama":             "Wool",
    "linen":             "Linen",
    "flax_linen":        "Linen",
    "ramie":             "Linen",
    "hemp":              "Linen",
    "nylon":             "Nylon",
    "elastane_spandex":  "Nylon",
    "polyolefin":        "Nylon",
    "aramid":            "Nylon",
    "fleece":            "Fleece",

    # Core target fabrics
    "denim":             "Denim",
    "velvet":            "Velvet",
    "corduroy":          "Corduroy",
    "satin":             "Satin",
    "knit":              "Knitted",
    "knitted":           "Knitted",
    "knitwear":          "Knitted",
    "leather":           "Leather",
    "suede":             "Suede",
    "fur":               "Fleece",

    # TextileNet folder names mapped into the 14-class contract
    "canvas":            "Cotton",
    "chambray":          "Cotton",
    "chenille":          "Velvet",
    "chiffon":           "Silk",
    "crepe":             "Silk",
    "faux_fur":          "Fleece",
    "faux_leather":      "Leather",
    "flannel":           "Wool",
    "gingham":           "Cotton",
    "jersey":            "Knitted",
    "lawn":              "Cotton",
    "neoprene":          "Nylon",
    "organza":           "Silk",
    "serge":             "Wool",
    "taffeta":           "Silk",
    "tulle":             "Nylon",
    "tweed":             "Wool",
    "twill":             "Cotton",
    "vinyl":             "Leather",

    # Alternate spellings / synonyms
    "woollen":           "Wool",
    "woolen":            "Wool",
    "polyester fabric":  "Polyester",
    "cotton fabric":     "Cotton",
    "silk fabric":       "Silk",
    "denim fabric":      "Denim",
    "nylon fabric":      "Nylon",
    "satin fabric":      "Satin",
}
