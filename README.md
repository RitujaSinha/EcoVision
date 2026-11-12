# ♻️ EcoVision: Deep Learning-Based Waste Classification and Sorting System
 
EcoVision is a low-cost, real-time waste classification system that uses computer vision and transfer learning (MobileNetV2) to sort everyday waste into six categories and, optionally, trigger a servo-driven flap to drop the item into the right bin.

---
 
## 📖 Overview
 
More than 2.1 billion metric tons of municipal solid waste are generated globally each year, yet less than 20% of recyclable material is actually recycled. The main culprit is **source-level contamination**: a greasy food box or half-full soda can in the wrong bin can spoil an entire batch, sending it to landfill.
 
Manual sorting is slow, unhealthy, and error-prone (human error rates of roughly 25–35% due to fatigue), while industrial optical sorters cost hundreds of thousands of dollars and are too large for neighborhood bins, schools, and offices.
 
EcoVision fills that gap: a camera plus a lightweight CNN running on a Raspberry Pi or an ordinary office PC.
 
## 🎯 Objectives
 
- **Classify 6 waste types:** Plastic, Paper, Glass, Metal, Cardboard, Organic
- **High accuracy:** >90% on real-world items (crushed, bent, partially dirty)
- **Fast inference:** <50 ms per frame on ordinary hardware, no GPU required
- **End-to-end prototype:** image pipeline, deep learning model, REST API backend, and web dashboard
## ✨ Key Results
 
| Metric | Value |
|---|---|
| Overall test accuracy | **94.6%** |
| Macro precision / recall / F1 | 94.8% / 94.6% / 94.7% |
| Best class (F1) | Cardboard, 96.7% |
| Weakest class (F1) | Glass, 92.1% |
| Baseline custom CNN accuracy | 81.4% |
| Inference, Intel i7 CPU | 38 ms |
| Inference, Raspberry Pi 4 (TFLite) | 45 ms |
| Inference, NVIDIA Jetson Nano (GPU) | 12 ms |
 
## 🏗️ System Architecture
 
EcoVision runs as a five-stage pipeline:
 
1. **Image capture:** a USB camera captures an RGB photo when an object is detected (HC-SR04 ultrasonic sensor in the hardware prototype).
2. **Preprocessing:** resize to 224×224 and normalize pixel values to [0, 1].
3. **Model inference:** MobileNetV2 extracts features and outputs class probabilities.
4. **Display and telemetry:** predicted category and confidence are shown on the dashboard.
5. **Mechanical sorting:** a servo motor tilts the sorting flap to drop the item into the correct bin.
```
Camera → Preprocess → MobileNetV2 + Classifier Head → Softmax → FastAPI → Dashboard / Servo Flap
```
 
## 🧠 Model
 
### Baseline: custom CNN
Three Conv2D blocks (32, 64, 128 filters, 3×3, ReLU, 2×2 max pooling), then Flatten → Dense(128) → Dropout(0.5) → Dense(6, softmax). It reached only **81.4%** accuracy, because three convolutional layers could not capture subtle differences between crumpled materials.
 
### Production: MobileNetV2 with transfer learning
- MobileNetV2 pre-trained on ImageNet, base layers **frozen**
- Head: Global Average Pooling → Dense(128) → Dropout(0.5) → Dense(6, softmax)
- Uses **depthwise separable convolutions** (depthwise filter per channel + 1×1 pointwise), cutting computation by roughly 85–90% compared with standard convolutions
### Training details
 
| Setting | Value |
|---|---|
| Loss | Categorical cross-entropy |
| Optimizer | Adam, learning rate 0.0001 |
| LR schedule | Halve the learning rate if validation loss does not improve for 3 epochs |
| Epochs / batch size | 30 / 32 |
| Input size | 224 × 224 × 3 |
| Augmentation | Rotation ±25°, horizontal flip (p=0.5), zoom ±20%, brightness ±15% |
 
## 📊 Dataset
 
About **3,500 real-world images** across six balanced classes, combining the benchmark **TrashNet** dataset with everyday rubbish photos taken under realistic lighting.
 
| Class | Examples |
|---|---|
| Plastic | Clear bottles, food tubs, lids, containers |
| Paper | Printouts, newspapers, mailers, envelopes |
| Glass | Beverage bottles, clear jars, broken glass |
| Metal | Soda cans, food tins, bottle caps, foil |
| Cardboard | Delivery boxes, packaging cartons |
| Organic | Fruit peels, food scraps, coffee grounds |
 
