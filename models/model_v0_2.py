import tensorflow as tf
from keras.losses import BinaryCrossentropy
from tensorflow import keras

class ContentBasedFiltering:
    # v0.2
    def __init__(self, 
                 num_G_features, 
                 num_T_features,
                 Group_NN_width,
                 Group_NN_depth,
                 Technique_NN_width,
                 Technique_NN_depth):
        self.seed = 17
        self.set_random_seed()
        
        # input / output config
        self.num_G_features = num_G_features
        self.num_T_features = num_T_features
        self.num_outputs = 32
        
        # neural network config
        self.Group_NN_width = Group_NN_width
        self.Group_NN_depth = Group_NN_depth
        self.Technique_NN_width = Technique_NN_width
        self.Technique_NN_depth = Technique_NN_depth
        
        
        self.early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',  # Monitor validation loss for early stopping
        patience=32,           # Number of epochs with no improvement before stopping
        restore_best_weights=True  # Restore model weights from the epoch with the best validation loss
        )   

        # BUILD MODEL
        self.model = self.build_model()
        self.compile_model ()
    
    def set_random_seed(self):
        tf.random.set_seed(self.seed)
    
    def build_hidden_layers(self, width, depth):
        layers = []
        for _ in range (depth):
            layers.append(tf.keras.layers.Dense (width, activation = 'relu'))
        return layers
    
    def build_model(self):
        self.set_random_seed()
        ### Group NN
        Group_NN = tf.keras.models.Sequential(
            layers= self.build_hidden_layers (width= self.Group_NN_width, depth = self.Group_NN_depth) +
            [tf.keras.layers.Dense (self.num_outputs, activation  = 'linear', name = 'output_Group')],
            name= "Group_NN")
        input_Group = tf.keras.layers.Input(shape = (self.num_G_features), name = "input_Group")
        vg = Group_NN(input_Group)
        
        ### Technique NN
        self.set_random_seed()
        Technique_NN = tf.keras.models.Sequential(
            layers = self.build_hidden_layers (width= self.Technique_NN_width, depth= self.Technique_NN_depth) +
            [tf.keras.layers.Dense (self.num_outputs, activation  = 'linear', name = 'output_Technique')],  
            name = "Technique_NN")
        input_Technique = tf.keras.layers.Input (shape= (self.num_T_features), name = "input_Technique")
        vt = Technique_NN (input_Technique)
        output = tf.keras.layers.Dot (axes=1)(inputs= [vg, vt])
        
        model = tf.keras.Model (inputs = [input_Group, input_Technique],
                        outputs = output, name = 'recsysNN_model')
        return model

    def compile_model (self):
        self.set_random_seed()
        opt = keras.optimizers.Adam (learning_rate= 0.01)
        self.model.compile  (optimizer = opt, loss = BinaryCrossentropy (from_logits= True))
        

    def train(self, train_data, val_data, epochs):
        history = self.model.fit(
            train_data, 
            validation_data=val_data, 
            epochs=epochs,
            callbacks=self.early_stopping)
        return history
    
    def evaluate(self, test_data):
        # Evaluate your model on the test data
        return self.model.evaluate(test_data)
    
    def predict(self, input_data):
        # Make predictions using your model
        return self.model.predict(input_data)

