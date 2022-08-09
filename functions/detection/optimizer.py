from mealpy.bio_based import SMA, BBO
from mealpy.evolutionary_based import GA
from mealpy.music_based import HS
from mealpy.swarm_based import PSO
from mealpy.system_based import AEO


def get_optimizer(optimizer, problem_dict):
    if optimizer == 'BBO':
        model = BBO.BaseBBO(problem_dict, epoch=100, pop_size=20)
    elif optimizer == 'PSO':
        model = PSO.BasePSO(problem_dict, epoch=100, pop_size=20)
    elif optimizer == 'AEO':
        model = AEO.OriginalAEO(problem_dict, epoch=100, pop_size=20)
    elif optimizer == 'HS':
        model = HS.BaseHS(problem_dict, epoch=100, pop_size=20)
    elif optimizer == 'GA':
        model = GA.BaseGA(problem_dict, epoch=100, pop_size=20)
    else:
        return None

    return model
