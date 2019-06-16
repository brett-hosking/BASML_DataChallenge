'''
    Functions used for the BASML Data Challenege
'''
# import shutil
# import requests
# import sys
import os
import numpy as np
import imageio

def loaddata(path,classlist=[None], height=None, width=None, channels=None,labelstr=False):
	'''
	Loads an image dataset (eg. .png .jpg) into numpy arrays X and Y, where X contains all images from the
	dataset and Y contains the corresponding one-hot labels.
	It is assumed that all images are of the same dimension

	Parameters
	----------
	path : string
		absolute or relative path to the image dataset containing folders named by class
	classlist: list of strings
		list of class names to import from path
		Default: load all classes in path
	height: int
		vertical spatial resolution of each image
		Default: uses dimensions of the first image in path
	width: int
		horizontal spatial resolution of each image
		Default: uses dimensions of the first image in path
	channels: int
		number of channels
		Default: uses dimensions of the first image in path
	labelstr: boolean
		True: 	return list of class names
		False: 	return only X and Y arrays

	Returns
	-------
	X : ndarray
		Feature matrix of shape (Total number of images, height, width, channels)
	Y : ndarray
		Labels of shape (Total number of images, total number of classes)
	cat_list : list of strings
		list of class names
		if labelstr=True

	'''
	if classlist[0] == None:
		classlist	= os.listdir(path)
	else:
		classlist	= classlist

	# Total number of labels
	label_num = len(classlist)

	# Total number of files
	file_num = 0
	for category in classlist:
		file_num 	+= len(os.listdir(os.path.join(path,category)  ))

	if None in [width,height,channels]:
		# Image dimensions from first image
		height,width,channels = np.shape( imageio.imread(os.path.join(path,classlist[0],os.listdir(os.path.join(path,classlist[0]))[0])) )

	X 	= np.array( np.zeros( (file_num,height,width,channels) ) )
	Y 	= np.array( np.zeros( (file_num,label_num) ) )

	c_label 	= -1
	annotation	= 0
	for c in classlist:
		c_label+=1
		for file in os.listdir(os.path.join(path,c)  ):
			X[annotation]	= imageio.imread(os.path.join(path,c,file))
			arr = np.array(np.zeros(label_num))
			arr[c_label]	= 1
			Y[annotation]	= arr
			annotation		+=1

	if labelstr:
		return X,Y,classlist
	else:
		return X,Y

def randomiseXY(X,Y):
	'''
	Randomise the order of the data in X and Y.
	This is should be applied prior to splitting the data into
	training and test sets.

	Parameters
	----------
	X : ndarray
		feature matrix
	Y : ndarray
		one-hot labels

	Returns
	-------
	X : ndarray
		randomised feature matrix
	Y : ndarray
		randomised one-hot labels

	'''
	rand_indices 	= np.random.permutation(len(Y));
	X   			= X[rand_indices,:,:,:]
	Y 		 		= Y[rand_indices]

	return X, Y

def class_samplecount(Y):
	'''
	The number of elements in each class


	Parameters
	----------
	Y : ndarray
		one-hot labels

	Returns
	-------
	An array of size equal to the number of classes

	'''
	return np.sum(Y,axis=0)


def ttsplit(X,Y,per=20):
	'''
	Split the dataset into training and test sets according
	to a percentage of each each class


	Parameters
	----------
	X : ndarray
		feature matrix
	Y : ndarray
		one-hot labels
	per : float
		Percentage of the original data used for validation/test

	Returns
	-------
	X : ndarray
		Training feature matrix
	Y : ndarray
		Trainng one-hot labels
	Xtest : ndarray
		Test feature matrix
	Ytest : ndarray
		Test one-hot labels

	'''

	file_num 	= len(Y)
	classes 	= np.shape(Y)[1]
	class_num 	= class_samplecount(Y)
	class_cur	= np.array(np.zeros(classes))
	class_max	= np.array(np.zeros(classes)) # number of samples per class (test)
	for c in range(classes):
		class_max[c] = int(np.rint((class_num[c]/100.0)*per))

	Xtest 		= []
	Ytest		= []
	Xtrain		= []
	Ytrain 		= []
	for i in range(file_num):
		c_idx = np.argmax(Y[i])
		if class_cur[c_idx] < class_max[c_idx]:
			Xtest.append(X[i])
			Ytest.append(Y[i])
			class_cur[c_idx] +=1
		else:
			Xtrain.append(X[i])
			Ytrain.append(Y[i])

	return np.array(Xtrain),np.array(Ytrain),np.array(Xtest),np.array(Ytest)

def save_image(arr,output):
    '''
        Use imageio library to save an image after clipping 
        the input between the range [0,255] and converting
        to unsigned 8-bit int

        Parameters
        ----------
        arr : numpy array 
            image array with either 1 (greyscale) or 3 (RGB)
            channels
        output : string 
            path to output

        Returns
        -------
        None
    '''
    imageio.imwrite(output,np.clip(arr,0,255).astype('uint8'))

# def downloader(url,localdir):
#     r = requests.get(url, allow_redirects=True, stream=True)
#     total_length = r.headers.get('content-length')
#     output = open(localdir, 'wb')
#     if total_length is None: # no content length header
#         output.write(r.content)
#     else:
#         dl = 0
#         total_length = int(total_length)
#         for data in r.iter_content(total_length/100):
#             dl += len(data)
#             output.write(data)
#             done = int(50 * dl / total_length)
#             sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
#             sys.stdout.flush()


# def zipextract(path,zipf):
#     '''
#         shutil method may not work on windows
#     '''
#     try:
#         shutil.unpack_archive(zipf,path)
#     except:
#         import zipfile
#         zip_ref = zipfile.ZipFile(zipf, 'r')
#         zip_ref.extractall(path)
#         zip_ref.close()