from matplotlib import pyplot as plt
import tifffile

# script to show check chosen images
img = tifffile.imread(files='data/images/source_7/20210723_Run2/nocodazole/CP2-SC1-04_B02_s3.tif')   # (5, 1080, 1080)
plt.imshow(img[0], cmap='gray')   # 0 = DNA, 1 = ER, 2 = Mito, 3 = AGP, 4 = RNA
plt.show()