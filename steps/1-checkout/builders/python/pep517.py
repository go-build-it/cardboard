import boto3


class Pep517Builder:
    def __init__(self, config):
        ...

    def upload_checkout(self, fobj):
        ...

    def set_up_aws(self, checkout):
        ...

    def run(self):
        ...


__builder__ = Pep517Builder
