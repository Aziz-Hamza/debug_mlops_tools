"""
module qui démontre l'utilisation d'hydra comme un outil de configuration;
avec la possibilité de charger des classes depuis un fichier de configuration
Dans ce cas des classes sont des samplers,
notre objective est dexpérimenterr avec  différentes combinaisons

+ la solution est d'utiliser:

        + le mot cle _target_ dans le fichier dans configuration
        + Utiliser  instantiate(from hydra.utils import instantiate);
        + la fonction décorée par hydra doit être considéré comme entry point de votre programme,et ne return rien

"""
import hydra
from omegaconf import DictConfig
import optuna
from hydra.utils import instantiate


@hydra.main(config_path="", config_name="config")
def entry_point(cfg: DictConfig):
    print(f'{cfg.date}')
    study = optimize(cfg)
    print(study.best_params)


def objective(trial):
    x = trial.suggest_float('x', -10, 10)
    return (x - 2) ** 2


def optimize(cfg):
    sampler = instantiate(cfg.sampler)
    study = optuna.create_study(sampler=sampler)
    study.optimize(objective, n_trials=100)
    print(cfg.sampler)
    return study


if __name__ == "__main__":
    entry_point()
