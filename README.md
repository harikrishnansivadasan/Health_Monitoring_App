# 🏥 Health Monitoring App

This is a real-time health monitoring dashboard built with **Streamlit**, designed to visualize vital signs like heart rate, body temperature, and SpO₂ levels. The app can be run locally using Docker or accessed via a public EC2 IP (if deployed).

---

## 🚀 Features

- 📊 Live health metrics dashboard
- 📡 Real-time data simulation
- ✅ Risk classification alerts
- 🐳 Dockerized for easy deployment

---

## 🛠️ Local Setup with Docker

### 1. **Clone the Repository**

```bash
git clone https://github.com/harikrishnansivadasan/Health_Monitoring_App.git
cd Health_Monitoring_App
```

### 2. **Run Locally**

```bash
streamlit run app.py
```
### OR

### 2. **Build Docker Image**

```bash
docker build -t streamlit-app .
```

### 3. **Run the Docker Container**

```bash
docker run -p 8501:8501 streamlit-app
```

### 4. **Open the App in Browser**

Visit: [http://localhost:8501](http://localhost:8501)

---

## ☁️ Accessing the Deployed App (EC2)

If the app is deployed on AWS EC2 and publicly available, use the following:

- **URL Format:**

```
```
http://51.20.89.224:8501
```

> Make sure port `8501` is open in your EC2 instance’s security group.

---

## 📦 DockerHub Image

If you want to pull the prebuilt image directly from DockerHub:

```bash
docker pull harikrishnansivadas/streamlit-app
docker run -p 8501:8501 harikrishnansivadas/streamlit-app
```

---


## 📌 Requirements (if running without Docker)

- Python 3.8+
- Streamlit
- Pandas, Numpy
- scikit-learn (if model-based predictions used)

Install with:

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🤝 Author

**Harikrishnan S**  

---

## 📄 License

This project is licensed under the MIT License.
