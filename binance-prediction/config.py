""" 
LSTM 项目主配置文件（兼容入口）

说明:
- 本项目的主配置文件是 `config_lstm.py`。
- 但为了满足教程/脚本中更通用的命名习惯，我们提供一个 `config.py` 作为兼容入口。

用法:
    from config import DataConfig, ModelConfig, TrainingConfig, PathConfig

作者: qinshihuang166
"""

from config_lstm import (  # noqa: F401
    DataConfig,
    ModelConfig,
    TrainingConfig,
    PathConfig,
    PresetConfigs,
    VisualizationConfig,
    LogConfig,
    print_config_summary,
    estimate_training_time,
    get_input_shape,
)
