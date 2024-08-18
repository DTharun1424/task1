import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, LSTM, Embedding, Dense, Dropout

def extract_image_features(image):
    base_model = ResNet50(weights='imagenet')
    model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)
    processed_image = preprocess_input_image(image)
    return model.predict(processed_image)

def preprocess_input_image(image):
    image = tf.image.resize(image, (224, 224))
    image = tf.keras.applications.resnet50.preprocess_input(image)
    return np.expand_dims(image, axis=0)

def build_caption_model(vocab_size, max_caption_length, embedding_dim=256, units=512):
    image_features_input = Input(shape=(2048,))  
    image_features = Dense(units, activation='relu')(image_features_input)
    image_features = Dropout(0.5)(image_features)

    caption_input = Input(shape=(max_caption_length,))
    caption_embedding = Embedding(vocab_size, embedding_dim, mask_zero=True)(caption_input)
    caption_embedding = Dropout(0.5)(caption_embedding)

    lstm_output = LSTM(units, return_sequences=False)(caption_embedding)

    combined = tf.keras.layers.add([image_features, lstm_output])
    combined = Dense(units, activation='relu')(combined)

    output = Dense(vocab_size, activation='softmax')(combined)

    model = Model(inputs=[image_features_input, caption_input], outputs=output)
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    return model

def generate_caption(model, image_features, tokenizer, max_caption_length):
    input_seq = [tokenizer.word_index['<start>']]
    for _ in range(max_caption_length):
        input_seq_padded = pad_sequences([input_seq], maxlen=max_caption_length)
        prediction = model.predict([image_features, input_seq_padded], verbose=0)
        predicted_word_idx = np.argmax(prediction)
        predicted_word = tokenizer.index_word[predicted_word_idx]
        if predicted_word == '<end>':
            break
        input_seq.append(predicted_word_idx)
    
    caption = ' '.join([tokenizer.index_word[idx] for idx in input_seq[1:]])
    return caption
def main():
    image = load_image('sample_image.jpg')  

    image_features = extract_image_features(image)

    tokenizer = Tokenizer()  
    vocab_size = len(tokenizer.word_index) + 1
    max_caption_length = 20 

    model = build_caption_model(vocab_size, max_caption_length)

    model.load_weights('caption_model_weights.h5') 

    caption = generate_caption(model, image_features, tokenizer, max_caption_length)
    print("Generated Caption:", caption)

if __name__ == "__main__":
    main()
