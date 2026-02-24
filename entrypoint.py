import hydra
from clearml import Task
from omegaconf import DictConfig


@hydra.main(version_base=None, config_path="config", config_name="config")
def main(cfg: DictConfig):
    task = Task.init(project_name="uv-hydra-testing", task_name=cfg.run.run_name)
    task.set_packages("requirements.txt")

    print("Hello, Hydra and ClearML!")
    print(cfg)


if __name__ == "__main__":
    main()
