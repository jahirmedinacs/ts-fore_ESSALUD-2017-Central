#! /usr/bin/python3 -s

from imageio import imread as imr
import numpy as np

import sys
import os
import copy

# from matplotlib import pyplot as plt

def gray_scale(dim_3_matrix):
	r, g, b = dim_3_matrix[ : , : , 0 ] , dim_3_matrix[ : , : , 1 ] , dim_3_matrix[ : , : , 2 ]

	return np.floor(0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)

def quantum_img(gray_img, b):
	return gray_img >> (8 - b)

def b_histogram(gray_img, b):
	return np.histogram(gray_img,range(int(2**b+1)))

def vector_probability(data):
	output = data / np.sum(data)

	# print(np.sum(output))

	return output

def co_ocurrence_matrix(image_data, b, shift=[1,1]):
	output = np.zeros((int(2**b),int(2**b)))

	for x in range(image_data.shape[0]):
		for y in range(image_data.shape[1]):
			try:
				i = image_data[x , y]
				j = image_data[x + shift[0] , y + shift[1]]
				output[i , j] += 1
			except:
				pass

	prob = output/np.sum(output)

	return [output,prob]


def descrivers(image_data, b, shift=[1,1]):
	[coocurrence, normal_prob] = co_ocurrence_matrix(image_data, b, shift)

	ids = np.arange(int(2**b))

	u_i = np.dot(ids.T, np.sum(normal_prob, axis=1))
	u_j = np.dot(ids.T, np.sum(normal_prob, axis=0))

	sigma_i = np.dot(np.power((ids - u_i), 2).T, np.sum(normal_prob, axis=1))
	sigma_j = np.dot(np.power((ids - u_j), 2).T, np.sum(normal_prob, axis=0))

	energy = np.sum(np.power(normal_prob,2))
	
	entropy = - np.sum(normal_prob * np.log(np.abs(normal_prob + 1e-64)))

	i_matrix = np.repeat(ids, ids.shape[0]).reshape(normal_prob.shape)
	j_matrix = i_matrix.T

	contrast = np.sum(np.power(i_matrix - j_matrix, 2) * normal_prob)
	contrast *= (1 / ((2**b - 1) ** 2))

	if (sigma_i * sigma_j) > 0:
		correlation = np.sum(i_matrix * j_matrix * normal_prob)
		correlation = (correlation - (u_i * u_j)) / (sigma_i * sigma_j)
	else:
		correlation = 0

	homogenity = np.sum(normal_prob / (1 + np.abs(i_matrix - j_matrix)))

	return np.array([energy, entropy, contrast, correlation, homogenity])

def convolve(img_d, fltr_d):

	zero_x = fltr_d.shape[0]//2
	zero_y = fltr_d.shape[1]//2

	output = np.zeros((img_d.shape[0] - 2, img_d.shape[1] - 2)) 

	re_indx_x = 0
	for ii in range(1, img_d.shape[0] - 1):
		re_indx_y = 0
		for jj in range(1, img_d.shape[1] - 1):
			crry = img_d[-1*zero_x + ii : zero_x + ii + 1, -1*zero_y + jj : zero_y + jj + 1]
			# doing the convolution operation , using the dot product form (the matrix are converted to arrays)
			output[re_indx_x , re_indx_y] = np.dot(fltr_d.flatten() , crry.flatten())

			re_indx_y += 1
		re_indx_x += 1

	return output

def gradient_orientation(image_data, bins=18):
	sobel_x = np.matrix(	[	
								[-1, -2, -1],
								[0, 0, 0],
								[1, 2, 1]
											]	)
	sobel_y = np.matrix(	[	
								[-1, 0, 1],
								[-2, 0, 2],
								[-1, 0, 1]
											]	)

	g_x = convolve(image_data, sobel_x) # convolution X for the sobel X matrix
	g_y = convolve(image_data, sobel_y) # convolution Y for the sobel Y matrix

	# print(np.min(g_x), np.min(g_y))

	#     _________________
	#__  /       2        2
	#  \/   ( g_x  ) + ( g_y  )
	g_sum_sqrt = np.sqrt( np.power(g_x , 2) + np.power(g_y , 2))

	M = g_sum_sqrt / (np.sum(g_sum_sqrt) + 1e-64)
	
	phi = (np.arctan2(g_y, g_x) * 180.0 / np.pi) + 180.0

	phi_hist = np.histogram(phi, bins, range=(0.0, 360.0))

	bin_phi = np.ceil((phi / 360) * bins ).astype(int) - 1

	grad_charc = phi_hist[0].astype(np.float32)
	for ii in range(phi.shape[0]):
		for jj in range(phi.shape[1]):
			grad_charc[bin_phi[ii, jj]] += M[ii, jj]

	return grad_charc

def characterist_vector(img_sample, b):
	img_sample_gray = gray_scale(img_sample)

	img_sample_quantum = quantum_img(img_sample_gray, b)

	img_sample_histogram = b_histogram(img_sample_quantum, b)

	d_histo = vector_probability(img_sample_histogram[0])
	
	d_descr = descrivers(img_sample_quantum, b)

	d_grad = gradient_orientation(img_sample_quantum)

	return np.append(np.append(d_histo, d_descr), d_grad)

def distance(v_1, v_2):
	return np.sqrt(np.sum(np.power((v_2 - v_1), 2)))

def descriptors(image_data):
	temp = np.zeros((1<<12, 1<<12, 3))
	temp[ : , : , : ] = image_data[ : , : , :3 ]
	output_carry = copy.copy(temp)
	del temp
	return characterist_vector(output_carry, 8)

# def main():
# 	path_file = "./" + input().rstrip()
# 	input_carry = imr(path_file, 'png')
# 	temp = np.zeros((32,32,3))
# 	temp[ : , : , : ] = input_carry[ : , : , :3 ]
# 	o_color_image = copy.copy(temp)
# 	del temp
# 	del input_carry

# 	path_file = "./" + input().rstrip()
# 	input_carry = imr(path_file, 'png')
# 	temp = np.zeros((256,256,3))
# 	temp[ : , : , : ] = input_carry[ : , : , :3 ]
# 	g_color_image = copy.copy(temp)
# 	del temp
# 	del input_carry

# 	b = int(input(""))

# 	o_descrivers = characterist_vector(o_color_image, b)

# 	min_distance = 1e64

# 	shift = 16

# 	window = 1
# 	rpta = None
# 	for ii in range(1,shift):
# 		start_ii = (ii - 1) * shift
# 		end_ii = (ii + 1) * shift - 1
# 		for jj in range(1,shift):
# 			start_jj = (jj - 1) * shift
# 			end_jj = (jj + 1) * shift - 1
			
# 			sub_sample = g_color_image[ start_ii : end_ii, start_jj : end_jj, :]

# 			sub_descrivers = characterist_vector(sub_sample, b)

# 			dist = distance(sub_descrivers, o_descrivers)

# 			if dist < min_distance:
# 				min_distance = dist
# 				rpta = window
			
# 			window += 1

# 	print(rpta)
# 	return None

# main()