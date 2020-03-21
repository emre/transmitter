#### transmitter

Transmitter is a CLI tool for HIVE blockchain witnesses. It quickly
allows you to enable/disable your witness or set some properties for the new
*witness_set_properties* call introduced in Hard Fork 20.

#### Installation

```
$ pip install transmitter
```

#### Configuration (Optional)

If you don't want to repeat yourself while calling commands, create a configuration file on your user directory:

```
$ mkdir -p ~/.transmitter
$ touch ~/.transmitter/config.json
```

Fill it with the corresponding values:

```javascript
{
    "NODES": [
        "https://api.hivekings.com"
    ],
    "WITNESS_ACCOUNT": "<your_witness_account>",
    "SIGNING_KEY": "<signing_key>",
    "ACTIVE_KEY": "<active_key>",
    "DEFAULT_PROPERTIES": {
      "account_creation_fee": "3 STEEM",
      "maximum_block_size": 65536,
      "sbd_interest_rate": 0
    },
    "URL": "https://hive.blog/@emrebeyler"
}
```

All keys are optional. If you don't want to keep your signing key and active key in the config file, that's fine.

You can pass it to the commands in different ways:

- Use ```TRANSMITTER_SIGNING_KEY``` and ```TRANSMITTER_ACTIVE_KEY``` environment values.
- Use --signing-key and --active-key params while running the tool.

That's the same with WITNESS_ACCOUNT and URL parameters. 

```DEFAULT_PROPERTIES``` has a special case. You can't pass it via CLI parameters or environment vars. If you
don't fill that key, transmitter will use the latest props information belongs to your witness account in the blockchain.

#### Enabling the witness

If you want to enable your witness:

```
$ transmitter enable 
```

#### Disabling the witness

```
$ transmitter disable
```

#### Setting a new property

```
$ transmitter set --property account_subsidy_decay=128 --property account_subsidy_budget=2
```

You can send single or multiple parameters.


#### Price feed

```
$ transmitter publish_feed
```


#### Bonus: Installation with Docker

```
$ git clone https://github.com/emre/transmitter.git
$ cd transmitter
```
Edit the config file as you wish:

```
$ vim config.json.docker 
$ docker build -t transmitter .
```

After that, you can run the transmitter like ```docker run -t transmitter <command>```.

Example: 

```
➜  transmitter git:(master) ✗ docker run -t transmitter disable
2018-10-08 19:14:20,326 - transmitter.main - INFO - Connecting to the blockchain using mainnet.
2018-10-08 19:14:21,007 - transmitter.main - INFO - Got the SIGNING_KEY in the config file.
2018-10-08 19:14:21,238 - transmitter.main - INFO - Got the WITNESS_ACCOUNT in the config file.
2018-10-08 19:14:21,403 - transmitter.main - INFO - Got the URL in the config file.
2018-10-08 19:14:21,403 - transmitter.main - INFO - Disabling the witness: <Witness emrebeyler>
2018-10-08 19:14:24,823 - transmitter.main - INFO - Operation broadcasted.
```

#### Disclaimer

Even though, I use ```transmitter``` in my witness operations, it's strongly advised for you
to review and audit the code before using it. This software may include bugs, use it at your own risk.
