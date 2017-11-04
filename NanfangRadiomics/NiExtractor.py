import numpy as np
import nibabel as nib
import dicom
import six,os,sys
import SimpleITK as sitk
from radiomics import featureextractor

def NiFeatureExtractor(slicePath, contourPath):
	# loading the NIfTI1 image & annotation
	ni_slice   = nib.load(slicePath)
	ni_contour = nib.load(contourPath)
	data       = np.array(ni_slice.get_data()).reshape(512,512).transpose()
	contour    = np.array(ni_contour.get_data()).reshape(512,512).transpose()
	sitk_data    = sitk.GetImageFromArray(data.reshape(512,512,1))
	sitk_contour = sitk.GetImageFromArray(contour.reshape(512,512,1))

	extractor = featureextractor.RadiomicsFeaturesExtractor()
	extractor.enableAllImageTypes()
	extractor.enableAllFeatures()
	result = extractor.execute(sitk_data, sitk_contour)
	return result

#slicePath = "C:/Users/chensj/Desktop/ITKSNP/1/baoyongyao.nii"
#contourPath = "C:/Users/chensj/Desktop/ITKSNP/1/Untitled.nii"

try:
	slicePath   = sys.argv[1]
	contourPath = sys.argv[2]
except IndexError:
	slicePath   = input("CT Nii File=")
	contourPath = input("Tumor Mask Nii File=")


result=NiFeatureExtractor(slicePath=slicePath,contourPath=contourPath)
outputFile = input("Please input the output location:")
fp = open(os.path.join(outputFile, "radiomics.tsv"),"w")

cnt =1
for key, val in six.iteritems(result):
    if key.startswith("general"):
        continue
    fp.write("%d\t%s\t%.12f\n"%(cnt, key, val))
    cnt+=1
    
fp.close()