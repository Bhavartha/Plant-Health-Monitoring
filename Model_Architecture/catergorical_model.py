import glob
import numpy as np
from cv2 import resize
from matplotlib.image import imread
from matplotlib.pyplot import imshow
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D,Dropout,Dense,MaxPool2D,Flatten
from keras.preprocessing.image import ImageDataGenerator

#for Potato
name = "Potato"
size = 2152
(width,height) = (28,28)
images = np.zeros((size,width,height,3))
labels = np.zeros((size))
label_val = {'Early_blight':0,'Late_blight':1,'healthy':2}

count = 0
for i in sorted(glob.glob('PlantVillage-Dataset/raw/color/*')):
  if name in i:
      print(i)
      for j in glob.glob(i+'/*'):
        images[count] = resize(imread(j)[:,:,:3],(width,height))
        labels[count] = label_val[i.split('___')[1]]
        count += 1
print(count)

y = to_categorical(labels,num_classes=len(label_val))
images = images/255
np.savez("{}_X_y.npz".format(name),X=images,y=y)

X_train,X_test,y_train,y_test = train_test_split(images,y,random_state=5,test_size=0.2)

model = Sequential()
model.add(Conv2D(128,3,3,input_shape=(width,height,3),activation='relu'))
model.add(Conv2D(256,2,1,activation='relu'))
model.add(Conv2D(512,2,1,activation='relu'))
model.add(MaxPool2D())
model.add(Flatten())
model.add(Dense(1024,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(512,activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(100,activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(len(label_val),activation="softmax"))
model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=['accuracy'])
model.summary()

#"""
datagen = ImageDataGenerator(width_shift_range=0.3,height_shift_range=0.3,zoom_range=[0.8,1.2],horizontal_flip=True)
data = datagen.flow(X_train,y_train)
model.fit_generator(data,steps_per_epoch=40,epochs=10,validation_data=(X_test,y_test))
#"""

#model.fit(X_train,y_train,epochs=10,batch_size=128,validation_data=(X_test,y_test))

model.save("{}_dieases.h5".format(name))
