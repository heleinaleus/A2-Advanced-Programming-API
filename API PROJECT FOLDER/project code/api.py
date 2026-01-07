"""
**********************************************

    DATA DRIVEN APPLICATION ASSESSMENT 2
         The Cocktail Database

**********************************************
"""

from tkinter import *
import tkinter as tk
import requests
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from io import BytesIO


# make the main app window

window = tk.Tk()
window.title("Cocktail Database")
window.geometry("750x470+300+200")
window.resizable(False, False)
window.config(bg="#2b2c2b")

# closes the window

def on_close():
    window.destroy()

# define a callback function, deletes palceholder text
def delete_placeholder(event):
    if textfield.get() == "Search for cocktails here":
        textfield.delete(0, "end")
        
        
"""
**********************************************

    API INTERACTION FUNCTIONS

**********************************************
"""

# functions to get a random cocktail from the API

def get_random_cocktail():
    # make a get request to the API
    response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/random.php") 
    
    # get the JSON data from the response
    data = response.json()
    
    # get cocktail info from the data
    if "drinks" in data:
        cocktail = data["drinks"][0]
    else:
        return None, None, None, None, None
    
    if "strDrink" in cocktail:
        name = cocktail["strDrink"]
    else:
        name = ""
        
    ingredients = []
    measures = []
    
    # get ingredients and measures for the cocktail
    for i in range(1, 16):
        ingredient = cocktail.get(f"strIngredient{i}")
        measure = cocktail.get(f"strMeasure{i}")
        if ingredient and measure:
            ingredients.append(ingredient)
            measures.append(measure)
    
    # 
    image_url = cocktail.get("strDrinkThumb", "")
    recipe = cocktail.get("strInstructions", "")
    return name, image_url, ingredients, measures, recipe

# functions to update cocktail info
    
def update_cocktail():
    name, image_url, ingredients, measures, recipe = get_random_cocktail()
    
    if name:
        name_label.config(text=name)
        if image_url:
            try:
                # gets picture from web and make it fit
                image_data = requests.get(image_url).content
                image = Image.open(BytesIO(image_data))
                image = image.resize((200, 200), Image.LANCZOS)  
                photo = ImageTk.PhotoImage(image)
                image_label.config(image=photo)
                image_label.image = photo
                
            except Exception as e:
                print(f"Error loading image: {e}")
                image_label.config(image="")
        ingredients_list = ", ".join([f"{m} {i}" for m, i in zip(measures, ingredients) if m and i])
        ingredients_label.config(text=ingredients_list)
        
        if len(recipe) < 300:
            recipe_label.config(text=recipe)
        else:
            recipe_label.config(text="Recipe not Found")  
    else:
        name_label.config(text="No cocktail found.")
        ingredients_label.config(text="")
        recipe_label.config(text="")
        image_label.config(image="")

# functions to search cocktails and shows it

def search_cocktails(name):
    api_url = "https://www.thecocktaildb.com/api/json/v1/1/search.php"
    params = {"s": name}
    
    response = requests.get(api_url, params=params)
    

    if response.status_code == 200:
        data = response.json()
        return data.get("drinks", [])
    return []

# functions to handle searching for cocktails

def search():
    name = textfield.get()
    cocktails = search_cocktails(name)
    
    if cocktails:
        
        cocktail = cocktails[0]
        name_label.config(text=cocktail["strDrink"])
        
        if len(cocktail.get("strInstructions", "")) < 300:
            recipe_label.config(text=cocktail["strInstructions"])
        else:
            recipe_label.config(text="Recipe not Found")
        # gets list of ingredients
        ingredients = [cocktail.get(f"strIngredient{i}", "") for i in range(1, 16) if cocktail.get(f"strIngredient{i}")]
        ingredients_text = ", ".join(ingredients)
        ingredients_label.config(text=ingredients_text)
        
        if cocktail.get("strDrinkThumb"):
            try:
                # get and show picture
                response = requests.get(cocktail["strDrinkThumb"])
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    image = image.resize((200, 200), Image.LANCZOS)  
                    photo = ImageTk.PhotoImage(image)
                    image_label.config(image=photo)
                    image_label.image = photo
                else:
                    image_label.config(image="")
            except Exception as e:
                print(f"Error loading image: {e}")
                image_label.config(image="")
    else:
        name_label.config(text="Cocktail not found.")
        ingredients_label.config(text="")
        image_label.config(image="")
        recipe_label.config(text="")
        
"""
**********************************************

    DESIGN

**********************************************
"""

# title

head1 = Label(window, text="Cocktail Finder", fg="#decc46", bg="#2b2c2b", font=('Papyrus', 30, 'bold'))
head1.place(x=15, y=20)

# set the app's icon

image_icon=PhotoImage(file="logo icon.png")
window.iconphoto(False,image_icon)

# search box
search_image = PhotoImage(file="rounded rectangle.png")
myimage = Label(window, image=search_image, bg="#2b2c2b")
myimage.place(x=15, y=117)

textfield = tk.Entry(window, justify="left", width=23, font=("poppins", 18, "bold"), bg="#ffffff", border=0, fg="black")
textfield.place(x=30, y=130)

search_icon = PhotoImage(file="search icon.png")
myimage_icon = Button(window, image=search_icon, borderwidth=0, cursor="hand2", bg="#ffffff", command=search)  
myimage_icon.place(x=330, y=127)

# bottom box
frame = Frame(window, width=900, height=180, bg="#4c4c4c")
frame.pack(side=BOTTOM)

# boxes
ingredientbox = PhotoImage(file="rounded rectangle 2.png")
recipebox = PhotoImage(file="rounded rectangle 2 copy.png")

Label(frame, image=ingredientbox, bg="#4c4c4c").place(x=20, y=45)
Label(frame, image=recipebox, bg="#4c4c4c").place(x=270, y=45)

# labels for the sections

head2 = Label(window, text="Ingredients", fg="#decc46", bg="#4c4c4c", font=('Papyrus', 18,))
head2.place(x=67, y=295)

head3 = Label(window, text="Recipe", fg="#decc46", bg="#4c4c4c", font=('Papyrus', 18,))
head3.place(x=340, y=295)

# shows the cocktail's name

name_label = Label(window, text="", fg="#ffffff", bg="#2b2c2b", font=("poppins", 12, "bold"))
name_label.place(x=510, y=40)

# shows the cocktail's picture

image_label = Label(window, bg="#2b2c2c")
image_label.place(x=480, y=70)

# shows the ingredients

ingredients_label = Label(window, justify="left", text="", fg="#ffffff", bg="#4c4c4c", font=("poppins", 10), wraplength=200)
ingredients_label.place(x=30, y=350)

# shows recipe

recipe_label = Label(window,justify="left", text="", fg="#ffffff", bg="#4c4c4c", font=("poppins", 10), wraplength=200)
recipe_label.place(x=280, y=350)

# random cocktail button

random_button = Button(window, width=20, text="Random Cocktail", command=update_cocktail, bg="#942727", fg="#ffffff", font=("poppins", 12))
random_button.place(x=530, y=360, height=70)

"""
**********************************************

    MAIN LOOP

**********************************************
"""

window.mainloop()