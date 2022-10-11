FROM centos:7
ARG KUBE_VERSION=1.18.6
ARG HELM3_VERSION=3.2.3
ARG GIT_VERSION=2.25.4
ARG NODE_VERSION=14.13.1
ARG MAVEN_VERSION=3.6.3
ARG GO_VERSION=1.14.1


# Change software source
RUN sed -i 's/enabled=1/enabled=0/' /etc/yum/pluginconf.d/fastestmirror.conf \
 && sed -i 's/mirrorlist/#mirrorlist/' /etc/yum.repos.d/*.repo \
 && sed -i 's|#\(baseurl.*\)mirror.centos.org/centos/$releasever|\1mirrors.cloud.tencent.com/centos/$releasever|' /etc/yum.repos.d/*.repo

RUN yum install -y --nogpgcheck  epel-release \
 && sed -e 's|^metalink=|#metalink=|g' \
         -e 's|^#baseurl=https\?://download.fedoraproject.org/pub/epel/|baseurl=http://mirrors.cloud.tencent.com/epel/|g' \
         -i.bak /etc/yum.repos.d/epel.repo \
 && yum install -y ansible



# Add automatic mount point
VOLUME ["/etc/gitlab-runner", "/home/gitlab-runner"]

##Add compilation tools 
RUN yum install -y vim bash  bash-completion wget unzip curl ca-certificates tzdata jq openssh-client \
  && yum groupinstall -y 'Development Tools' 'Legacy UNIX Compatibility' \
  && yum install -y  openssl-devel zlib-devel

# Install openjdk 1.8
RUN yum install -y java-1.8.0-openjdk-devel

# Install Maven tools 
RUN mkdir -p /root/ts \
 && wget -q -P /root/ts https://mirror.azure.cn/apache/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz \
 && tar -xf /root/ts/apache-maven-${MAVEN_VERSION}-bin.tar.gz -C /opt \
 && mkdir -p /root/.m3 \
 && cp /opt/apache-maven-${MAVEN_VERSION}/conf/settings.xml /root/.m3/settings.xml \
 && ln -sf /root/.m3/settings.xml /opt/apache-maven-${MAVEN_VERSION}/conf/settings.xml \
 && rm -rf /root/ts
#
# Install npm
RUN mkdir -p /root/ts \
 && wget -q -P /root/ts https://npm.taobao.org/mirrors/node/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz\
 && tar -xf /root/ts/node-v${NODE_VERSION}-linux-x64.tar.gz -C /opt \
 && rm -rf /root/ts

# Install pythin3
RUN yum install -y python3-devel python3-pip python3-setuptools  yamllint


# Install golang

RUN wget -q -P /root/ts https://mirror.azure.cn/go/go${GO_VERSION}.linux-amd64.tar.gz \
 && tar -xzf /root/ts/go${GO_VERSION}.linux-amd64.tar.gz -C /opt \
 && rm -rf /root/ts


# Install docker
RUN yum install -y yum-utils device-mapper-persistent-data lvm2 \
 && yum-config-manager --add-repo  http://download.docker.com/linux/centos/docker-ce.repo \
 && sed -i 's+download.docker.com+mirrors.cloud.tencent.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo \
 && yum install -y docker-ce docker-compose

# Install git
RUN mkdir -p /root/ts \
 && yum install -y  openssl-devel zlib-devel curl-devel expat-devel gettext-devel \
 && wget -q -P /root/ts "http://mirrors.ustc.edu.cn/kernel.org/software/scm/git/git-${GIT_VERSION}.tar.gz" \
 && tar -xzf /root/ts/git-${GIT_VERSION}.tar.gz -C /root/ts \
 && make -j2 prefix=/usr/local install -C /root/ts/git-${GIT_VERSION} \
 && yum install --nogpgcheck -y git-lfs \
 && git --version \
 && rm -rf /root/ts


# add offical deploy tools, k8s relate
RUN mkdir -pv /root/.m2 /root/.docker /root/.kube 


# kubernetes client.
RUN wget -q http://mirror.azure.cn/kubernetes/kubectl/v${KUBE_VERSION}/bin/linux/amd64/kubectl -O /usr/local/bin/kubectl \
    && chmod +x /usr/local/bin/kubectl 




# helm3
#RUN mkdir -p /root/ts \
# && cd /root/ts \
# && git clone https://gitee.com/chimeh/helm.git \
# && cd helm; git checkout v${HELM3_VERSION} \
# && env GOPROXY="http://mirrors.cloud.tencent.com/go/,https://goproxy.cn,direct" PATH="${PATH}:/opt/go/bin:/root/go/bin" make -j2 -C . \
# && cp /root/ts/helm/bin/helm /usr/local/bin/helm3  \
# && rm -rf /root/ts

RUN mkdir -p /root/ts \
    && wget -q -P /root/ts http://mirror.azure.cn/kubernetes/helm/helm-v${HELM3_VERSION}-linux-amd64.tar.gz \
    && cd /root/ts && tar -xf helm-v${HELM3_VERSION}-linux-amd64.tar.gz \
    && cp /root/ts/linux-amd64/helm /usr/local/bin/ \
    && chmod +x /usr/local/bin/helm



# android
#RUN mkdir -p /root/ts  \
#    &&  wget -q -P /root/ts  https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip \
#    && cd /root/ts \
#    && mkdir -p /opt/android \
#    && unzip  -qq sdk-tools-linux-4333796.zip -d /opt/android \
#    && echo 'Y'|/opt/android/tools/bin/sdkmanager  "build-tools;29.0.3" > sdkmanager.log\
#    && echo 'Y'|/opt/android/tools/bin/sdkmanager "platform-tools" "platforms;android-29" >> sdkmanager.log \
#    && rm -rf /root/ts
## Install gradle
RUN mkdir -p /root/ts \
    &&  wget -q -P /root/ts  https://downloads.gradle-dn.com/distributions/gradle-6.2.2-all.zip \
    && cd /root/ts \
    && mkdir -p /opt/gradle \
    && unzip  -qq gradle-6.2.2-all.zip -d /opt/gradle \
    && rm -rf /root/ts

# gitlab cli
RUN  pip3 install --index-url http://mirrors.cloud.tencent.com/pypi/simple \
  --trusted-host mirrors.cloud.tencent.com --upgrade python-gitlab

# jira ... atlassian cli
# atlassian cli https://marketplace.atlassian.com/search?query=bob%20swift%20cli
# https://bobswift.atlassian.net/wiki/spaces/ACLI/pages/710705369/Docker+Image+for+CLI
#ARG ACLI=atlassian-cli-9.1.1
#RUN mkdir -p /root/ts \
# &&  wget  -q -O /opt/${ACLI}.zip  https://marketplace.atlassian.com/download/plugins/org.swift.atlassian.cli/version/9110 \
# && unzip /opt/${ACLI}.zip -d /opt \
# && rm /opt/${ACLI}.zip \
# && ln -sf  /root/jira/acli.properties /opt/${ACLI}/acli.properties
# && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash

# cloud cli aliyun, tencent cloud
#ADD https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz /opt/aliyun-cli-linux-latest-amd64.tgz
#RUN tar -xf /opt/aliyun-cli-linux-latest-amd64.tgz -C /usr/local/bin && rm -f /opt/aliyun-cli-linux-latest-amd64.tgz \
# && pip3 install --index-url http://mirrors.cloud.tencent.com/pypi/simple --trusted-host mirrors.cloud.tencent.com  coscmd tccli

#rancher cli
#ARG RANCHER_VER=v2.3.1
#RUN wget -q https://releases.rancher.com/cli2/${RANCHER_VER}/rancher-linux-amd64-${RANCHER_VER}.tar.gz -O /opt/rancher-linux-amd64-${RANCHER_VER}.tar.gz \
# && tar -xf /opt/rancher-linux-amd64-${RANCHER_VER}.tar.gz -C /opt \
# && rm /opt/rancher-linux-amd64-${RANCHER_VER}.tar.gz
#
 # redis
# RUN mkdir -p /root/ts \
#     &&  wget -q -P /root/ts  http://mirror.azure.cn/redis/releases/redis-5.0.8.tar.gz \
#     && cd /root/ts \
#     && tar -xf redis-5.0.8.tar.gz \
#     && cd redis-5.0.8 \
#     && make install && rm -rf /root/ts

#
RUN yum install -y git-lfs cmake3 pigz sshpass mercurial
# mail cli, font, 
RUN yum install -y wqy-microhei-fonts mailx expect initscripts tree

#metricd server
#COPY deployments/s2erunner/metricbeat/secrets/filebeat/elastic.repo                 /etc/yum.repos.d/elastic.repo
#RUN yum install -y elasticsearch-7.6.2 kibana-7.6.2 logstash-7.6.2 filebeat-7.6.2 \
# && perl -ni -e 's/sysctl/echo sysctl/g;print' /etc/init.d/elasticsearch

# Install gitlab runner, github runner
#RUN curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | bash \
COPY deployments/runner/secrets/gitlab-runner/gitlab-runner.repo /etc/yum.repos.d/gitlab-runner.repo
RUN yum install -y --nogpgcheck gitlab-runner


#RUN GH_RUNNER_VERSION=${GH_RUNNER_VERSION:-$(curl --silent "https://api.github.com/repos/actions/runner/releases/latest" | grep tag_name | sed -E 's/.*"v([^"]+)".*/\1/')} \
#    && mkdir -p /home/github-runner \
#     && cd /home/github-runner \
#     && curl -L -O https://github.com/actions/runner/releases/download/v${GH_RUNNER_VERSION}/actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz \
#     && tar -zxf actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz \
#     && rm -f actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz \
#     && ./bin/installdependencies.sh \
#     && chown -R root: /home/github-runner