**Split:** 70% train (2,450) · 15% validation (525) · 15% test (525)
 
## 📈 Evaluation
 
### Training curves
- Training accuracy: 48.2% (epoch 1) → 96.8% (epoch 30)
- Validation accuracy: 45.1% → **94.6%**
- Loss: 1.85 → 0.12 (train), 0.18 (validation)
### Per-class performance on the 525-image test set
 
| Waste Category | Precision | Recall | F1-Score | Test Images |
|---|---|---|---|---|
| Plastic | 95.2% | 94.0% | 94.6% | 99 |
| Paper | 93.8% | 95.1% | 94.4% | 92 |
| Glass | 92.4% | 91.8% | 92.1% | 80 |
| Metal | 96.1% | 94.8% | 95.4% | 84 |
| Cardboard | 97.0% | 96.5% | 96.7% | 89 |
| Organic | 94.5% | 95.2% | 94.8% | 81 |
| **Overall Average** | **94.8%** | **94.6%** | **94.7%** | **525** |
 
### Error analysis
- **Clear plastic vs. clear glass:** specular highlights on clean PET bottles resemble glass jars (4 of 80 glass test images were predicted as plastic). Recommended fix: a polarizing filter or diffuse LED ring light.
- **Food-stained cardboard:** greasy boxes (e.g., pizza boxes) drop model confidence below 75%. **Safety rule:** if confidence < 70%, the item is routed to general waste or compost to avoid contaminating clean paper batches.
## 🔧 Hardware Prototype (Smart Sorting Bin)
 
- Webcam mounted above the drop chute
- HC-SR04 ultrasonic sensor to detect an inserted object
- Local processor (Raspberry Pi 4) runs inference
- 180° servo motor, driven over GPIO, tilts the sorting flap into the right compartment
- End-to-end decision time of roughly 40 ms
## 🛠️ Tech Stack
 
| Component | Technology | Purpose |
|---|---|---|
| Language | Python 3.10 | Core logic and model training |
| Deep learning | TensorFlow / Keras | Training and transfer learning |
| Computer vision | OpenCV | Frame capture and resizing |
| Backend API | FastAPI / Uvicorn | Asynchronous REST server |
| User interface | React & modern CSS | Live dashboard showing predictions |
| Target hardware | Raspberry Pi 4 | Edge inference and servo control |
 
## ⚠️ Limitations
 
- **Severe crushing:** a completely flattened metal can may be confused with reflective plastic wrappers. An inductive metal sensor under the flap can resolve this.
- **Dirty environments:** dust on the lens causes blurry images in outdoor settings, so a protective clear cover is needed.
## 🗺️ Roadmap
 
1. **Real-time video detection (YOLOv8):** track multiple moving items on a conveyor
2. **Robotic arm integration:** 3-axis arm to pick up items automatically
3. **Smart bin fill sensors:** ultrasonic sensors with LoRa / Wi-Fi alerts when a bin is 90% full
4. **Citizen incentive app:** scan a QR code at the bin to earn loyalty points or transport discounts
## 🌍 Use Cases
 
University campuses, residential complexes, shopping malls, offices, schools, and municipal collection centers, anywhere waste is sorted at the point of disposal.
 
## 📚 References
 
1. M. Yang and G. Thung, "Classification of trash for recyclability: A deep learning approach," Stanford CS229 Technical Report, 2016.
2. M. Sandler et al., "MobileNetV2: Inverted residuals and linear bottlenecks," *CVPR*, 2018, pp. 4510–4520.
3. UNEP, "Global waste management outlook: Towards circular economy solutions," 2024.
4. J. Redmon and A. Farhadi, "YOLOv3: An incremental improvement," arXiv:1804.02767, 2018.
5. A. Krizhevsky, I. Sutskever, and G. E. Hinton, "ImageNet classification with deep convolutional neural networks," *NeurIPS*, vol. 25, 2012.
6. C. Szegedy et al., "Going deeper with convolutions," *CVPR*, 2015.
7. K. He et al., "Deep residual learning for image recognition," *CVPR*, 2016.
8. S. Zhi, J. Zhou, and H. Fan, "Smart waste classification system using deep learning and edge computing," *IEEE Internet of Things Journal*, vol. 9, no. 14, 2022.
## 🔗 Repository
 
[github.com/RitujaSinha/EcoVision](https://github.com/RitujaSinha/EcoVision)

## 🎥 Project Demo


https://github.com/user-attachments/assets/17de4b62-b9c8-439b-9c7f-ba76d1c41e51


