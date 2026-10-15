from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import pymongo
import certifi
import numpy as np

app = FastAPI()

# Frontend permission (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. MONGODB CONNECTION
# ⚠️ APNI ASLI CONNECTION STRING YAHAN DETE WAQT PASSWORD SAHI DAALEIN
MONGO_URI = "mongodb+srv://kumarayshu852_db_user:Dic6Qf207uPHDDWY@mvuwewh.mongodb.net/?retryWrites=true&w=majority&authSource=admin"

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

# Database aur Collection (Table) banana
db = client["AI_Database"]
collection = db["tables_memory"]

@app.get("/get-table/{number}")
def get_table(number: int):
    target_key = str(number)
    
    # 2. DATABASE SE FETCH (REPLY) KARNA 🔍
    # Check karna kya ye number database mein pehle se save hai?
    existing_memory = collection.find_one({"number_key": target_key})
    
    if existing_memory:
        weight = existing_memory["weight"]
        status = "🧠 It was remembered! Loaded from the database."
    else:
        # 3. AGAR NAYA HAI TOH ZERO SE TRAIN KARNA 🔥
        status = "❌ I didn't remember. I learned something new in MongoDB and saved it!"
        
        weight = 0.0  
        learning_rate = 0.01  
        inputs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        true_outputs = inputs * number  

        for epoch in range(500):  
            predictions = inputs * weight
            error = true_outputs - predictions
            weight_adjustment = learning_rate * np.mean(error * inputs)
            weight += weight_adjustment

        final_weight = float(round(weight, 2))
        
        # 4. DATABASE MEIN SAVE KARNA 💾
        # Nayi seekhi hui baat ko MongoDB mein insert kar dena
        collection.insert_one({
            "number_key": target_key,
            "weight": final_weight
        })
        weight = final_weight

    # Table ka array banana
    table_data = []
    for i in range(1, 11):
        table_data.append(f"{number} x {i} = {round(i * weight)}")
        
    return {"status": status, "table": table_data}
