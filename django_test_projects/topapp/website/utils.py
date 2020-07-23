from inspect import isclass
import website.models as web_models
from website.models import *

classes = [x for x in dir(web_models) if isclass(getattr(web_models,x))]

for model_class in classes:
    print(model_class)