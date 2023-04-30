# DollGear
## 2D VTubers implemented in Python
DollGear is a Python library that can 
make 2D VTuber models and run them.

https://user-images.githubusercontent.com/57708101/235346064-722b3604-6ed5-4af4-bada-b23e2bbfc200.mov


## Requirements
- pygame
- numpy

- dlib
- opencv

## Features
### Simple definition of 2D model
You can define your 2D model using 3 classes.
- Inheriting `Doll`, you can define a 2D model.
- `Part` instances can be added in `Doll`.
You can create model's hands, head, legs, or 
other parts by `Part` instances.
- `Joint` instances are useful for adding 
joints in `Part`.

### Extea Tools
- you can run and see examples in `examples`.
- other utils provide webcam, face landmark extractor,
and so on.
- `part_point_extractor.py` enables you to
clip parts on your model and to determine the location
of Joints on the clipped parts. 
