from .en_stepper import EnStepper
from .wfxs_strategy import Wfxs
from .wx256_strategy import Wx256
from .zh_82zg_strategy import Zg
from .zh_shuka import ChiShuka
from .zh_stepper_strategy import ChiStepper
from .zhuishukan_strategy import Zhuishukan


def strategy_class(class_name, *args, **kwargs):
    classes = {
        'EnStepper': EnStepper,
        'Wfxs': Wfxs,
        'Wx256': Wx256,
        'Zg': Zg,
        'ChiShuka': ChiShuka,
        'ChiStepper': ChiStepper,
        'Zhuishukan': Zhuishukan
    }
    cls = classes[class_name]
    return cls(*args, **kwargs)