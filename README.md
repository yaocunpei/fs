# CIKM 2022 AnalytiCup Competition 参赛代码 #
团队名：**小跟班**
## 命令行运行指令 ##
1.下载官方数据集至`data`文件夹\
2.进入到`fs`文件夹\
3.然后在命令行运行以下指令
```commandline
federatedscope\main.py --cfg federatedscope/gfl/baseline/fedavg_gin_minibatch_on_cikmcup.yaml --client_cfg federatedscope/gfl/baseline/fedavg_gin_minibatch_on_cikmcup_per_client.yaml
```
## 所开发算法简介 ##
在FedAvg算法的基础上，通过调节 `federate.total_round_num` 和 `train.local_update_steps` 来改善算法