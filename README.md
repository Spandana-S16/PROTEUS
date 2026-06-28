# PROTEUS

## Adaptive Supply Chain Intelligence through Context-Aware Hybrid Ensemble Forecasting

---

## Overview

Demand forecasting in modern supply chains is challenging because market behavior is inherently non-stationary. Demand patterns evolve due to seasonality, disruptions, economic changes, and operational uncertainty, making it difficult for any single forecasting model to consistently outperform across all scenarios.

PROTEUS addresses this challenge by combining statistical, machine learning, and deep learning models through a **learnable adaptive fusion mechanism**. Instead of assigning fixed weights to each forecasting model, PROTEUS employs a neural gating network that dynamically determines how much influence each model should have based on the current market context.

The system integrates **Prophet**, **XGBoost**, and **LSTM**, alongside a contextual gating network trained on volatility indicators, demand dynamics, operational signals, and seasonal information. This enables the ensemble to continuously adapt as market conditions change.

---

## Motivation

Traditional ensemble forecasting methods generally rely on manually selected or static weights. Although effective under stable conditions, these approaches fail to adapt when demand patterns shift.

Different forecasting models excel under different circumstances:

* **Prophet** captures long-term trends and recurring seasonal patterns.
* **XGBoost** models nonlinear relationships between engineered demand and operational features.
* **LSTM** learns temporal dependencies and sequential demand behavior.

Rather than assuming one model is always superior, PROTEUS learns **when each model should be trusted** using a context-aware gating mechanism.

---

## Core Idea

The central innovation of PROTEUS is its **Adaptive Fusion Network**.

The gating network receives two categories of information:

1. **Market Context**

   * Demand volatility
   * Demand growth
   * Demand momentum
   * Operational indicators
   * Seasonal information

2. **Individual Model Predictions**

   * Prophet forecast
   * XGBoost forecast
   * LSTM forecast

Based on these inputs, the network produces three normalized weights using a Softmax layer. These weights determine the contribution of each forecasting model to the final prediction.

Unlike conventional weighted averaging, the weights change dynamically according to the observed supply chain conditions.

---

## Why This Is More Than a Stacked Ensemble

Conventional stacked ensembles learn a mapping from model outputs to a final prediction.

PROTEUS extends this concept by incorporating **contextual market features** alongside model predictions. This allows the system to learn *why* a particular forecasting model should be favored under specific operating conditions.

For example:

* During stable periods, trend-based statistical forecasting receives greater importance.
* During demand disruptions, feature-driven models become more influential.
* During transitional market phases, the ensemble automatically balances all three models.

The fusion process is therefore conditioned on both prediction quality and environmental context.

---

## System Architecture

The forecasting pipeline consists of the following stages:

1. **Data Processing**

   * Weekly aggregation of DataCo supply chain transactions
   * Feature engineering
   * Temporal preprocessing

2. **Individual Forecasting Models**

   * Prophet
   * XGBoost
   * LSTM

3. **Adaptive Fusion**

   * Context-aware neural gating network
   * Dynamic model weighting
   * Final ensemble prediction

4. **Supply Chain Intelligence**

   * Stability analysis
   * Regime detection
   * Business recommendations
   * AI-generated executive report

5. **Interactive Dashboard**

   * Forecast visualization
   * Scenario simulation
   * Model contribution analysis
   * Supply chain health monitoring

---

## Dataset

The project uses the **DataCo Smart Supply Chain Dataset**, containing over **180,000 supply chain transactions** collected across **23 global regions**.

The raw transactional data is transformed into weekly regional demand series and enriched with engineered contextual features including:

* Weekly demand
* Rolling demand volatility
* Demand growth
* Demand momentum
* Shipping delay variation
* Profit variation
* Late delivery risk
* Holiday indicators
* Calendar features

Each region is divided using an **80:20 chronological train-test split** to preserve temporal consistency during evaluation.

---

## Forecasting Models

### Prophet

Prophet models long-term demand trends and seasonal behavior using additive time-series decomposition. Independent regional models capture localized demand characteristics while maintaining interpretability.

### XGBoost

Gradient Boosted Decision Trees are trained using engineered demand and operational features, enabling the model to capture complex nonlinear relationships and sudden market changes.

### LSTM

A multi-layer Long Short-Term Memory network models sequential demand behavior and temporal dependencies that traditional machine learning models cannot easily capture.

---

## Adaptive Gating Network

The gating network is implemented as a lightweight feed-forward neural network.

**Architecture**

* Input Layer (12 contextual features)
* Dense Layer (32 neurons, ReLU)
* Dropout (0.2)
* Dense Layer (16 neurons, ReLU)
* Output Layer (3 neurons, Softmax)

The network predicts three normalized weights corresponding to Prophet, XGBoost, and LSTM.

Training targets are generated using inverse forecasting error, allowing the network to learn which model performs best under different operating conditions.

KL-Divergence is used as the loss function because the target outputs represent probability distributions rather than independent regression values.

---

## Supply Chain Stability Analysis

Before generating forecasts, PROTEUS computes a **Supply Chain Stability Index (SCSI)** using four independent components:

* Demand Stability
* Economic Stability
* Trend Stability
* Seasonality Stability

The overall stability score is then used to classify the operating environment into one of four demand regimes:

* Stable
* Seasonal
* Transitional
* Disrupted

These regimes support business recommendations and provide additional contextual information for decision-making.

---

## Key Features

* Context-aware adaptive ensemble forecasting
* Dynamic neural model weighting
* Stability and regime analysis
* Interactive scenario simulation
* AI-generated executive reports
* Real-time forecasting dashboard
* Business recommendation engine

---

## Technology Stack

| Layer                   | Technology                  |
| ----------------------- | --------------------------- |
| Frontend                | React, Vite, Recharts       |
| Backend                 | Python, Flask               |
| Statistical Forecasting | Prophet                     |
| Machine Learning        | XGBoost                     |
| Deep Learning           | TensorFlow / Keras (LSTM)   |
| Adaptive Fusion         | Neural Gating Network       |
| Data Processing         | Pandas, NumPy, Scikit-learn |
| AI Reporting            | Google Gemini API           |

---

## Conclusion

PROTEUS demonstrates that adaptive, context-aware ensemble forecasting can outperform static fusion approaches in dynamic supply chain environments. By continuously adjusting model importance according to current operating conditions, the system provides more resilient forecasts while simultaneously generating interpretable business insights through stability analysis, regime detection, and AI-assisted decision support.
