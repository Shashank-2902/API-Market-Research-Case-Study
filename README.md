# 📊 API Market Research: Data Collection and Database Handling

A student project exploring market dynamics of Arduino UNO components using API-based data collection, database management, and visualization tools.

## 🧠 Overview

This project was developed as part of the **"Intelligent Systems in Production"** case study under the supervision of **Prof. Tim Weber** at **Deggendorf Institute of Technology**.  
It demonstrates how to collect, store, and analyze component-level data—focusing on **price trends**, **availability**, and **sales volumes**—using:

- **Nexar API** (data collection)
- **SQLite** (data storage)
- **R programming** (data visualization)
- **Docker** (containerization for deployment)

## 🎯 Objective

To provide data-driven insights for suppliers, manufacturers, and consumers by tracking:

- 💰 Price trends
- 📦 Product availability
- 📈 Sales volumes

## 📦 Tech Stack

- **Python**: API integration and data parsing
- **Nexar API**: Real-time component-level data
- **SQLite**: Lightweight and structured storage of collected data
- **R**: Visualization and analysis
- **Docker**: Containerized environment setup

## 📌 Key Features

- ✅ Automated Arduino UNO component data extraction
- ✅ Structured database with `parts`, `price`, and `availability` tables
- ✅ Interactive visualizations (e.g., scatter plots, trend lines)
- ✅ Insights on vendor pricing strategies and availability dynamics
- ✅ Reproducible and portable via Docker

## 📊 Data Insights

- Time Range: **Jan 7–20, 2025**
- Highlighted Vendors: **Jameco**, **Mouser**, **id Electro**
- Findings:
  - Certain vendors maintain premium pricing with limited supply.
  - Availability increases rapidly post-Jan 13.
  - Most companies show consistent pricing behavior.

## 📁 Project Structure

```bash
├── db/                   # SQLite database: electronic_parts.db
├── scripts/              # Python and R scripts
├── Dockerfile            # Docker environment setup
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
