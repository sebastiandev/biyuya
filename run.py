#!/usr/bin/env python

import os

opt = {
    'HOST': os.getenv('BIYUYA_BACKEND_HOST', '0.0.0.0'),
    'PORT': int(os.getenv('BIYUYA_BACKEND_PORT', 8080)),
}

if __name__ == '__main__':
    import argparse
    args_parser = argparse.ArgumentParser(description="Launch Biyuya Api")
    args = args_parser.parse_args()

    from biyuya import app
    app.run(port=opt['PORT'], host=opt['HOST'])
