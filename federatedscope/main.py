import os
import sys

from yacs.config import CfgNode

DEV_MODE = False  # simplify the federatedscope re-setup everytime we change
# the source codes of federatedscope
if DEV_MODE:
    file_dir = os.path.join(os.path.dirname(__file__), '..')
    sys.path.append(file_dir)

from federatedscope.core.cmd_args import parse_args
from federatedscope.core.auxiliaries.data_builder import get_data
from federatedscope.core.auxiliaries.utils import setup_seed, update_logger
from federatedscope.core.auxiliaries.worker_builder import get_client_cls, \
    get_server_cls
from federatedscope.core.configs.config import global_cfg
from federatedscope.core.fed_runner import FedRunner

if os.environ.get('https_proxy'):
    del os.environ['https_proxy']
if os.environ.get('http_proxy'):
    del os.environ['http_proxy']

if __name__ == '__main__':
    init_cfg = global_cfg.clone()
    """
        复制一个全局对象global_cfg，并赋值给init_cfg Recursively copy this CfgNode
        init_cfg是一个基于yacs的配置扩展系统的实例化例子
        允许简单键值管理与访问
    """
    args = parse_args()  # 用于将命令行字符串解析为Python对象的对象
    init_cfg.merge_from_file(args.cfg_file)  # 加载args中的--cfg文件
    init_cfg.merge_from_list(args.opts)  # 加载args中的配置键值

    update_logger(init_cfg)  # 创建存放用于存放训练配置、训练结果、评估结果等文件的文件夹，并输出服务器相关信息
    setup_seed(init_cfg.seed)  # 设置初始化种子

    # 加载args中的客户端的配置文件--client_cfg
    client_cfg = CfgNode.load_cfg(open(args.client_cfg_file,
                                       'r')) if args.client_cfg_file else None

    # federated dataset might change the number of clients
    # thus, we allow the creation procedure of dataset to modify the global
    # cfg object
    data, modified_cfg = get_data(config=init_cfg.clone())  # 加载客户端clien数据集，并返回数据集对象和更新后的cfg（对象）
    init_cfg.merge_from_other_cfg(modified_cfg)  # 用新的配置（modified_cfg）更新原来的配置

    init_cfg.freeze()  # 保存当前的全部配置并生成一个新的配置文件 config.yaml

    # 初始化训练对象
    runner = FedRunner(data=data,
                       server_class=get_server_cls(init_cfg),
                       client_class=get_client_cls(init_cfg),
                       config=init_cfg.clone(),
                       client_config=client_cfg)
    # 开始训练模型
    _ = runner.run()

    """
    python federatedscope\main.py --cfg federatedscope/gfl/baseline/fedavg_gin_minibatch_on_cikmcup.yaml --client_cfg federatedscope/gfl/baseline/fedavg_gin_minibatch_on_cikmcup_per_client.yaml
    """