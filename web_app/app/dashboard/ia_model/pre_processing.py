import pickle
import os
import numpy as np
from django.conf import settings

def load_scaler_encoder(nome_conjunto):
    model_dir = os.path.join(settings.BASE_DIR, 'dashboard', 'ia_model')

    scaler_path = os.path.join(model_dir, f'scaler_{nome_conjunto}.pkl')
    encoder_path = os.path.join(model_dir, f'encoder_{nome_conjunto}.pkl')

    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    with open(encoder_path, 'rb') as f:
        encoder = pickle.load(f)

    return scaler, encoder

def preprocess_input(data_dict, nome_conjunto='baseline'):
    """
    data_dict deve ter as chaves:
    X1, X2, X3, X4, X5, X6, X7, X8
    """
    # 1️⃣ Separar as variáveis
    continuous_cols = ['X1', 'X2', 'X3', 'X4', 'X5', 'X7']
    categorical_cols = ['X6', 'X8']

    continuous_data = [[data_dict[col] for col in continuous_cols]]
    categorical_data = [[data_dict[col] for col in categorical_cols]]

    # 2️⃣ Carregar scaler e encoder
    scaler, encoder = load_scaler_encoder(nome_conjunto)

    # 3️⃣ Transformar
    scaled_continuous = scaler.transform(continuous_data)
    encoded_categorical = encoder.transform(categorical_data)

    # 4️⃣ Concatenar
    X_processed = np.hstack([scaled_continuous, encoded_categorical])

    return X_processed
