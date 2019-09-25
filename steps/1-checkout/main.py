# 1. Checkout
# 2. Static analysis
# 3. Set up AWS
# 4. Start jobs


# $ mkdir foo && cd foo
# $ git init
# $ git fetch --depth 1 https://github.com/some/repo pull/123/merge
# $ git checkout FETCH_HEAD


from contextlib import contextmanager
import importlib
import os
import pathlib
import subprocess
import sys
import tempfile


def call_git(*cmd, **opts):
    return subprocess.run(
        ['git', *map(str, cmd)],
        check=True,
    )


@contextmanager
def make_checkout(url: str, ref: str, branch: str):
    """
    url: git url to check out
    ref: git ref to check out
    branch: local branch name to give ref
    """
    with tempfile.TemporaryDirectory() as workdir:
        call_git('init', cwd=workdir)
        # TODO: set up authentication
        call_git('fetch', '--depth', '1', url, ref, cwd=workdir)
        call_git('checkout', '-b', branch, 'FETCH_HEAD')

        @contextmanager
        def make_tarball():
            with tempfile.TemporaryFile() as tarbuff:
                subprocess.run(
                    ['tar', '-c', *os.listdir(workdir)], check=True,
                    cwd=workdir, stdout=tarbuff
                )
                tarbuff.seek(0)
                yield tarbuff

        yield pathlib.Path(workdir), make_tarball


def guess_project_type(workdir: pathlib.Path):
    if (workdir / 'pyproject.toml').exists():
        return 'python.pep517'
    elif (workdir / 'setup.py').exists() or (workdir / 'setup.cfg').exists():
        return 'python.setuptools'
    # TODO: NPM, ruby+gem
    else:
        return None


def get_builder_class(kind):
    mod = importlib.import_module(f'builders.{kind}')
    return mod.__builder__


def main(config):
    with make_checkout(..., ..., ...) as (workdir, make_tarball):
        kind = guess_project_type(workdir)
        if kind is None:
            return "Unable to determine type of project; aborting"

        builder = get_builder_class(kind)(config)

        with make_tarball() as tarbuff:
            s3object = builder.upload_checkout(tarbuff)

        builder.set_up_aws(checkout=s3object)
        builder.run()


if __name__ == '__main__':
    sys.exit(main({}))
