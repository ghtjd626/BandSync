import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from music21 import stream, note, chord

class AIComposer:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def train_model(self, sequences, vocab_size, seq_length):
        """
        Train an LSTM-based model for chord sequence generation.
        :param sequences: List of tokenized sequences.
        :param vocab_size: Total number of unique tokens.
        :param seq_length: Length of input sequences.
        """
        self.model = Sequential([
            Embedding(input_dim=vocab_size, output_dim=50, input_length=seq_length),
            LSTM(256, return_sequences=True),
            LSTM(256),
            Dense(256, activation='relu'),
            Dense(vocab_size, activation='softmax')
        ])
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        X, y = self._prepare_data(sequences, seq_length)
        self.model.fit(X, y, epochs=50, batch_size=64)

    def generate_sequence(self, seed_sequence, seq_length, num_steps):
        """
        Generate a sequence of chords or notes based on a seed sequence.
        :param seed_sequence: List of seed tokens.
        :param seq_length: Length of input sequences.
        :param num_steps: Number of steps to generate.
        :return: Generated sequence of tokens.
        """
        generated = list(seed_sequence)
        for _ in range(num_steps):
            input_seq = np.array(generated[-seq_length:]).reshape(1, seq_length)
            prediction = np.argmax(self.model.predict(input_seq), axis=-1)[0]
            generated.append(prediction)
        return generated

    def save_to_midi(self, token_sequence, output_file):
        """
        Convert a token sequence to MIDI format and save it.
        :param token_sequence: List of tokens representing notes or chords.
        :param output_file: Path to save the MIDI file.
        """
        midi_stream = stream.Stream()
        for token in token_sequence:
            if "." in token:
                notes = [note.Note(n) for n in token.split(".")]
                midi_stream.append(chord.Chord(notes))
            else:
                midi_stream.append(note.Note(token))
        midi_stream.write('midi', fp=output_file)

    @staticmethod
    def _prepare_data(sequences, seq_length):
        """
        Prepare input and output data for training.
        :param sequences: List of tokenized sequences.
        :param seq_length: Length of input sequences.
        :return: Input and output arrays.
        """
        X, y = [], []
        for seq in sequences:
            for i in range(len(seq) - seq_length):
                X.append(seq[i:i + seq_length])
                y.append(seq[i + seq_length])
        return np.array(X), np.array(y)

# Example usage
if __name__ == "__main__":
    composer = AIComposer()
    # Example data: Tokenized sequences of chords or notes
    sequences = [
        [1, 2, 3, 4, 5],
        [3, 4, 5, 6, 7],
        [5, 6, 7, 8, 9]
    ]
    vocab_size = 10  # Number of unique tokens
    seq_length = 4

    # Train the model
    composer.train_model(sequences, vocab_size, seq_length)

    # Generate music
    seed = [1, 2, 3, 4]
    generated_sequence = composer.generate_sequence(seed, seq_length, num_steps=10)
    print("Generated Sequence:", generated_sequence)

    # Save to MIDI
    composer.save_to_midi([str(x) for x in generated_sequence], "output.mid")
