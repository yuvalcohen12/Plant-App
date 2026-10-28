import os
import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def check_status():
    return {"status": "Server is running with AI!"}

@app.post("/identify")
async def identify_plant(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = """
            Analyze this image and identify the plant. 
            Return ONLY a valid JSON object with no additional text or markdown formatting.
            The JSON must have exactly these keys:
            - "name": The common name of the plant in Hebrew.
            - "water_in_days": An integer representing how often (in days) it usually needs to be watered.
            - "light": A short string describing light requirements in Hebrew (e.g., 'אור מלא', 'צל חלקי').
            - "toxicity": A short warning in Hebrew if toxic to pets, or 'בטוח לחיות מחמד' if safe.
            - "tip": One short, useful care tip in Hebrew.
            """
        
        image_part = {
            "mime_type": "image/jpeg", 
            "data": image_bytes
        }
        
        response = model.generate_content([prompt, image_part])
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        ai_data = json.loads(clean_text)
        
        return {
            "filename": image.filename,
            "message": "התמונה נותחה בהצלחה על ידי AI!",
            "identified_plant": ai_data
        }
        
    except Exception as e:
        return {
            "filename": image.filename,
            "message": f"שגיאה בזיהוי: {str(e)}",
            "identified_plant": {
                "name": "תקלה בזיהוי",
                "water_in_days": 0
            }
        }

@app.get("/api/search")
def search_plant(name: str):
    print(f"Received search request for: {name}")
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
            Provide botanical care information for the plant named '{name}'.
            Return ONLY a valid JSON object with no additional text or markdown formatting.
            The JSON must have exactly these keys:
            - "name": The common name of the plant in Hebrew.
            - "water_in_days": An integer representing how often (in days) it usually needs to be watered.
            - "light": A short string describing light requirements in Hebrew.
            - "toxicity": A short warning in Hebrew if toxic to pets, or 'בטוח לחיות מחמד' if safe.
            - "tip": One short, useful care tip in Hebrew.
            """
        
        print("Sending request to Gemini AI...")
        response = model.generate_content(prompt)
        print("Received response from Gemini!")
        
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        ai_data = json.loads(clean_text)
        
        return ai_data
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=404, detail="Plant not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
