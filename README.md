# ML_ScratchPad
Semantic Segmentation of Images using Popular FCN based Architectures
---
#### Following Models are implemented
* [Attention U-Net](http://arxiv.org/abs/1804.03999)
* [Deep Dilation Net](http://arxiv.org/abs/1905.12120)

#### The Potsdam Dataset (RGBIR + DSM & Labels) is also uploaded and divided into training, validation and testing (no labels available).
The images and corresponding labels are indexed in the form of hash table stored in a `json` file. Custom loss functions are also implemented accordingly.

#### Requirements
* tensorflow >= 2.1
* keras
* numpy
* rasterio
