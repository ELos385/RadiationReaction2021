#!/usr/bin/python3
# Author: Chris Arran
# Date: September 2021
#
# Aims to estimate the a0 from the gamma profile

import numpy as np
from scipy.constants import pi,c,alpha,m_e
from scipy.signal import medfilt
from lib import moments_2d
	
# Image processing to remove salt and pepper noise and constant background
def spot_filtering(im,medfiltwidth=5,threshold=1):
	despeckled = medfilt(im,kernel_size=medfiltwidth)
	bg = np.median(despeckled)
	imout = despeckled - threshold*bg

	return imout	

# Find the difference in width between the two axes
def get_vardiff(im,rad_per_px):
	xw,yw = moments_2d.findwidth(im)
	vardiff = np.abs(xw**2-yw**2)*rad_per_px**2

	return vardiff

# Approx estimate which is model independent
def a0_estimate_av(vardiff,gammai,gammaf):
	a0 = np.sqrt(4*np.sqrt(2))*np.sqrt(gammaf*gammai*vardiff)
	
	return a0

# Assume a Gaussian beam and classical RR
def a0_estimate_cl(vardiff,gammai,tau=40.0e-15,lambda0=0.8e-6):
	R = (8.0/5.0)*gammai**2 * vardiff - 1.0
	omega0 = 2*pi*c/lambda0
	g2 = omega0*tau*np.sqrt(pi/(4*np.log(2)))
	a0 = np.sqrt((3*m_e*R)/(2*alpha*gammai*omega0*g2))
	
	return a0

# Class for estimating a0
class a0_Estimator:
	"""

	"""
	# Initialise
	def __init__(self, wavelength=0.8e-6, FWHM_t=40.0e-15, medfiltwidth=5, threshold=1, rad_per_px=None):
		self.lambda0 = wavelength
		self.tau = FWHM_t
		self.medfiltwidth = medfiltwidth
		self.threshold = threshold
		self.rad_per_px = rad_per_px
	
	# Estimate a0
	def get_a0(self,im):
		imout = spot_filtering(im, medfiltwidth=self.medfiltwidth, threshold=self.threshold)
		vardiff = get_vardiff(imout,self.rad_per_px)
		a0 = a0_estimate_av(vardiff,gammai,gammaf)
		
		return a0
