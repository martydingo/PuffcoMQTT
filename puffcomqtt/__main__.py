import argparse
import puffcomqtt

argSetup = argparse.ArgumentParser()
argSetup.add_argument("-c", "--config", required=True)
args = argSetup.parse_args()

PuffcoMQTT = puffcomqtt.PuffcoMQTT(args.config)
