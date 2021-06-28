# 指定基础镜像
FROM python:3.6
ADD requirements.txt /
# 安装项目依赖项
RUN pip3 install -U pip wheel cmake -i https://pypi.mirrors.ustc.edu.cn/simple/
RUN pip3 install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
ADD . /app
WORKDIR /app
# 为启动脚本添加执行权限
ADD start.sh /
RUN chmod 755 start.sh
# 容器启动时要执行的命令
ENTRYPOINT ["./start.sh"]
# 暴露端口
EXPOSE 5000