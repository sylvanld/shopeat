OPENAPI_TITLE = "ShopEat API"
OPENAPI_DESCRIPTION = """
Shopeat is an application that helps you plan the recipes you want to cook,
create shopping lists, and do online shopping with your friends or family.

It allows you to easily plan your meals and save time and money by organizing your shopping in an efficient way. 
You can use the app to choose recipes based on your preferences and dietary needs, and then generate a shopping list 
based on the required ingredients. You can also invite your friends or family to join and contribute to the shopping list,
which can be convenient when organizing shared meals or when you want to share the shopping tasks.
""".strip()
OPENAPI_VERSION = "v1"
OPENAPI_TAGS = [
    {
        "name": "Accounts",
        "description": "Endpoints to create and manage accounts, and get access tokens.",
    },
    {
        "name": "Groups",
        "description": "Manage groups of users who shares the same table and may do shopping together.",
    },
    {
        "name": "Ingredients",
        "description": "Manage ingredients and ingredients' shelves.",
    }
]
