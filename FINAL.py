import tkinter as tk
import os
import base64
import openai
import requests

openai.api_key = "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"
prs=''
root = tk.Tk()
root.title("Real Estate Price Predictor")
root.geometry("1980x1080")

label = tk.Label(root, text="CONSTRUCTIONS FOR DOMESTIVE HOUSE PLANS ", width=90, fg='black', bg='white', font=('times', 20, 'bold'))
label1 = tk.Label(root, text='COST PREDICTIONS', padx=25, pady=25, fg='black', bg='white', font=('times', 20, 'bold'), width=45)
label2 = tk.Label(root, text='IMAGE PREDICTIONS', padx=25, pady=25, fg='black', bg='white', font=('times', 20, 'bold'), width=45)

label.grid(columnspan=2, row=0)
label1.grid(column=0, row=1)
label2.grid(column=1, row=1)

import pickle

def predict_price():
    global prs
    area_value = float(area.get())
    bedrooms_value = int(bedrooms.get())
    bathrooms_value = int(bathrooms.get())
    stories_value = int(stories.get())
    mainroad_value = 1 if mainroad.get().lower() == 'yes' else 0
    guestroom_value = 1 if guestroom.get().lower() == 'yes' else 0
    basement_value = 1 if basement.get().lower() == 'yes' else 0
    parking_value = int(parking.get())

    with open('model_pickle', 'rb') as f:
        rg = pickle.load(f)

    features = [area_value, bedrooms_value, bathrooms_value, stories_value, mainroad_value, guestroom_value, basement_value, parking_value]

    for i in features:
        prs += str(i) + ' '

    price = rg.predict([features])

    def generate_image(prompt, n=1, size="256x256"):
        try:
            response = openai.Image.create(prompt=prompt, n=n, size=size)
            return response.get('data')
        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    predicted_price.set(f"Predicted Price: ${price[0]}")
    prompt = 'generate a floor plan with these features {} without any text in it'.format(prs)

   
    images = generate_image(prompt)

   
    if images:
        for i, image in enumerate(images):
            try:
                image_url = image.get('url')
                if image_url:
                   
                    image_data = requests.get(image_url).content
                else:
                    image_data = base64.b64decode(image.get('b64_encoded_data'))  

               
                filename = f"generated_image_{i+1}.png"
                with open(filename, "wb") as f:
                    f.write(image_data)
                print(f"Saved image: {filename}")

                
                image = tk.PhotoImage(file=filename)
                image_label = tk.Label(root, image=image)
                image_label.image = image
                image_label.grid(column=0, rowspan=9, columnspan=2)

            except Exception as e:
                print(f"Error generating/saving image {i+1}: {e}")

    else:
        print("An error occurred during image generation. Please check your API key or prompt.")


area = tk.StringVar()
bedrooms = tk.StringVar()
bathrooms = tk.StringVar()
stories = tk.StringVar()
mainroad = tk.StringVar()
guestroom = tk.StringVar()
basement = tk.StringVar()
parking = tk.StringVar()
predicted_price = tk.StringVar()

tk.Label(root, text="Area",fg='white', bg='grey',width=100, font=('times', 10, 'bold')).grid(row=2, column=0,sticky='e')
tk.Entry(root, textvariable=area,width=100).grid(row=2, column=1,sticky='w')

tk.Label(root, text="Bedrooms",fg='white',width=100, bg='grey', font=('times', 10, 'bold')).grid(row=3, column=0,sticky='e')
tk.Entry(root, textvariable=bedrooms,width=100).grid(row=3, column=1,sticky='w')

tk.Label(root, text="Bathrooms",fg='white',width=100, bg='grey', font=('times', 10, 'bold')).grid(row=4, column=0,sticky='e')
tk.Entry(root, textvariable=bathrooms,width=100).grid(row=4, column=1,sticky='w')

tk.Label(root, text="Stories",fg='white',width=100, bg='grey', font=('times', 10, 'bold')).grid(row=5, column=0,sticky='e')
tk.Entry(root, textvariable=stories,width=100).grid(row=5, column=1,sticky='w')

tk.Label(root, text="Main Road",fg='white',width=100, bg='grey', font=('times', 10, 'bold')).grid(row=6, column=0,sticky='e')
tk.Entry(root, textvariable=mainroad,width=100).grid(row=6, column=1,sticky='w')

tk.Label(root, text="Guest Room",fg='white',width=100, bg='grey', font=('times', 10, 'bold')).grid(row=7, column=0,sticky='e')
tk.Entry(root, textvariable=guestroom,width=100).grid(row=7, column=1,sticky='w')

tk.Label(root, text="Basement",fg='white',width=100, bg='grey', font=('times', 10, 'bold')).grid(row=8, column=0,sticky='e')
tk.Entry(root, textvariable=basement,width=100).grid(row=8, column=1,sticky='w')

tk.Label(root, text="Parking",fg='white',width=100, bg='grey', font=('times', 10, 'bold')).grid(row=9, column=0,sticky='e')
tk.Entry(root, textvariable=parking,width=100).grid(row=9, column=1,sticky='w')

tk.Button(root, text="Predict",fg='white',width=100, bg='black', font=('times', 10, 'bold'), command=predict_price).grid(row=10, column=0, columnspan=2)

tk.Label(root, textvariable=predicted_price).grid(row=11, column=0)

root.mainloop()