# let fetch ci/cd template via http://localhost
COPY deployments/runner/secrets/gitlab-runner/config.toml /etc/gitlab-runner/config.toml
COPY deployments/runner/secrets/profile.d/env.sh /etc/profile.d/env.sh
COPY deployments/runner/secrets/maven/settings.xml        /root/.m2/settings.xml
COPY deployments/runner/secrets/k8s/                      /root/.kube

# cicd logic script
RUN export PATH="/opt/go/bin/:${PATH}" \
 && go env -w GOPROXY="http://mirrors.cloud.tencent.com/go/,https://goproxy.cn,direct"
# && cd /s2ectl;bash build.sh;

# runner entrypoint
COPY docker /docker

RUN yum -y --disablerepo=* --enablerepo=base,extras,updates,epel update \
 && yum install --nogpgcheck -y sudo bind-utils\
 && echo "gitlab-runner ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
 && yum clean all \
 && rm -rf /var/cache/yum \
 && rm -rf /root/ts \
 && chmod -R +x /docker/ 

ENV PATH="/opt/apache-maven-${MAVEN_VERSION}/bin:/opt/node-v${NODE_VERSION}-linux-x64/bin:/opt/gradle/gradle-6.2.2/bin:/opt/go/bin:/root/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV LANG=en_US.UTF-8
ENV RUNNER_S2I_VERSION=2
RUN echo "PATH=${PATH}" >> /etc/profile.d/env.sh
EXPOSE 8888
ENTRYPOINT ["/docker/docker-entrypoint.sh"]

