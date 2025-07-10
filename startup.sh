#!/bin/bash

echo "Running ShopVerse Dashboard"
streamlit run scripts/dashboard.py --server.port=$PORT --server.enableCORS=false

