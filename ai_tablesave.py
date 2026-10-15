import numpy as np
import time
import json
import os

print("--- SMART AI TABLE GENERATOR (WITH MEMORY) ---")

MEMORY_FILE = "ai_memory.json"

# 1. Puraani Memory Load Karna (Agar file bani hui hai)
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, 'r') as f:
        ai_memory = json.load(f)
else:
    ai_memory = {} # Shuruat mein memory khaali hai

# User se number mangna
target_number = int(input("Aap kis number ka table generate karna chahte hain?: "))
target_key = str(target_number)

# 2. Check karna: Kya AI ke paas ye number pehle se yaad hai?
if target_key in ai_memory:
    print(f"\n🧠 AI ko yaad hai! Purani memory se weight load ho raha hai...")
    weight = ai_memory[target_key]
    time.sleep(1) # Chota sa suspense
else:
    # Agar naya number hai, toh AI use zero se seekhega
    print(f"\n❌ AI ko ye number yaad nahi hai. Zero se training shuru ho rahi hai...")
    time.sleep(1)
    
    weight = 0.0  
    learning_rate = 0.01  
    inputs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    true_outputs = inputs * target_number  

    # Training Loop
    for epoch in range(500):  
        predictions = inputs * weight
        error = true_outputs - predictions
        weight_adjustment = learning_rate * np.mean(error * inputs)
        weight += weight_adjustment
        
        if epoch % 100 == 0:
            loss = np.mean(error ** 2)
            print(f"Attempt {epoch}: Galti (Loss) = {loss:.4f}, Weight = {weight:.2f}")

    print("\n🎉 Training Poori Hui! AI ne naya number seekh liya hai.")
    
    # Nayi seekhi hui baat ko memory memory mein jodna aur file mein save karna
    ai_memory[target_key] = float(round(weight, 2))
    with open(MEMORY_FILE, 'w') as f:
        json.dump(ai_memory, f)
    print("💾 Nayi memory computer ki hard disk mein save ho gayi hai!")

# 3. Final Table Output (Trained Weight ke dum par)
print(f"\n--- AI Generated Table for {target_number} ---")
for i in range(1, 11):
    ai_answer = round(i * weight)
    print(f"{target_number} x {i} = {ai_answer}")
