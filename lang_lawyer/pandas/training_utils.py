
import tensorflow as tf
import matplotlib.pyplot as plt
from IPython.display import clear_output


class PlotLearning(tf.keras.callbacks.Callback):
    def __init__(self, *args, clear=True, log_scale=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear = clear
        self.log_scale = log_scale
        
    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        self.acc = []
        self.val_acc = []
        self.fig = plt.figure()
        self.plot_accuracy = False
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.i += 1
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        if logs.get('acc'):
            self.plot_accuracy = True
            self.acc.append(logs.get('acc'))
            self.val_acc.append(logs.get('val_acc'))
            
            f, (ax1, ax2) = plt.subplots(1, 2, sharex=True)
        else:
            f, ax1 = plt.subplots(1, 1)
            
        if self.clear:
            clear_output(wait=True)
        
        if self.log_scale:
            ax1.set_yscale('log')
            
        ax1.plot(self.x, self.losses, label="loss")
        ax1.plot(self.x, self.val_losses, label="val_loss")
        ax1.legend()
        
        if self.plot_accuracy:
            ax2.plot(self.x, self.acc, label="accuracy")
            ax2.plot(self.x, self.val_acc, label="validation accuracy")
            ax2.legend()
        
        plt.show()

        
def limit_memory(fraction=0.25):
    from keras.backend.tensorflow_backend import set_session
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = fraction
    config.gpu_options.allow_growth = True
    set_session(tf.Session(config=config))
