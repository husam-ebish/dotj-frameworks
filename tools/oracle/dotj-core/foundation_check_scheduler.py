"""Bounded execution for independent candidate checks; serial phases fail before the next step."""
from concurrent.futures import ThreadPoolExecutor


def run_checks(names, execute, *, workers=1, emit=None):
    names=tuple(names)
    if workers not in (1,2,3):
        raise ValueError('Foundation check workers must be between one and three')

    def accept(name,result):
        passed=any(line=='PASS' or line.startswith('PASS ') for line in result.stdout.splitlines())
        if result.returncode or not passed:
            raise RuntimeError(f'{name} failed ({result.returncode})\n{result.stdout}{result.stderr}')
        if emit is not None:
            emit(result.stdout.strip())

    if workers==1:
        for name in names:
            accept(name,execute(name))
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pending=[pool.submit(execute,name) for name in names]
            try:
                for name,future in zip(names,pending):
                    accept(name,future.result())
            except BaseException:
                for future in pending:
                    future.cancel()
                raise
    return list(names)
