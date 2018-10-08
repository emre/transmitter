import argparse
import getpass
import json
import logging
import os
from os.path import exists
from os.path import expanduser

from beem.steem import Steem
from beem.witness import Witness
from beemgraphenebase.account import PrivateKey

from .constants import (NULL_WITNESS_KEY, ENV_KEYS, CONFIG_FILE)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig()


class Transmitter:

    def __init__(self, config_file, signing_key=None, active_key=None,
                 witness_account=None, url=None):

        self.config = self.get_config(config_file)
        self.steem = self.get_steem_instance(self.config, keys=None)

        # Private signing key
        if signing_key:
            self.signing_key = PrivateKey(signing_key)
            logger.info(f"Got the SIGNING_KEY in the parameters.")
        else:
            self.signing_key = self._get_config_key('SIGNING_KEY', is_key=True)

        # Convert the witness account string into beem.Witness
        if witness_account:
            self.witness_account = witness_account
            logger.info("Got the WITNESS_ACCOUNT in the parameters.")
        else:
            self.witness_account = self._get_config_key('WITNESS_ACCOUNT')
        self.witness_account = Witness(
            self.witness_account, steem_instance=self.steem)

        # register the witness URL
        if url:
            logger.info("Got the URL in the parameters.")
            self.url = url
        else:
            self.url = self._get_config_key('URL')

        # register the active key if it's passed by CLI.
        self.active_key = active_key

    def get_config(self, config_file):
        if not exists(config_file):
            logger.warning(
                f'Warning: No config file found at {config_file}.')
            config = {}
        else:
            config = json.loads(open(config_file).read())

        return config

    def get_steem_instance(self, config, keys=None):
        if not keys:
            keys = []

        logger.info("Connecting to the blockchain using mainnet.")
        nodes = config.get("nodes") or ["https://api.steemit.com"]
        steem = Steem(node=nodes, keys=keys)

        return steem

    def _get_config_key(self, config_key, is_key=False):

        # check config file
        if config_key in self.config:
            logger.info(f"Got the {config_key} in the config file.")
            if is_key:
                return PrivateKey(
                    self.config.get(config_key))
            else:
                return self.config.get(config_key)

        # check the environment vars
        config_val = os.getenv(ENV_KEYS[config_key])
        if config_val:
            logger.info(f"Got the {config_key} in the environment vars.")
            if is_key:
                return PrivateKey(config_val)
            return config_val

        if is_key:
            config_val = PrivateKey(
                getpass.getpass(f"{config_key}:\n"))
        else:
            config_val = input(f"{config_key}:\n")

        return config_val

    def get_active_key(self):
        if self.active_key:
            return PrivateKey(self.active_key)

        active_key = self._get_config_key('ACTIVE_KEY', is_key=True)
        return active_key

    def _get_base_properties(self):
        default_props = self.config.get("DEFAULT_PROPERTIES")
        if not default_props:
            logger.info("Couldn't find DEFAULT_PROPERTIES in the config. "
                             "Falling back to latest props on the blockchain.")
            default_props = self.witness_account["props"]

        if not default_props:
            raise ValueError('Cannot identify default properties.')
        return default_props

    def enable(self):
        self.steem = self.get_steem_instance(
            self.config, keys=[self.get_active_key()])
        props = self._get_base_properties()

        self.steem.witness_update(
            str(self.signing_key.pubkey),
            self.url,
            props,
            account=self.witness_account["owner"],
        )
        logger.info(f'Operation broadcasted.')

    def disable(self):
        logger.info(f"Disabling the witness: {self.witness_account}")
        self.steem.witness_set_properties(
            str(self.signing_key),
            self.witness_account["owner"],
            {
                "new_signing_key": NULL_WITNESS_KEY,
            }
        )
        logger.info(f'Operation broadcasted.')

    def set(self, properties):
        if not len(properties):
            raise ValueError('Choose a property to set.')

        props = {}
        for _property in properties:
            key, val = _property.split("=")
            try:
                props[key] = int(val)
            except ValueError:
                props[key] = val

        self.steem.witness_set_properties(
            str(self.signing_key),
            self.witness_account["owner"],
            props,
        )
        logger.info(f'Operation broadcasted.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        help="An action to perform.",
        choices=["enable", "disable", "set"])
    parser.add_argument('--signing-key', help="Private signing key")
    parser.add_argument('--active-key', help="Private active key")
    parser.add_argument('--witness-account', help="Witness account")
    parser.add_argument('--property', action="append")
    parser.add_argument('--url', help="Witness URL")

    args = parser.parse_args()

    config_file = expanduser(CONFIG_FILE)
    transmitter = Transmitter(
        config_file,
        signing_key=args.signing_key,
        witness_account=args.witness_account,
        url=args.url,
    )
    if args.property:
        getattr(transmitter, args.action)(args.property)
    else:
        getattr(transmitter, args.action)()


if __name__ == '__main__':
    main()
