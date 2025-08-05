import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
from src.logger import logging
import os
import sys
from src.pipeline.predict_pipeline import PredictionPipeline
from src.exception import CustomException

# # Configure logging
# LOG_FILE = "logs/dashboard.log"
# os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
# logging.basicConfig(
#     filename=LOG_FILE,
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

st.set_page_config(page_title="Chronic Care Health Monitor", layout="wide")
st.title("🩺 Real-Time Chronic Health Monitoring Dashboard")

if "running" not in st.session_state:
    st.session_state.running = False

# Toggle button
if st.button(
    "▶️ Start Monitoring" if not st.session_state.running else "⏹️ Stop Monitoring"
):
    st.session_state.running = not st.session_state.running
    if st.session_state.running:
        logging.info("Monitoring started by user.")
    else:
        logging.info("Monitoring stopped by user.")


try:
    # Load test data
    test_data = pd.read_csv("artifacts/test.csv")
    predictor = PredictionPipeline()
    logging.info("Test data and prediction pipeline loaded successfully.")

    # Streamlit placeholders
    col1, col2 = st.columns(2)
    bp_chart = col1.empty()
    sugar_chart = col2.empty()

    col3, col4 = st.columns(2)
    metrics_box = col3.empty()
    alert_box = col4.empty()

    # Real-time simulation
    i = 0
    while st.session_state.running == True and i < len(test_data):
        try:
            row = test_data.iloc[[i]].drop(
                columns=["Condition_Worsening"], errors="ignore"
            )
            input_data = row.copy()

            # Prediction
            prediction = predictor.predict(input_data)[0]
            logging.info(f"Prediction for row {i}: {prediction}")

            # Blood Pressure Chart
            # bp_fig = go.Figure()
            # bp_fig.add_trace(
            #     go.Bar(
            #         name="Systolic",
            #         x=["BP"],
            #         y=[row["Systolic Blood Pressure"].values[0]],
            #     )
            # )
            # bp_fig.add_trace(
            #     go.Bar(
            #         name="Diastolic",
            #         x=["BP"],
            #         y=[row["Diastolic Blood Pressure"].values[0]],
            #     )
            # )
            # bp_fig.update_layout(title="Blood Pressure", barmode="group")
            # bp_chart.plotly_chart(bp_fig, use_container_width=True)
            # Blood Pressure Gauges (Systolic & Diastolic)

            bp_fig = go.Figure()

            bp_fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=row["Systolic Blood Pressure"].values[0],
                    domain={"x": [0, 0.5], "y": [0, 1]},
                    title={"text": "Systolic (mmHg)"},
                    gauge={
                        "axis": {"range": [80, 200]},
                        "bar": {"color": "darkred"},
                        "steps": [
                            {"range": [80, 120], "color": "lightgreen"},
                            {"range": [120, 140], "color": "yellow"},
                            {"range": [140, 200], "color": "red"},
                        ],
                    },
                )
            )

            bp_fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=row["Diastolic Blood Pressure"].values[0],
                    domain={"x": [0.5, 1], "y": [0, 1]},
                    title={"text": "Diastolic (mmHg)"},
                    gauge={
                        "axis": {"range": [50, 130]},
                        "bar": {"color": "darkblue"},
                        "steps": [
                            {"range": [50, 80], "color": "lightgreen"},
                            {"range": [80, 90], "color": "yellow"},
                            {"range": [90, 130], "color": "red"},
                        ],
                    },
                )
            )

            bp_fig.update_layout(title="Blood Pressure Monitor (Systolic & Diastolic)")
            bp_chart.plotly_chart(bp_fig, use_container_width=True, key=f"systolic_{i}")

            # Blood Sugar Level Gauge
            sugar_fig = go.Figure()
            sugar_fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=row["Blood Glucose Level(BGL)"].values[0],
                    title={"text": "Blood Glucose Level (mg/dL)"},
                    gauge={"axis": {"range": [0, 400]}},
                )
            )
            sugar_chart.plotly_chart(
                sugar_fig, use_container_width=True, key=f"sugar_{i}"
            )

            # Vitals Metrics
            # with metrics_box.container():
            #     st.metric("Heart Rate (bpm)", row["Heart Rate"].values[0])
            #     st.metric("Body Temperature (°C)", row["Body Temperature"].values[0])
            #     st.metric("SpO2 (%)", row["SPO2"].values[0])

            with metrics_box.container():
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(
                        """
                        <div style="background-color:#f0f2f6;padding:20px;border-radius:10px;text-align:center;">
                            <h4 style="margin-bottom:10px;color:black;">❤️ Heart Rate</h4>
                            <h2 style="color:#dc3545;">{:.2f} bpm</h2>
                        </div>
                    """.format(
                            row["Heart Rate"].values[0]
                        ),
                        unsafe_allow_html=True,
                    )

                with col2:
                    st.markdown(
                        """
                        <div style="background-color:#f0f2f6;padding:20px;border-radius:10px;text-align:center;">
                            <h4 style="margin-bottom:10px;color:black;">🌡️ Temperature</h4>
                            <h2 style="color:#ff9900;">{:.2f} °C</h2>
                        </div>
                    """.format(
                            row["Body Temperature"].values[0]
                        ),
                        unsafe_allow_html=True,
                    )

                with col3:
                    st.markdown(
                        """
                        <div style="background-color:#f0f2f6;padding:20px;border-radius:10px;text-align:center;">
                            <h4 style="margin-bottom:10px;color:black;">🫁 SpO₂</h4>
                            <h2 style="color:#007bff;">{:.2f} %</h2>
                        </div>
                    """.format(
                            row["SPO2"].values[0]
                        ),
                        unsafe_allow_html=True,
                    )

            # Risk Alert
            if prediction == 1:
                alert_box.error("⚠️ Health Risk Detected: Condition Likely to Worsen")
            else:
                alert_box.success("✅ Stable Condition")

            time.sleep(1.7)
            i += 1

        except Exception as inner_e:
            logging.error(f"Error in row {i} prediction: {inner_e}")
            alert_box.warning("⚠️ Error processing this record. Check logs.")
            continue

except Exception as e:
    st.error("🚨 Failed to initialize dashboard. See logs for details.")
    logging.critical(f"Dashboard initialization failed: {e}")
    raise CustomException(e, sys)
