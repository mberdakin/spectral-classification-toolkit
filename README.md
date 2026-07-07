|README.md

1. Motivation 

2. Project description

3. Repository structure

4. Dataset

5. Workflow

6. Neural Network

7. Results

8. Future work

#1. Motivation 
Laser-Induced Breakdown Spectroscopy (LIBS) produces high-dimensional spectra whose interpretation can benefit from machine learning methods. This repository illustrates a complete TensorFlow workflow for supervised classification of experimental spectra.

Beyond achieving high classification accuracy, the project investigates whether models trained on one bone specimen can generalize to different bones belonging to the same individual (as done http://dx.doi.org/10.1016/j.sab.2014.07.008 or https://doi.org/10.1016/j.talanta.2021.122780), a scenario that better reflects potential forensic applications. 


#2. Project description:  
###LIBS Bone Classification using TensorFlow

This repository contains a simplified machine learning workflow for the classification of Laser-Induced Breakdown Spectroscopy (LIBS) spectra.

The project was developed as a proof-of-concept for applying supervised learning techniques to experimental spectroscopic data. The objective is to classify bone spectra according to the individual from which the sample originated and to evaluate the model's ability to generalize to spectra acquired from different bones belonging to the same individual.

#3. Repository structure
.
├── notebooks/
│   └── LIBS_classification.ipynb
│
├── raw_data/
│
├── results/
│
├── ML_libs/
│
├── requirements.txt
│
└── README.md

#4. Dataset
Each experiment corresponds to approximately 100 LIBS spectra acquired from a single bone sample.

Each spectrum contains the measured emission intensity as a function of wavelength.

Multiple bone samples from the same individual are available, allowing the evaluation of the model's ability to generalize beyond the training specimens.

#5. Workflow
(a) Raw spectra
(b) preprocessing: Normalization/region selection/ Baseline correction  
(c) Train/Test split
(d) Random Forest
(e) TensorFlow Neural Network
(f) Generalization Test

#6. Neural Network 

The TensorFlow model consists of  

- Dense(128, ReLU)
- Dropout(0.5)
- Dense(64, ReLU)
- Dense(Output, Softmax)

Optimization:
- Adam optimizer
- Sparse categorical crossentropy
- Early stopping

#7. Results 
Both Random Forest and the Feedforward Neural Network achieved excellent performance on the held-out test set.

The notebook also evaluates the models on spectra acquired from different bones belonging to the same individuals, providing a preliminary assessment of their ability to generalize beyond the training specimens.

#8. Future Work 

Future improvements include

- evaluation on larger datasets
- hyperparameter optimization
- uncertainty estimation
- explainable AI methods (e.g. SHAP)
