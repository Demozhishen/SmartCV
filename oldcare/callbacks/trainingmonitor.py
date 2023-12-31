# -*- coding: utf-8 -*-

# import the necessary packages
from keras.callbacks import BaseLogger
import matplotlib.pyplot as plt
import numpy as np
import json
import os

class TrainingMonitor(BaseLogger):
	def __init__(self, figPath, jsonPath=None, startAt=0):
		# store the output path for the figure, the path to the JSON
		# serialized file, and the starting epoch
		super(TrainingMonitor, self).__init__()
		self.figPath = figPath
		self.jsonPath = jsonPath
		self.startAt = startAt

	def on_train_begin(self, logs={}):
		'''
		is called once the training process starts:
		'''
		# initialize the history dictionary
		self.H = {}

		# if the JSON history path exists, load the training history
		if self.jsonPath is not None:
			if os.path.exists(self.jsonPath):
				self.H = json.loads(open(self.jsonPath).read())

				# check to see if a starting epoch was supplied
				if self.startAt > 0:
					# loop over the entries in the history log and
					# trim any entries that are past the starting
					# epoch
					for k in self.H.keys():
						self.H[k] = self.H[k][:self.startAt]

	def on_epoch_end(self, epoch, logs={}):
		# loop over the logs and update the loss, accuracy, etc.
		# for the entire training process
		for (k, v) in logs.items():
			l = self.H.get(k, [])
			l.append(v)
			self.H[k] = l

		# check to see if the training history should be serialized
		# to file
		if self.jsonPath is not None:
			f = open(self.jsonPath, "w")
			f.write(json.dumps(self.H))
			f.close()

		# ensure at least two epochs have passed before plotting
		# (epoch starts at zero)
		# plot the training loss and accuracy
		N = np.arange(1, len(self.H["loss"]) + 1)
		plt.style.use("ggplot")
		
		file_name = os.path.splitext(self.figPath)[0]
		file_extent = os.path.splitext(self.figPath)[1]
		loss_plot_file = '%s_loss%s' %(file_name , file_extent)
		accuracy_plot_file = '%s_accuracy%s' %(file_name ,file_extent)

        # loss curve
		plt.figure()
		plt.plot(N, self.H["loss"], label="train_loss")
		plt.plot(N, self.H["val_loss"], label="val_loss")
		plt.title("Training Loss [Epoch {}]"
                  .format(len(self.H["loss"])))
		plt.xlabel("Epoch #")
		plt.ylabel("Loss")
		plt.legend()
		# save the figure
		plt.savefig(loss_plot_file)
		plt.close()
        
        # accuracy curve            
		plt.figure()
		plt.plot(N, self.H["acc"], label="train_acc")
		plt.plot(N, self.H["val_acc"], label="val_acc")
		plt.title("Training Accuracy [Epoch {}]"
                  .format(len(self.H["loss"])))
		plt.xlabel("Epoch #")
		plt.ylabel("Accuracy")
		plt.legend()
		# save the figure
		plt.savefig(accuracy_plot_file)
		plt.close()

