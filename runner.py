#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Small helper script to run the flask app and celery worker
#

import subprocess


def main():
    try:
        flask_process = subprocess.Popen(
            ['python', 'app.py']
        )

        celery_process = subprocess.Popen(
            ['celery', 'worker', '-A', 'app.celery', '--loglevel=info']
        )

        flask_process.wait()
        celery_process.wait()

    except KeyboardInterrupt:
        print("\n Caught KeyboardInterrupt")

    finally:
        if flask_process.poll() is None:
            flask_process.kill()
        if celery_process.poll() is None:
            celery_process.kill()

if __name__ == "__main__":
    main()
