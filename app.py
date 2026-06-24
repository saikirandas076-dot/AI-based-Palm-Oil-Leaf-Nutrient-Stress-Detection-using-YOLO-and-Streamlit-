import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import gdown


# ---------------- MODEL DOWNLOAD ----------------

MODEL_PATH = "best.pt"

FILE_ID = "1G1nZ-6TPcdAHyIOyo6Mgvrsqsckx37i1"

if not os.path.exists(MODEL_PATH):
    gdown.download(
        id=FILE_ID,
        output=MODEL_PATH,
        quiet=False
    )


# Load YOLO model
model = YOLO(MODEL_PATH)

def add_bg(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image:
            linear-gradient(
                rgba(0,0,0,0.65),
                rgba(0,0,0,0.65)
            ),
            url("data:image/jpg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

add_bg("bg.jpg")


# ---------------- APP TITLE ----------------

st.title("🌴 Palm Oil Leaf Nutrient Stress Detection")

st.write(
    "Upload a palm oil leaf image to detect nutrient stress"
)


# ---------------- LANGUAGE ----------------

language = st.selectbox(
    "Select Language / భాష ఎంచుకోండి",
    [
        "English",
        "Telugu",
        "Hindi",
        "Tamil"
    ]
)


# ---------------- REMEDIES ----------------

remedies = {
    "boron": {
        "English": "Boron deficiency detected. Use Borax or Solubor fertilizer in recommended quantity. Consult a local agriculture officer before applying.",
        "Telugu": "బోరాన్ లోపం కనిపించింది. బోరాక్స్ లేదా సోలుబోర్ ఎరువును సిఫార్సు చేసిన మోతాదులో వాడండి. వాడే ముందు స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి.",
        "Hindi": "बोरॉन की कमी पाई गई है। Borax या Solubor खाद को recommended मात्रा में उपयोग करें। उपयोग से पहले कृषि अधिकारी से सलाह लें।",
        "Tamil": "போரான் குறைபாடு கண்டறியப்பட்டது. Borax அல்லது Solubor உரத்தை பரிந்துரைக்கப்பட்ட அளவில் பயன்படுத்தவும்."
    },
    "nitrogen": {
        "English": "Nitrogen deficiency detected. Use Urea or nitrogen-rich fertilizer in recommended quantity. Consult a local agriculture officer before applying.",
        "Telugu": "నైట్రోజన్ లోపం కనిపించింది. యూరియా లేదా నైట్రోజన్ అధికంగా ఉన్న ఎరువును సిఫార్సు చేసిన మోతాదులో వాడండి.",
        "Hindi": "नाइट्रोजन की कमी पाई गई है। Urea या nitrogen-rich fertilizer को recommended मात्रा में उपयोग करें।",
        "Tamil": "நைட்ரஜன் குறைபாடு கண்டறியப்பட்டது. Urea அல்லது nitrogen-rich உரத்தை பரிந்துரைக்கப்பட்ட அளவில் பயன்படுத்தவும்."
    },
    "magnesium": {
        "English": "Magnesium deficiency detected. Use Magnesium sulphate or Epsom salt in recommended quantity. Consult a local agriculture officer before applying.",
        "Telugu": "మెగ్నీషియం లోపం కనిపించింది. మెగ్నీషియం సల్ఫేట్ లేదా ఎప్సమ్ సాల్ట్‌ను సిఫార్సు చేసిన మోతాదులో వాడండి.",
        "Hindi": "मैग्नीशियम की कमी पाई गई है। Magnesium sulphate या Epsom salt को recommended मात्रा में उपयोग करें।",
        "Tamil": "மக்னீசியம் குறைபாடு கண்டறியப்பட்டது. Magnesium sulphate அல்லது Epsom salt பயன்படுத்தவும்."
    },
    "kalium": {
        "English": "Potassium deficiency detected. Use MOP or Potash fertilizer in recommended quantity. Consult a local agriculture officer before applying.",
        "Telugu": "పొటాషియం లోపం కనిపించింది. MOP లేదా పొటాష్ ఎరువును సిఫార్సు చేసిన మోతాదులో వాడండి.",
        "Hindi": "पोटैशियम की कमी पाई गई है। MOP या Potash fertilizer को recommended मात्रा में उपयोग करें।",
        "Tamil": "பொட்டாசியம் குறைபாடு கண்டறியப்பட்டது. MOP அல்லது Potash உரத்தை பயன்படுத்தவும்."
    },
    "healthy": {
        "English": "Leaf looks healthy. No medicine required. Continue regular monitoring.",
        "Telugu": "ఆకు ఆరోగ్యంగా ఉంది. మందు అవసరం లేదు. రెగ్యులర్‌గా గమనించండి.",
        "Hindi": "पत्ता स्वस्थ है। दवा की आवश्यकता नहीं है। नियमित निगरानी जारी रखें।",
        "Tamil": "இலை ஆரோக்கியமாக உள்ளது. மருந்து தேவையில்லை."
    }
}



# ---------------- IMAGE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Choose Palm Leaf Image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)



if uploaded_file is not None:


    # Open image
    image = Image.open(uploaded_file)


    # Prediction
    results = model(image)


    # Bounding box image
    detected_image = results[0].plot()



    # SIDE BY SIDE VIEW

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("Before 🌿")

        st.image(
            image,
            caption="Original Leaf",
            use_container_width=True
        )



    with col2:

        st.subheader("After 🤖")

        st.image(
            detected_image,
            caption="AI Detection Result",
            use_container_width=True
        )




    # ---------------- RESULT ----------------


    if len(results[0].boxes) > 0:


        for box in results[0].boxes:


            class_id = int(box.cls[0])

            confidence = float(box.conf[0])


            class_name = model.names[class_id]

            class_key = class_name.lower().strip()



            st.success(
                f"Detected Disease: {class_name}"
            )


            st.info(
                f"Confidence: {confidence*100:.2f}%"
            )


            st.subheader(
                "Recommended Solution 💊"
            )


            solution = remedies.get(
                class_key,
                {}
            ).get(
                language,
                "Solution not available"
            )


            st.write(solution)



    else:

        st.warning(
            "No nutrient stress detected"
        )

