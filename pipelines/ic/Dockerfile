FROM us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-8:m92

WORKDIR /

COPY . .

# for debugging - shouldn't go to pipelines
RUN sudo apt-get install vim

RUN pip install google-cloud-storage

ENTRYPOINT ["python", "-m", "trainer.task"]
