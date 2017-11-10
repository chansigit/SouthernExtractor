import numpy as np
import nibabel as nib
import dicom
import six, os, sys, time
import SimpleITK as sitk
from radiomics import featureextractor
#slicePath = "C:/Users/chensj/Desktop/ITKSNP/3d/1.nii"
#contourPath = "C:/Users/chensj/Desktop/ITKSNP/3d/Untitled.nii"

t1=time.time()

slicePath = sys.argv[1]
contourPath = sys.argv[2]

ni_slice  = nib.load(slicePath)
ni_contour  = nib.load(contourPath)

data = np.array(ni_slice.get_data()).transpose((1,0,2))
contour= np.array(ni_contour.get_data()).transpose((1,0,2))
data_spacing = ni_slice.header.get_zooms()
contour_spacing = ni_contour.header.get_zooms()

print("Spacing in x-, y-, z- axes: (%.6f, %.6f, %.6f)"%data_spacing)
print("Data shape: "+str(data.shape))


sitk_data    = sitk.GetImageFromArray(data)
sitk_data.SetSpacing((float(data_spacing[0]), float(data_spacing[1]), float(data_spacing[2])))
sitk_contour = sitk.GetImageFromArray(contour)
sitk_contour.SetSpacing((float(contour_spacing[0]), float(contour_spacing[1]), float(contour_spacing[2])))


extractor = featureextractor.RadiomicsFeaturesExtractor()
extractor.enableAllImageTypes()
extractor.enableAllFeatures()
result = extractor.execute(sitk_data, sitk_contour)

import pandas as pd
df = pd.DataFrame(columns=['feature_id', 'feature_name', 'feature_value'])
cnt =1
for key, val in six.iteritems(result):
    if key.startswith("general"):
        continue
    df.loc[cnt]=[cnt, key, val]
    cnt+=1

holder=sys.argv[3]
outputFile=os.path.join(holder, os.path.basename(slicePath)+".xlsx")
xlsxWriter = pd.ExcelWriter(outputFile)
df.to_excel(xlsxWriter,sheet_name='radiomics',index=False)
xlsxWriter.save()    
print("taking %.4f seconds" %(time.time()-t1))