#!/bin/bash

# Run Python script with arguments
python3 inference_privacy_policy.py \
    --url="https://www.tiktok.com/legal/page/row/privacy-policy/vi" \
    --k-nearest-legal=3 \
    --k-nearest-policy=10 \
